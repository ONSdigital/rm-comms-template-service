from application.controllers.template_controller import UPLOAD_SUCCESSFUL
from tests.test_client import TestClient


class TestTemplateView(TestClient):
    """ Template View unit tests"""

    def test_comms_template_upload(self):
        # request_data = dict()
        # When a valid comms template is uploaded
        response = self.client.post('/upload/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef97', content_type='application/json',
                                    data={})
        print(response.json.errors)

        self.assertStatus(response, 200)
        self.assertEquals(response.data.decode(), UPLOAD_SUCCESSFUL)
