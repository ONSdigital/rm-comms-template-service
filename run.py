import logging
import os
import structlog


from flask import Flask, _app_ctx_stack
from flask_cors import CORS
from retrying import RetryError, retry
from sqlalchemy import create_engine, column, text
from sqlalchemy.exc import ProgrammingError, DatabaseError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import exists, select
from json import loads


def create_app():
    # create and configure the Flask app
    app = Flask(__name__)
    app_config = 'config.{}'.format('Config')
    app.config.from_object(app_config)

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
    logging.error(exception)
    return isinstance(exception, DatabaseError) and not isinstance(exception, ProgrammingError)


@retry(retry_on_exception=retry_if_database_error, wait_fixed=2000, stop_max_delay=30000, wrap_exception=True)
def initialise_db(app):
    app.db = create_database(app.config['SQLALCHEMY_DATABASE_URI'],
                             app.config['SCHEMA'])


def create_database(db_connection, db_schema):
    from application.models import models

    def current_request():
        return _app_ctx_stack.__ident_func__()

    engine = create_engine(db_connection, convert_unicode=True)
    session = scoped_session(sessionmaker(), scopefunc=current_request)
    session.configure(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    engine.session = session

    if db_connection.startswith('postgres'):

        for t in models.Base.metadata.sorted_tables:
            t.schema = db_schema

        schemata_exists = exists(select([column('schema_name')])
                                 .select_from(text("information_schema.schemata"))
                                 .where(text(f"schema_name = '{db_schema}'")))

        if not session().query(schemata_exists).scalar():
            logging.info("Creating schema ", db_schema=db_schema)
            engine.execute(f"CREATE SCHEMA {db_schema}")
            logging.info("Creating database tables.")
            models.Base.metadata.create_all(engine)

    else:
        logging.info("Creating database tables.")
        models.Base.metadata.create_all(engine)

    logging.info("Ok, database tables have been created.")
    return engine


if __name__ == '__main__':
    config_path = "config.Config"

    app = create_app()

    try:
        initialise_db(app)
    except RetryError:
        logging.exception('Failed to initialise database')
        exit(1)

    host, port = app.config['HOST'], int(app.config['PORT'])
    logging.error(port)
    app.run(debug=app.config['DEBUG'], host=host, port=port)
