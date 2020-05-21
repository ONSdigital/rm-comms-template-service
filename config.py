import os


class Config:
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", 8182)
    VERSION = os.getenv('VERSION', '0.3.0')
    DEBUG = os.getenv("DEBUG", False)
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI',
                                        'postgresql://postgres:postgres@localhost:5432/postgres')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True  # This handles session rollback on exception and commit on success,
    # https://github.com/mitsuhiko/flask-sqlalchemy/pull/115/files

    SECURITY_USER_NAME = os.getenv('SECURITY_USER_NAME', 'admin')
    SECURITY_USER_PASSWORD = os.getenv('SECURITY_USER_PASSWORD', 'secret')
