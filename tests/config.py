from config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI",
                                        "postgres://postgres:postgres@localhost:5432/postgres")

