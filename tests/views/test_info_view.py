from tests.test_client import TestClient


class TestInfoView(TestClient):
    """ Info view unit tests"""

    def test_info(self):

        # Given the application is running
        # When a get is made to the info end point
        response = self.client.get('/info', headers=self.get_auth_headers())

        # Then the info returns a 200
        self.assertStatus(response, 200)
        self.assertIn('rm-comms-template', response.data.decode())
