from flask_testing import TestCase
from run import create_app


class TestClient(TestCase):

    @staticmethod
    def create_app():
        return create_app("tests.config.TestConfig")

    @staticmethod
    def tearDown():
        # TODO: TRUNCATE POSTGRES TABLES IN DOCKER CONTAINER,
        # TODO: also relies on docker container being up, could start it in startup (needs to really be clean)
        pass
