from config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/postgres"
