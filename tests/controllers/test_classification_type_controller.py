from application.controllers import classification_type_controller
from application.utils.exceptions import InvalidClassificationType
from tests.test_client import TestClient


class TestClassificationTypeController(TestClient):

    def test_upload_existing_classification_type_raises_invalid_classification_type_exception(self):
        # Given the object already exists in the database
        classification_type = "GEOGRAPHY"
        classification_type_controller.upload_classification_type(classification_type)

        # When a template with the same id is uploaded
        with self.assertRaises(InvalidClassificationType):
            classification_type_controller.upload_classification_type(classification_type)

    def test_get_non_existing_classification_type(self):
        # Given the classification type is not in the database
        classification_type = "GEOGRAPHY"

        # When we try to get the classification type
        classification = classification_type_controller.get_classification_type(classification_type)

        # Then we receive none
        self.assertEquals(classification, None)

    def test_get_non_existing_classification_types(self):
        # Given there are no classification types in the database
        # When we try to get all the classification types
        classification_types = classification_type_controller.get_classification_types()

        # Then we receive none
        self.assertEquals(classification_types, None)
