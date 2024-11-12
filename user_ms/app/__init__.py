import os
from flask import Flask
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
from urllib.parse import quote_plus
from sqlalchemy.engine.url import URL

# Inicialización de bases de datos y marshmallow
db = SQLAlchemy()
metadata = db.metadata
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    load_dotenv()

    # Configuración de la base de datos usando URL.create
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

    # Exportador de trazas a Azure Monitor
    if connection_string:
        trace_exporter = AzureMonitorTraceExporter(connection_string=connection_string)
        tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))

    # Instrumentación de Flask y Requests
    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app