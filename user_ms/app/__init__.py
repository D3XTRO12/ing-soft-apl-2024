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

db = SQLAlchemy()
metadata = db.metadata

ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    load_dotenv()

    # Load the configuration
    db_parameters = {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "database": os.getenv("DB_NAME")
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{db_parameters['user']}:{db_parameters['password']}@{db_parameters['host']}:{db_parameters['port']}/{db_parameters['database']}"

    # Initialize the database
    db.init_app(app)

    migrate = Migrate(app)
    migrate.init_app(app, db)

    from app.controllers.user_controllers import user, home
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(home, url_prefix='')
    #app.register_blueprint(category, url_prefix='/category')
    #app.register_blueprint(vehicle, url_prefix='/vehicle')

    # Configuración de OpenTelemetry
    logger_provider = LoggerProvider()
    set_logger_provider(logger_provider)
    connection_string = os.getenv('CONNECTION_STRING')
    if connection_string:
        exporter = AzureMonitorLogExporter(connection_string=connection_string)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    else:
        print("CONNECTION_STRING not found in environment variables.")

    # Configuración del manejador de registros y configuración del nivel de registro
    handler = LoggingHandler()
    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)

    app.config['OTEL_SERVICE_NAME'] = os.getenv('OTEL_SERVICE_NAME', 'user-ms')

    # Configure tracer with Azure Monitor service name
    tracer_provider = TracerProvider(
        resource=Resource.create({
            SERVICE_NAME: app.config['OTEL_SERVICE_NAME'],
            "service.namespace": "my-namespace",  # Optional: add namespace
            "deployment.environment": os.getenv('ENVIRONMENT', 'development')
        })
    )
    trace.set_tracer_provider(tracer_provider)

    # Habilitar la instrumentación de trazas para la biblioteca Flask
    FlaskInstrumentor().instrument_app(app)

    RequestsInstrumentor().instrument()

    trace_exporter = AzureMonitorTraceExporter(connection_string=connection_string)
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(trace_exporter)
    )

    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app