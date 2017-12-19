import json
from tests.test_client import TestClient


class TestTemplateView(TestClient):
    """ Template View unit tests"""

    def _create_template(self, template_id, data):
        response = self.client.post(f'/template/{template_id}', content_type='application/json',
                                    data=json.dumps(data), headers=self.get_auth_headers())
        self.assertStatus(response, 201)

    def _create_classification_type(self, classification_type):
        response = self.client.post(f'/classificationtype/{classification_type}', headers=self.get_auth_headers())
        self.assertStatus(response, 201)

    def test_create_comms_template(self):
        # Given the classification type exists
        self._create_classification_type("GEOGRAPHY")

        # When a valid comms template is uploaded
        data = dict(id="cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99", label="test data", type="EMAIL", uri="test-uri.com",
                    classification={"GEOGRAPHY": "NI"})
        response = self.client.post('/template/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99', content_type='application/json',
                                    data=json.dumps(data), headers=self.get_auth_headers())

        # Then it is Created
        self.assertStatus(response, 201)

    def test_create_comms_template_with_no_classification_types_in_database(self):
        # Given no classification types exist

        # When a valid comms template is uploaded
        data = dict(id="cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99", label="test data", type="EMAIL", uri="test-uri.com",
                    classification={"GEOGRAPHY": "NI"})

        response = self.client.post('/template/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99', content_type='application/json',
                                    data=json.dumps(data), headers=self.get_auth_headers())

        # Then we receive an appropriate error message
        self.assertStatus(response, 500)
        self.assertEquals(response.json["error"], 'There are no classification types available to create a template')

    def test_create_comms_template_without_basic_auth(self):
        # Given the classification type exists
        self._create_classification_type("GEOGRAPHY")

        # When a valid comms template is uploaded without correct basic auth
        data = dict(id="cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99", label="test data", type="EMAIL", uri="test-uri.com",
                    classification={"GEOGRAPHY": "NI"})
        response = self.client.post('/template/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99', content_type='application/json',
                                    data=json.dumps(data))

        # Then we receive a Unauthorized response
        self.assertStatus(response, 401)

    def test_create_invalid_comms_template(self):
        # Given a classification type exists
        self._create_classification_type("GEOGRAPHY")

        # When an invalid comms template is uploaded
        data = dict(label="test data")
        response = self.client.post('/template/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99', content_type='application/json',
                                    data=json.dumps(data), headers=self.get_auth_headers())

        # Then we receive a Bad Request with a validation message
        self.assertStatus(response, 400)
        self.assertEquals(response.json, {"error": "'id' is a required property"})

    def test_create_comms_template_with_empty_classification(self):
        # Given a classification type exists
        self._create_classification_type("GEOGRAPHY")

        # When an invalid comms template is uploaded
        data = dict(id="cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99", label="test data", type="EMAIL", uri="test-uri.com",
                    classification=None)
        response = self.client.post('/template/cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99', content_type='application/json',
                                    data=json.dumps(data), headers=self.get_auth_headers())

        # Then we receive a Bad Request
        self.assertStatus(response, 400)

    def test_get_template(self):
        # Given there is a template in the database
        self._create_classification_type("GEOGRAPHY")
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef89"
        data = dict(id=template_id, label="test data", type="EMAIL", uri="test-uri.com",
                    classification={"GEOGRAPHY": "NI"})
        self._create_template(template_id, data)

        # When the template is searched by id
        response = self.client.get(f'/template/{template_id}')

        # Then the correct data is received
        self.assertStatus(response, 200)
        expected_response_json = dict(id=template_id, label="test data", type="EMAIL", uri="test-uri.com",
                                      classification={"GEOGRAPHY": "NI"}, params=None)
        self.assertEquals(response.json, expected_response_json)

    def test_get_non_existent_template(self):
        # Given a template does not exist in the database
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef79"

        # When the template is searched by id
        response = self.client.get(f'/template/{template_id}')

        # Then it is Not Found
        self.assertStatus(response, 404)

    def test_get_only_matching_templates_by_classifier(self):
        # Given there are multiple templates in the database
        self._create_classification_type("GEOGRAPHY")
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef89"
        classifiers = {"GEOGRAPHY": "NI"}
        data = dict(id=template_id, label="test data", type="EMAIL", uri="test-uri.com",
                    classification=classifiers)
        self._create_template(template_id, data)

        template_id_2 = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99"
        classifiers_2 = {"GEOGRAPHY": "ENGLAND"}
        data_2 = dict(id=template_id_2, label="test data", type="EMAIL", uri="test-uri.com",
                      classification=classifiers_2)
        self._create_template(template_id_2, data_2)

        # When i attempt to get templates by matching classifier
        response = self.client.get("/template?GEOGRAPHY=NI")

        # Then i a list of matching templates
        return_object = data.copy()
        return_object["params"] = None

        self.assertStatus(response, 200)
        self.assertEquals(response.json, [return_object])

    def test_get_non_existent_template_by_classifier(self):
        # Given no template is in the database

        # When we attempt to get the template by it's classifiers
        response = self.client.get("/template?GEOGRAPHY=NI")

        # Then it is Not Found
        self.assertStatus(response, 404)
        self.assertEquals(response.json, None)

    def test_get_multiple_templates_by_classifier(self):
        # Given there are multiple matching templates in the database
        self._create_classification_type("GEOGRAPHY")
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef89"
        classifiers = {"GEOGRAPHY": "NI"}
        data = dict(id=template_id, label="test data", type="EMAIL", uri="test-uri.com", classification=classifiers)
        self._create_template(template_id, data)

        template_id2 = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef90"
        data2 = dict(id=template_id2, label="test data", type="EMAIL", uri="test-uri.com", classification=classifiers)
        self._create_template(template_id2, data2)

        # When i attempt to get templates by matching classifier
        response = self.client.get("/template?GEOGRAPHY=NI")

        # Then i receive a 200 response and a list of matching templates
        return_object = data.copy()
        return_object["params"] = None
        return_object1 = data2.copy()
        return_object1["params"] = None

        # Then we get the correct matching data
        self.assertStatus(response, 200)
        self.assertEquals(response.json, [return_object, return_object1])

    def test_update_template(self):
        # Given there is a template in the database
        self._create_classification_type("GEOGRAPHY")
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef89"
        data = dict(id=template_id, label="test data", type="EMAIL", uri="test-uri.com",
                    classification={"GEOGRAPHY": "NI"})
        self._create_template(template_id, data)

        # When i update the template
        new_data = data.copy()
        new_data["label"] = "new label"

        response = self.client.put(f'/template/{template_id}', content_type='application/json',
                                   data=json.dumps(new_data), headers=self.get_auth_headers())

        # Then the template is correctly updated
        self.assertStatus(response, 200)

        expected_template_object = new_data.copy()
        expected_template_object["params"] = None

        template = self.client.get(f'/template/{template_id}', content_type='application/json')
        self.assertEquals(expected_template_object, template.json)

    def test_update_template_without_basic_auth(self):
        # Given there is a template in the database
        self._create_classification_type("GEOGRAPHY")

        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef89"
        data = dict(id=template_id, label="test data", type="EMAIL", uri="test-uri.com",
                    classification={"GEOGRAPHY": "NI"})
        self._create_template(template_id, data)

        # When i update the template without basic auth
        new_data = data.copy()
        new_data["label"] = "new label"

        response = self.client.put("/template/{}".format(template_id), content_type='application/json',
                                   data=json.dumps(new_data))

        # Then it is Unauthorized
        self.assertStatus(response, 401)

    def test_update_non_existent_template_creates_new(self):
        # Given the template existS in the database
        self._create_classification_type("GEOGRAPHY")

        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef89"
        data = dict(id=template_id, label="test data", type="EMAIL", uri="test-uri.com",
                    classification={"GEOGRAPHY": "NI"})

        # When i update the template
        response = self.client.put(f'/template/{template_id}', content_type='application/json',
                                   data=json.dumps(data), headers=self.get_auth_headers())

        # Then the template is correctly updated
        self.assertStatus(response, 201)
        expected_template_object = data.copy()
        expected_template_object["params"] = None

        template = self.client.get(f'/template/{template_id}', content_type='application/json')
        self.assertEquals(expected_template_object, template.json)

    def test_delete_template(self):
        # Given there is a template in the database
        self._create_classification_type("GEOGRAPHY")

        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef89"
        data = dict(id=template_id, label="test data", type="EMAIL", uri="test-uri.com",
                    classification={"GEOGRAPHY": "NI"})
        self._create_template(template_id, data)

        # When the template is deleted by id
        response = self.client.delete(f'/template/{template_id}', headers=self.get_auth_headers())

        # Then it is deleted
        self.assertStatus(response, 200)

    def test_delete_template_without_basic_auth(self):
        # Given there is a template in the database
        self._create_classification_type("GEOGRAPHY")

        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef89"
        data = dict(id=template_id, label="test data", type="EMAIL", uri="test-uri.com",
                    classification={"GEOGRAPHY": "NI"})
        self._create_template(template_id, data)

        # When the template is deleted by id
        response = self.client.delete('/template/{}'.format(template_id))

        # Then it is Unauthorized
        self.assertStatus(response, 401)

    def test_delete_non_existent_template(self):
        # Given the template doesn't exist in the database
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef89"

        # When the template is deleted by id
        response = self.client.delete(f'/template/{template_id}', headers=self.get_auth_headers())

        # Then we receive Not Found
        self.assertStatus(response, 404)
