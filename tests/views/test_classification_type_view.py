from tests.test_client import TestClient


class TestClassificationTypeView(TestClient):

    def _create_classification_type(self, classification_type):
        response = self.client.post(f'/classificationtype/{classification_type}', headers=self.get_auth_headers())
        self.assertStatus(response, 201)

    def test_upload_classification_type(self):
        # when we upload a new classification type
        classification_type = "LEGAL_BASIS"
        response = self.client.post(f'/classificationtype/{classification_type}', headers=self.get_auth_headers())

        # Then the classification type is successfully uploaded to the database
        self.assertStatus(response, 201)

    def test_create_classification_type_without_basic_auth(self):
        # when we upload a new classification type
        classification_type = "LEGAL_BASIS"
        response = self.client.post(f'/classificationtype/{classification_type}')

        # It is Unauthorized
        self.assertStatus(response, 401)

    def test_upload_existing_classification_type(self):
        # Given a ClassificationType exists in the database
        classification_type = "LEGAL_BASIS"
        self._create_classification_type(classification_type)

        # When the same classification type is uploaded
        response = self.client.post(f'/classificationtype/{classification_type}', headers=self.get_auth_headers())

        # Then it returns Conflict
        self.assertStatus(response, 409)

    def test_get_classification_types(self):
        # Given there are existing classification types in the database
        self._create_classification_type("LEGAL_BASIS")
        self._create_classification_type("GEOGRAPHY")

        # When we get all the classification types
        response = self.client.get("/classificationtype")

        # Then the service returns the classification types
        self.assertStatus(response, 200)
        self.assertEquals(response.json, ["LEGAL_BASIS", "GEOGRAPHY"])

    def test_get_classification_types_if_none_in_db(self):
        # Given there are no classification types in the database
        # When we get all the classification types
        response = self.client.get("/classificationtype")

        # Then no classification types are found
        self.assertStatus(response, 404)

    def test_get_classification_type(self):
        # Given there is an existing classification type in the database
        classification_type = "LEGAL_BASIS"
        self._create_classification_type(classification_type)

        # When we get the classification type
        response = self.client.get(f'/classificationtype/{classification_type}')

        # Then the service returns the classfication type
        self.assertStatus(response, 200)
        self.assertEquals(response.json, classification_type)

    def test_get_non_existent_classification_type(self):
        # Given the classification type doesn't exist
        classification_type = "LEGAL_BASIS"

        # When we try to get the classification type
        response = self.client.get(f'/classificationtype/{classification_type}')

        # Then the classification type is Not Found
        self.assertStatus(response, 404)

    def test_delete_classification_type(self):
        # Given there is an existing classification type in the database
        classification_type = "LEGAL_BASIS"
        self._create_classification_type(classification_type)

        # When we delete the classification type
        response = self.client.delete(f'/classificationtype/{classification_type}', headers=self.get_auth_headers())

        # The classification is deleted
        self.assertStatus(response, 200)

    def test_delete_classification_type_without_basic_auth(self):
        # Given there is an existing classification type in the database
        classification_type = "LEGAL_BASIS"
        self._create_classification_type(classification_type)

        # When we delete the classification type
        response = self.client.delete(f'/classificationtype/{classification_type}')

        # It is Unauthorized
        self.assertStatus(response, 401)

    def test_delete_non_existent_classification_type(self):
        # Given the classification type doesn't exist
        classification_type = "LEGAL_BASIS"

        # When we delete the classification type
        response = self.client.delete(f'/classificationtype/{classification_type}', headers=self.get_auth_headers())

        # It is Not Found
        self.assertStatus(response, 404)
