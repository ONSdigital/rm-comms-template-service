from flask_testing import TestCase
from run import create_app


class TestClient(TestCase):

    @staticmethod
    def create_app():
        return create_app("tests.config.TestConfig")
