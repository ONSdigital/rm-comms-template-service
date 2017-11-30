import os


class Config(object):
    NAME = os.getenv('NAME', "rm-comms-template")
    SCHEME = os.getenv("SCHEME", "http")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = os.getenv("PORT", 8081)
    DEBUG = os.getenv("DEBUG", False)
    SCHEMA = os.getenv("SCHEMA", "templatesvc")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI",
                                        "postgres://postgres:postgres@postgres:5432/postgres")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", False)



