from application.controllers.template_controller import UPLOAD_SUCCESSFUL
from application.error_handlers import INVALID_TEMPLATE_MESSAGE
from tests.test_client import TestClient
import json


class TestTemplateView(TestClient):
    """ Template View unit tests"""

    def _insert_test_data(self, template_id, data):
        response = self.client.post('/upload/{}'.format(template_id), content_type='application/json',
                                    data=json.dumps(data))

        self.assertStatus(response, 201)
        self.assertEquals(response.data.decode(), UPLOAD_SUCCESSFUL)

    def test_comms_template_upload(self):
        # When a valid comms template is uploaded
        data = dict(id="cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99", label="test data", type="EMAIL", uri="test-uri.com",
                    classification={"GEOGRAPHY": "NI"})
        response = self.client.post('/upload/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99', content_type='application/json',
                                    data=json.dumps(data))

        # Then it is uploaded successfully with a 201 response
        self.assertStatus(response, 201)
        self.assertEquals(response.data.decode(), UPLOAD_SUCCESSFUL)

    def test_invalid_comms_template_upload_(self):
        # When an invalid comms template is uploaded
        data = dict(label="test data")
        response = self.client.post('/upload/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99', content_type='application/json',
                                    data=json.dumps(data))

        # Then it is uploaded successfully with a 400 response
        self.assertStatus(response, 400)
        self.assertEquals(response.json, {"error": INVALID_TEMPLATE_MESSAGE})

    def test_get_template_by_id(self):
        # Given there is a template in the database
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef89"
        data = dict(id=template_id, label="test data", type="EMAIL", uri="test-uri.com",
                    classification={"GEOGRAPHY": "NI"})
        self._insert_test_data(template_id, data)

        # When the template is searched by id
        response = self.client.get('/template/{}'.format(template_id))

        # A 200 response and the correct data is received
        self.assertStatus(response, 200)

        expected_response_json = dict(id=template_id, label="test data", type=0, uri="test-uri.com",
                                      classification={"GEOGRAPHY": "NI"}, params=None)
        self.assertEquals(response.json, expected_response_json)
