from unittest import mock
from sqlalchemy.exc import SQLAlchemyError
from application.controllers import classification_type_controller
from application.utils.exceptions import InvalidClassificationType, DatabaseError
from tests.test_client import TestClient


class TestClassificationTypeController(TestClient):

    def test_upload_existing_classification_type_raises_invalid_classification_type_exception(self):
        # Given the object already exists in the database
        classification_type = "GEOGRAPHY"
        classification_type_controller.create_classification_type(classification_type)

        # When a template with the same id is uploaded
        with self.assertRaises(InvalidClassificationType):
            classification_type_controller.create_classification_type(classification_type)

    def test_get_non_existing_classification_type(self):
        # Given the classification type is not in the database
        classification_type = "GEOGRAPHY"

        # When we try to get the classification type
        classification = classification_type_controller.get_classification_type(classification_type)

        # Then we receive none
        self.assertEqual(classification, None)

    def test_get_non_existing_classification_types(self):
        # Given there are no classification types in the database
        # When we try to get all the classification types
        classification_types = classification_type_controller.get_classification_types()

        # Then we receive none
        self.assertEqual(classification_types, None)

    @mock.patch('application.controllers.classification_type_controller.db')
    def test_get_classification_types(self, mock_db):
        # Given there is an error connecting with the database
        mock_db.session.query = mock.MagicMock(side_effect=SQLAlchemyError)

        # When we try to get all the classification types
        # Then it raises a database error
        with self.assertRaises(DatabaseError):
            classification_type_controller.get_classification_types()

    @mock.patch('application.controllers.classification_type_controller.db')
    def test_get_classification_type(self, mock_db):
        # Given there is an error connecting with the database
        mock_db.session.query = mock.MagicMock(side_effect=SQLAlchemyError)

        # When we try to get all the classification types
        # Then it raises a database error
        with self.assertRaises(DatabaseError):
            classification_type_controller.get_classification_type('LEGAL BASIS')

    @mock.patch('application.controllers.classification_type_controller.db')
    def test_delete_classification_type(self, mock_db):
        # Given there is an error connecting with the database
        mock_db.session.query = mock.MagicMock(side_effect=SQLAlchemyError)

        # When we try to delete a classification type
        # Then it raises a database error
        with self.assertRaises(DatabaseError):
            classification_type_controller.delete_classification_type('LEGAL BASIS')

    @mock.patch('application.controllers.classification_type_controller._get_classification', return_value=None)
    @mock.patch('application.controllers.classification_type_controller.db')
    def test_create_classification_type(self, mock_db, mock_get_classification_type):
        # Given there is an error connecting with the database
        mock_db.session.add = mock.MagicMock(side_effect=SQLAlchemyError)

        # When we try to create a classification type
        # Then it raises a database error
        with self.assertRaises(DatabaseError):
            classification_type_controller.create_classification_type('LEGAL BASIS')
