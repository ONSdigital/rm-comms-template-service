from flask_testing import TestCase
from flask import current_app

from application.models.models import CommunicationTemplate
from application.models.classification_type import ClassificationType
from run import create_app


class TestClient(TestCase):

    @staticmethod
    def create_app():
        return create_app("tests.config.TestConfig")

    def tearDown(self):
        session = current_app.db.session()
        session.query(CommunicationTemplate).delete()
        session.query(ClassificationType).delete()
