from application.controllers import template_controller
from application.utils.exceptions import InvalidTemplateException
from tests.test_client import TestClient


class TestTemplateController(TestClient):

    def test_upload_existing_template_raises_invalid_template_exception(self):
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91"
        template_object = dict(id="cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91", label="test data", type="EMAIL",
                               uri="test-uri.com", classification={"GEOGRAPHY": "NI"})

        request_method = "POST"
        # Given the object already exists in the database
        is_created = template_controller.upload_comms_template(template_id, template_object, request_method)
        self.assertEquals(is_created, True)

        # When a template with the same id is uploaded
        with self.assertRaises(InvalidTemplateException):
            template_controller.upload_comms_template(template_id, template_object, request_method)

    def test_update_non_existent_template_creates_new_template(self):
        # given the template doesn't exist in the database
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91"
        template_object = dict(id="cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91", label="test data", type="EMAIL",
                               uri="test-uri.com", classification={"GEOGRAPHY": "NI"})

        request_method = "PUT"

        # When the template is updated
        is_created = template_controller.upload_comms_template(template_id, template_object, request_method)

        # We receive an upload successful message with a boolean is_created
        self.assertEquals(is_created, True)

    def test_get_non_existing_template(self):
        template_id = "db0711c3-0ac8-41d3-ae0e-567e5ea1ef91"

        template = template_controller.get_comms_template_by_id(template_id)

        self.assertEquals(template, None)
