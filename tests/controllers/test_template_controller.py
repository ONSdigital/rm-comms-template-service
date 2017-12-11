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

    def test_get_template_by_classifiers(self):
        # given the template exists in the database
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91"
        classifiers = {"GEOGRAPHY": "NI",
                       "INDUSTRY": "construction"}
        template_object = dict(id="cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91", label="test data", type="EMAIL",
                               uri="test-uri.com", classification=classifiers)

        template_controller.upload_comms_template(template_id, template_object)

        # When we search for a template by classifiers we retrieve the matching template
        template_list = template_controller.get_comms_templates_by_classifiers(classifiers)

        expected_response = template_object.copy()
        expected_response["params"] = None

        self.assertEquals(template_list, [expected_response])

    def test_get_non_existent_template_by_classifier(self):
        # given the template doesnt exist in the database
        classifiers = {"GEOGRAPHY": "NI"}

        # When we search for a template by classifiers we retrieve the matching template
        template_list = template_controller.get_comms_templates_by_classifiers(classifiers)

        self.assertEquals(template_list, None)
