import base64
from flask_testing import TestCase
from flask import current_app

from application.models.models import CommunicationTemplate
from application.models.classification_type import ClassificationType
from run import create_app


class TestClient(TestCase):

    def get_auth_headers(self):
        auth = f'{current_app.config.get("SECURITY_USER_NAME")}:{current_app.config.get("SECURITY_USER_PASSWORD")}'
        return {
            'Authorization': 'Basic %s' % base64.b64encode(bytes(auth, "utf-8")).decode("ascii")
        }

    @staticmethod
    def create_app():
        return create_app("tests.config.TestConfig")

    def tearDown(self):
        session = current_app.db.session()
        session.query(CommunicationTemplate).delete()
        session.query(ClassificationType).delete()
