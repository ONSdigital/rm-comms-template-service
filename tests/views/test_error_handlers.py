from unittest import mock

from application.utils.exceptions import DatabaseError
from tests.test_client import TestClient


class TestExceptionHandlers(TestClient):

    @mock.patch('application.views.classification_type_view.classification_type_controller')
    def test_handle_exception(self, mock_classification_type_controller):
        # Given an unhandled exception
        mock_classification_type_controller.delete_classification_type.side_effect = Exception

        # When we delete a classification type
        response = self.client.delete('/classificationtypes/LEGAL_BASIS', headers=self.get_auth_headers())

        # we get an error response
        self.assertStatus(response, 500)
        self.assertEqual(response.json, {'error': "Internal Server error"})

    @mock.patch('application.views.classification_type_view.classification_type_controller')
    def test_handle_database_exception(self, mock_classification_type_controller):
        # Given the database throws an exception
        mock_classification_type_controller.delete_classification_type.side_effect = DatabaseError(
            error="Database Exception", status_code=500)

        # When we delete a classification type
        response = self.client.delete('/classificationtypes/LEGAL_BASIS', headers=self.get_auth_headers())

        # we get an appropriate error response
        self.assertStatus(response, 500)
        self.assertEqual(response.json, {'error': "Database Exception"})
