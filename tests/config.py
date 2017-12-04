from config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:postgres@localhost:6432/postgres"
