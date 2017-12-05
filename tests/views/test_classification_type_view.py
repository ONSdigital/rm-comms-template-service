from tests.test_client import TestClient
from application.controllers.template_controller import UPLOAD_SUCCESSFUL


class TestClassificationTypeView(TestClient):

    def __upload_classification_type(self, classification_type):
        response = self.client.post('/classificationtype/{}'.format(classification_type))
        self.assertStatus(response, 201)
        self.assertEquals(response.json, UPLOAD_SUCCESSFUL)

    def test_upload_classification_type(self):
        # when we upload a new classification type
        classification_type = "LEGAL_BASIS"
        response = self.client.post('/classificationtype/{}'.format(classification_type))

        # Then the classification type is successfully uploaded to the database
        self.assertStatus(response, 201)
        self.assertEquals(response.json, UPLOAD_SUCCESSFUL)

    def test_upload_existing_classification_type(self):
        # Given a ClassificationType exists in the database
        classification_type = "LEGAL_BASIS"
        self.__upload_classification_type(classification_type)

        # When the same classification type is uploaded
        response = self.client.post('/classificationtype/{}'.format(classification_type))

        # Then the service returns a 400 response
        self.assertStatus(response, 400)

    def test_get_classification_types(self):
        # Given there are existing classification types in the database
        self.__upload_classification_type("LEGAL_BASIS")
        self.__upload_classification_type("GEOGRAPHY")

        # When we get all the classification types
        response = self.client.get("/classificationtype")

        # Then the service returns the classification types
        self.assertStatus(response, 200)
        expected_response = [{"name": "LEGAL_BASIS"}, {"name": "GEOGRAPHY"}]
        self.assertEquals(response.json, expected_response)

    def test_get_classification_types_if_none_in_dbd(self):
        # Given there are no classification types in the database
        # When we get all the classification types
        response = self.client.get("/classificationtype")

        self.assertStatus(response, 404)

    def test_get_classification_type(self):
        # Given there is an existing classification type in the database
        classification_type = "LEGAL_BASIS"
        self.__upload_classification_type(classification_type)

        # When we get the classification type
        response = self.client.get("/classificationtype/{}".format(classification_type))

        # Then the service returns the classfication type
        expected_response = {"name": classification_type}
        self.assertStatus(response, 200)
        self.assertEquals(response.json, expected_response)

    def test_get_non_existent_classification_type(self):
        # Given the classifciation type doesn't exist
        classification_type = "LEGAL_BASIS"

        # When we try to get the classification type
        response = self.client.get("/classificationtype/{}".format(classification_type))

        # Then the server returns a 404 response
        self.assertStatus(response, 404)
