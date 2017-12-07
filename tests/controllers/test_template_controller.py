from application.controllers.template_controller import TemplateController, UPLOAD_SUCCESSFUL
from application.utils.exceptions import InvalidTemplateException
from tests.test_client import TestClient


class TestTemplateController(TestClient):

    def test_upload_existing_template_raises_invalid_template_exception(self):
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91"
        template_object = dict(id="cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91", label="test data", type="EMAIL",
                               uri="test-uri.com", classification={"GEOGRAPHY": "NI"})

        # Given the object already exists in the database
        response = TemplateController.upload_comms_template(template_id, template_object)
        self.assertEquals(response, UPLOAD_SUCCESSFUL)

        # When an object with the same id is uploaded
        with self.assertRaises(InvalidTemplateException):
            TemplateController.upload_comms_template(template_id, template_object)

    def test_get_non_existing_template(self):
        template_id = "db0711c3-0ac8-41d3-ae0e-567e5ea1ef91"

        template = TemplateController.get_comms_template_by_id(template_id)

        self.assertEquals(template, None)
