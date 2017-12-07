import json
from flask import current_app

from tests.test_client import TestClient
from application.controllers.template_controller import get_template_by_id, UPLOAD_SUCCESSFUL


class TestSessions(TestClient):
    """ This test class is to check that the inbuilt flask and flask-sqlalchemy session management is working
    I.e does it rollback sessions on exception, is it committed """

    def test_template_not_commited_on_exception(self):
        # When an invalid comms template is uploaded
        data = dict(label="test data")
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99"
        response = self.client.post('/template/{}'.format(template_id), content_type='application/json',
                                    data=json.dumps(data))
        self.assertStatus(response, 400)
        self.assertEquals(response.json, {"error": "'id' is a required property"})

        # Then it is not uploaded to the database
        session = current_app.db.session()
        template = get_template_by_id(template_id, session)

        self.assertEquals(template, None)

    def test_template_commited_on_successful_post(self):
        # When a valid comms template is uploaded
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef99"
        data = dict(id=template_id, label="test data", type="EMAIL", uri="test-uri.com",
                    classification={"GEOGRAPHY": "NI"})
        response = self.client.post('/template/{}'.format(template_id), content_type='application/json',
                                    data=json.dumps(data))
        self.assertStatus(response, 201)
        self.assertEquals(response.data.decode(), UPLOAD_SUCCESSFUL)

        # Then it is persisted to the database
        session = current_app.db.session()
        template = get_template_by_id(template_id, session)

        expected_data = data.copy()
        expected_data["params"] = None

        self.assertEquals(template.to_dict(), expected_data)
