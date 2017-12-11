import json

from tests.test_client import TestClient


class TestTemplateView(TestClient):
    """ Template View unit tests"""

    def _upload_template(self, template_id, data):
        response = self.client.post('/template/{}'.format(template_id), content_type='application/json',
                                    data=json.dumps(data))
        self.assertStatus(response, 201)

    def test_comms_template_upload(self):
        # When a valid comms template is uploaded
        data = dict(id="cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99", label="test data", type="EMAIL", uri="test-uri.com",
                    classification={"GEOGRAPHY": "NI"})
        response = self.client.post('/template/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99', content_type='application/json',
                                    data=json.dumps(data))

        # Then it is uploaded successfully with a 201 response
        self.assertStatus(response, 201)

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

    def test_get_only_matching_templates_by_classifier(self):
        # Given there are multiple templates in the database
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef89"
        classifiers = {"GEOGRAPHY": "NI"}
        data = dict(id=template_id, label="test data", type="EMAIL", uri="test-uri.com",
                    classification=classifiers)
        self._upload_template(template_id, data)

        template_id_2 = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99"
        classifiers_2 = {"GEOGRAPHY": "ENGLAND"}
        data_2 = dict(id=template_id_2, label="test data", type="EMAIL", uri="test-uri.com",
                      classification=classifiers_2)
        self._upload_template(template_id_2, data_2)

        # When i attempt to get templates by matching classifier
        response = self.client.get("/template?GEOGRAPHY=NI")

        # Then i receive a 200 response and a list of matching templates
        return_object = data.copy()
        return_object["params"] = None

        self.assertStatus(response, 200)
        self.assertEquals(response.json, [return_object])

    def test_get_non_existent_template_by_classifier(self):
        # Given no template is in the database

        # When we attempt to get the template by it's classifiers
        response = self.client.get("/template?GEOGRAPHY=NI")

        # Then we receive a 404 response
        self.assertStatus(response, 404)
        self.assertEquals(response.json, None)

    def test_get_multiple_templates_by_classifier(self):
        # Given there are multiple matching templates in the database
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef89"
        classifiers = {"GEOGRAPHY": "NI"}
        data = dict(id=template_id, label="test data", type="EMAIL", uri="test-uri.com", classification=classifiers)
        self._upload_template(template_id, data)

        template_id2 = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef90"
        data2 = dict(id=template_id2, label="test data", type="EMAIL", uri="test-uri.com", classification=classifiers)
        self._upload_template(template_id2, data2)

        # When i attempt to get templates by matching classifier
        response = self.client.get("/template?GEOGRAPHY=NI")

        # Then i receive a 200 response and a list of matching templates
        return_object = data.copy()
        return_object["params"] = None
        return_object1 = data2.copy()
        return_object1["params"] = None

        self.assertStatus(response, 200)
        self.assertEquals(response.json, [return_object, return_object1])
