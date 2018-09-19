import logging
import structlog

from flask_cors import CORS
from flask import Flask
from sqlalchemy import event, DDL
from sqlalchemy.exc import ProgrammingError, DatabaseError
from retrying import RetryError, retry

from application.utils.logging import configure_structlogger
from application.models.models import db

logger = structlog.wrap_logger(logging.getLogger(__name__))


def create_app(config_path):
    # create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(config_path)

    # register view blueprints
    from application.views.info_view import info_view
    from application.views.template_view import template_view
    from application.views.classification_type_view import classification_type_view
    from application import error_handlers
    app.register_blueprint(info_view)
    app.register_blueprint(template_view)
    app.register_blueprint(classification_type_view)
    app.register_blueprint(error_handlers.blueprint)

    CORS(app)
    return app


def retry_if_database_error(exception):
    logger.error("Error when initialising database", error=exception)
    return isinstance(exception, DatabaseError) and not isinstance(exception, ProgrammingError)


@retry(retry_on_exception=retry_if_database_error, wait_fixed=2000, stop_max_delay=30000, wrap_exception=True)
def initialise_db(app):
    from application.models.models import CommunicationTemplate, CommunicationType # NOQA  # pylint: disable=wrong-import-position
    from application.models.classification_type import ClassificationType # NOQA  # pylint: disable=wrong-import-position

    # Set up database
    with app.app_context():
        db.init_app(app)
        # Creates the schema, can't create the tables otherwise
        event.listen(db.metadata, 'before_create', DDL("CREATE SCHEMA IF NOT EXISTS templatesvc"))
        # Creates the tables from the models
        db.create_all()


if __name__ == '__main__':
    config_path = "config.Config"

    app = create_app(config_path)

    configure_structlogger(app.config)

    try:
        initialise_db(app)
    except RetryError:
        logger.exception('Failed to initialise database')
        exit(1)

    host, port = app.config['HOST'], int(app.config['PORT'])

    app.run(debug=app.config['DEBUG'], host=host, port=port)
