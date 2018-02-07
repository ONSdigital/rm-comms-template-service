from unittest import mock
from sqlalchemy.exc import SQLAlchemyError

from application.controllers import template_controller
from application.utils.exceptions import InvalidTemplateException, DatabaseError
from tests.test_client import TestClient


class TestTemplateController(TestClient):

    @mock.patch('application.controllers.template_controller.get_classification_types', return_value=["GEOGRAPHY"])
    def test_create_existing_template_raises_invalid_template_exception(self, get_classification_types):
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91"
        template_object = dict(id=template_id, label="test data", type="EMAIL",
                               uri="test-uri.com", classification={"GEOGRAPHY": "NI"})

        # Given the object already exists in the database
        template_controller.create_comms_template(template_id, template=template_object)

        # When a template with the same id is uploaded
        with self.assertRaises(InvalidTemplateException):
            template_controller.create_comms_template(template_id, template=template_object)

    @mock.patch('application.controllers.template_controller.get_classification_types', return_value=["GEOGRAPHY"])
    def test_create_template_with_invalid_classification_type(self, get_classification_types):
        # Given the classification type doesn't exist

        # When a template with the same id is uploaded
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91"
        template_object = dict(id=template_id, label="test data", type="EMAIL",
                               uri="test-uri.com", classification={"LEGAL BASIS": "NI"})

        # Then it throws an invalid exception
        with self.assertRaises(InvalidTemplateException):
            template_controller.create_comms_template(template_id, template=template_object)

    def test_update_non_existent_template_creates_new_template(self):
        # given the template doesn't exist in the database
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91"
        template_object = dict(id=template_id, label="test data", type="EMAIL",
                               uri="test-uri.com", classification={"GEOGRAPHY": "NI"})

        # When the template is updated
        is_created = template_controller.update_comms_template(template_id, template=template_object)

        # We receive an upload successful message with a boolean is_created
        self.assertEquals(is_created, True)

    def test_get_non_existing_template(self):
        # Given the template doesn't exist in the database
        template_id = "db0711c3-0ac8-41d3-ae0e-567e5ea1ef91"

        # When the template is retrieved
        template = template_controller.get_comms_template_by_id(template_id)

        # Then we receive None
        self.assertEquals(template, None)

    @mock.patch('application.controllers.template_controller.get_classification_types',
                return_value=["GEOGRAPHY", "INDUSTRY"])
    def test_get_template_by_classifiers(self, get_classification_types):
        # given the template exists in the database
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91"
        classifiers = {"GEOGRAPHY": "NI",
                       "INDUSTRY": "construction"}
        template_object = dict(id="cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91", label="test data", type="EMAIL",
                               uri="test-uri.com", classification=classifiers)

        template_controller.create_comms_template(template_id, template_object)

        # When we search for a template by classifiers we retrieve the matching template
        template_list = template_controller.get_comms_template_by_classifiers(classifiers=classifiers)

        expected_response = template_object.copy()
        expected_response["params"] = None

        self.assertEquals(template_list, expected_response)

    def test_get_non_existent_template_by_classifier(self):
        # Given the template doesnt exist in the database

        # When we search for a template by classifiers we retrieve the matching template
        template_list = template_controller.get_comms_template_by_classifiers(classifiers={"GEOGRAPHY": "NI"})

        self.assertEquals(template_list, None)

    @mock.patch('application.controllers.template_controller.get_classification_types', return_value=["GEOGRAPHY"])
    def test_delete_template(self, get_classification_types):
        # Given the template exists in the database
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91"
        template_object = dict(id=template_id, label="test data", type="EMAIL",
                               uri="test-uri.com", classification={"GEOGRAPHY": "NI"})

        template_controller.create_comms_template(template_id, template_object)

        # When the template is deleted
        is_deleted = template_controller.delete_comms_template(template_id)

        # We receive a true is deleted response
        self.assertEquals(is_deleted, True)

    @mock.patch('application.controllers.template_controller.db')
    def test_get_template(self, mock_db):
        # Given there is an error connecting with the database
        mock_db.session.query = mock.MagicMock(side_effect=SQLAlchemyError)

        # When we try to get a template
        # Then it raises a database error
        with self.assertRaises(DatabaseError):
            template_controller.get_comms_template_by_id("cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91")

    @mock.patch('application.controllers.template_controller.db')
    def test_delete_template_exception(self, mock_db):
        # Given there is an error connecting with the database
        mock_db.session.query = mock.MagicMock(side_effect=SQLAlchemyError)

        # When we try to delete a template
        # Then it raises a database error
        with self.assertRaises(DatabaseError):
            template_controller.delete_comms_template("cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91")

    @mock.patch('application.controllers.template_controller.get_classification_types', return_value=["GEOGRAPHY"])
    @mock.patch('application.controllers.template_controller._get_template_by_id', return_value=None)
    @mock.patch('application.controllers.template_controller.db')
    def test_create_template(self, mock_db, mock_get_template_by_id, mock_get_classifcation_types):
        # Given there is an error connecting with the database
        mock_db.session.merge = mock.MagicMock(side_effect=SQLAlchemyError)

        # When a template with the same id is uploaded
        template_id = "cb0711c3-0ac8-41d3-ae0e-567e5ea1ef91"
        template_object = dict(id=template_id, label="test data", type="EMAIL",
                               uri="test-uri.com", classification={"GEOGRAPHY": "NI"})

        # Then it raises a database error
        with self.assertRaises(DatabaseError):
            template_controller.create_comms_template(template_id, template=template_object)

    @mock.patch('application.controllers.template_controller.db')
    def test_get_template_by_classifier_throws_exception(self, mock_db):
        # Given there is an error connecting with the database
        mock_db.session.query = mock.MagicMock(side_effect=SQLAlchemyError)

        # When we try to get a template by classifier
        # Then it raises a database error
        with self.assertRaises(DatabaseError):
            template_controller.get_comms_template_by_classifiers(classifiers={"GEOGRAPHY": "NI",
                                                                               "INDUSTRY": "construction",
                                                                               })
