import os
from flask import Flask, request
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_marshmallow import Marshmallow
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry._logs import set_logger_provider
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
# MANTENER: Importaciones específicas para manejo de URLs de DB
from urllib.parse import quote_plus
from sqlalchemy.engine.url import URL
# NUEVO: Importaciones adicionales para telemetría mejorada
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.trace.status import Status, StatusCode
from functools import wraps

# Inicialización de bases de datos y marshmallow
db = SQLAlchemy()
metadata = db.metadata
ma = Marshmallow()

# NUEVO: Decorador para trazar operaciones de usuario
def trace_user_operation(operation_name):
    """
    Decorador para agregar trazabilidad detallada a operaciones de usuario
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span(f"user_operation.{operation_name}") as span:
                try:
                    span.set_attribute("user_operation.name", operation_name)
                    if 'user_id' in kwargs:
                        span.set_attribute("user_operation.user_id", kwargs['user_id'])
                    
                    result = f(*args, **kwargs)
                    
                    span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise
        return wrapper
    return decorator

def create_app():
    app = Flask(__name__)
    load_dotenv()

    # MANTENER: Tu configuración actualizada de base de datos usando URL.create
    db_url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME")
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url

    # Inicialización de base de datos
    db.init_app(app)
    migrate = Migrate(app, db)

    # Registro de blueprints
    from app.controllers.home_controllers import home
    from app.controllers.user_controllers import user
    from app.controllers.health_controller import health
    app.register_blueprint(health, url_prefix='/api')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(home, url_prefix='/home')

    # Configuración de OpenTelemetry
    connection_string = os.getenv('CONNECTION_STRING')
    service_name = os.getenv('OTEL_SERVICE_NAME', 'user-ms')

    # Inicialización de Logger Provider
    logger_provider = LoggerProvider()
    set_logger_provider(logger_provider)

    if connection_string:
        # Exportador de logs a Azure Monitor
        log_exporter = AzureMonitorLogExporter(connection_string=connection_string)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

        # Configuración de logging de Python
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        handler = LoggingHandler()
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    else:
        print("CONNECTION_STRING no encontrado en variables de entorno.")

    # Configuración de OpenTelemetry para trazas
    tracer_provider = TracerProvider(
        resource=Resource.create({
            SERVICE_NAME: service_name,
            "service.namespace": "my-namespace",
            "deployment.environment": os.getenv('ENVIRONMENT', 'development')
        })
    )
    trace.set_tracer_provider(tracer_provider)

    if connection_string:
        trace_exporter = AzureMonitorTraceExporter(connection_string=connection_string)
        tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))

    # NUEVO: MEJORAS DE TELEMETRÍA

    # Configuración mejorada de Flask Instrumentor
    FlaskInstrumentor().instrument_app(
        app,
        excluded_urls="health,metrics",
        request_hook=lambda span, environ: span.set_attribute(
            "custom.user_agent", environ.get("HTTP_USER_AGENT", "")
        ) if span else None
    )

    # Configuración mejorada de Requests
    RequestsInstrumentor().instrument(
        tracer_provider=tracer_provider,
    )

    # Instrumentación de SQLAlchemy
    SQLAlchemyInstrumentor().instrument(
        engine=db.engine,
        enable_commenter=True,
        commenter_options={
            "db_framework": "sqlalchemy",
            "application": "user-ms"
        }
    )

    # Middleware para enriquecer las trazas HTTP
    @app.before_request
    def before_request():
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("user_ms.version", "1.0.0")
            span.set_attribute("user_ms.environment", os.getenv('ENVIRONMENT', 'development'))
            span.set_attribute("http.request_id", request.headers.get("X-Request-ID", ""))

    # Middleware para registrar información de respuesta
    @app.after_request
    def after_request(response):
        span = trace.get_current_span()
        if span.is_recording():
            span.set_attribute("http.status_code", response.status_code)
            span.set_attribute("http.response_content_length", 
                             response.headers.get("Content-Length", 0))
        return response

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app