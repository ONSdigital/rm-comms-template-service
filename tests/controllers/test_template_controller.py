from application.controllers import template_controller
from application.utils.exceptions import InvalidTemplateException
from tests.test_client import TestClient


class TestTemplateController(TestClient):

    def test_upload_existing_template_raises_invalid_template_exception(self):
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91"
        template_object = dict(id="cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91", label="test data", type="EMAIL",
                               uri="test-uri.com", classification={"GEOGRAPHY": "NI"})

        # Given the object already exists in the database
        template_controller.upload_comms_template(template_id, template_object)

        # When an object with the same id is uploaded
        with self.assertRaises(InvalidTemplateException):
            template_controller.upload_comms_template(template_id, template_object)

    def test_get_non_existing_template(self):
        template_id = "db0711c3-0ac8-41d3-ae0e-567e5ea1ef91"

        template = template_controller.get_comms_template_by_id(template_id)

        self.assertEquals(template, None)

    def test_delete_template(self):
        # Given the template exists in the database
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91"
        template_object = dict(id="cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91", label="test data", type="EMAIL",
                               uri="test-uri.com", classification={"GEOGRAPHY": "NI"})

        template_controller.upload_comms_template(template_id, template_object)

        # When the template is deleted
        number_of_deleted_templates = template_controller.delete_comms_template(template_id)

        self.assertEquals(number_of_deleted_templates, 1)
