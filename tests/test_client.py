from flask_testing import TestCase
from application.utils.session_wrapper import with_db_session
from application.models.models import CommunicationTemplate
from run import create_app


class TestClient(TestCase):

    @staticmethod
    def create_app():
        return create_app("tests.config.TestConfig")

    def tearDown(self):
        self.cleardown_database()

    @with_db_session
    def cleardown_database(self, session):
        session.query(CommunicationTemplate).delete()
