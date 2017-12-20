import os


class Config(object):
    NAME = os.getenv('NAME', "rm-comms-template")
    SCHEME = os.getenv("SCHEME", "http")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", 8081)
    DEBUG = os.getenv("DEBUG", False)
    SCHEMA = os.getenv("SCHEMA", "templatesvc")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI",
                                        "postgres://postgres:postgres@db:5432/postgres")
    # Needs to be "postgres://postgres:postgres@localhost:6432/postgres" for gunicorn to work locally
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # This handles session rollback on exception and commit on success,
    # https://github.com/mitsuhiko/flask-sqlalchemy/pull/115/files

    SECURITY_USER_NAME = os.getenv('SECURITY_USER_NAME', 'dummy_user')
    SECURITY_USER_PASSWORD = os.getenv('SECURITY_USER_PASSWORD', 'dummy_password')
