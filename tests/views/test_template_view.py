import json

from application.controllers.template_controller import UPLOAD_SUCCESSFUL
from tests.test_client import TestClient


class TestTemplateView(TestClient):
    """ Template View unit tests"""

    def _upload_template(self, template_id, data):
        response = self.client.post('/template/{}'.format(template_id), content_type='application/json',
                                    data=json.dumps(data))

        self.assertStatus(response, 201)
        self.assertEquals(response.data.decode(), UPLOAD_SUCCESSFUL)

    def test_comms_template_upload(self):
        # When a valid comms template is uploaded
        data = dict(id="cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99", label="test data", type="EMAIL", uri="test-uri.com",
                    classification={"GEOGRAPHY": "NI"})
        response = self.client.post('/template/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99', content_type='application/json',
                                    data=json.dumps(data))

        # Then it is uploaded successfully with a 201 response
        self.assertStatus(response, 201)
        self.assertEquals(response.data.decode(), UPLOAD_SUCCESSFUL)

    def test_invalid_comms_template_upload_(self):
        # When an invalid comms template is uploaded
        data = dict(label="test data")
        response = self.client.post('/template/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99', content_type='application/json',
                                    data=json.dumps(data))

        # Then we receive a 400 response with a validation message
        self.assertStatus(response, 400)
        self.assertEquals(response.json, {"error": "'id' is a required property"})

    def test_get_template_by_id(self):
        # Given there is a template in the database
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef89"
        data = dict(id=template_id, label="test data", type="EMAIL", uri="test-uri.com",
                    classification={"GEOGRAPHY": "NI"})
        self._upload_template(template_id, data)

        # When the template is searched by id
        response = self.client.get('/template/{}'.format(template_id))

        # A 200 response and the correct data is received
        self.assertStatus(response, 200)

        expected_response_json = dict(id=template_id, label="test data", type="EMAIL", uri="test-uri.com",
                                      classification={"GEOGRAPHY": "NI"}, params=None)
        self.assertEquals(response.json, expected_response_json)

    def test_get_non_existent_template(self):
        # Given a template does not exist in the database
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef79"

        # When the template is searched by id
        response = self.client.get('/template/{}'.format(template_id))

        self.assertStatus(response, 404)
