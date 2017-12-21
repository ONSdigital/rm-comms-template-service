from application.utils.basic_auth import get_pw
from flask import current_app
from tests.test_client import TestClient


class TestBasicAuth(TestClient):

    def test_getpw(self):
        password = get_pw(current_app.config.get('SECURITY_USER_NAME'))
        self.assertEquals(password, current_app.config.get('SECURITY_USER_PASSWORD'))