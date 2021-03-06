import json

from tests.test_client import TestClient
from application.controllers.template_controller import _get_template_by_id


class TestSessions(TestClient):
    """ This test class is to check that the inbuilt flask and flask-sqlalchemy session management is working
    I.e does it rollback sessions on exception, is it committed """

    def _create_classification_type(self, classification_type):
        response = self.client.post('/classificationtypes/{}'.format(classification_type),
                                    headers=self.get_auth_headers())
        self.assertStatus(response, 201)

    def test_rollback_on_exception(self):
        # Given there are classification types
        self._create_classification_type("GEOGRAPHY")

        # When an invalid comms template is uploaded
        data = dict(label="test data")
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99"
        response = self.client.post(f'/templates', content_type='application/json',  # noqa: F541
                                    data=json.dumps(data), headers=self.get_auth_headers())

        self.assertStatus(response, 400)
        self.assertEqual(response.json, {"error": "'id' is a required property"})

        # Then it is not uploaded to the database
        template = _get_template_by_id(template_id)

        self.assertEqual(template, None)

    def test_commit_on_successful_request(self):
        # Given there are classification types
        self._create_classification_type("GEOGRAPHY")

        # When a valid comms template is uploaded
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99"
        data = dict(id=template_id, label="test data", type="EMAIL", uri="test-uri.com",
                    classification={"GEOGRAPHY": "NI"})
        response = self.client.post(f'/templates', content_type='application/json',  # noqa: F541
                                    data=json.dumps(data), headers=self.get_auth_headers())

        self.assertStatus(response, 201)

        # Then it is persisted to the database
        template = _get_template_by_id(template_id)

        expected_data = data.copy()
        expected_data["params"] = None

        self.assertEqual(template.to_dict(), expected_data)
