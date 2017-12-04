from application.controllers.classification_type_controller import ClassificationTypeController
from flask import Blueprint, make_response, jsonify

classification_type_view = Blueprint('classification_type_view', __name__)


@classification_type_view.route('/classificationtype', methods=['GET'])
def get_classification_types():
    classification_types = ClassificationTypeController.get_classification_types()
    return make_response(jsonify(classification_types), 200)


@classification_type_view.route('/classificationtype/<classification_type>', methods=['POST'])
def upload_classification_type(classification_type):
    msg = ClassificationTypeController.upload_classification_type(classification_type)
    return make_response(jsonify(msg), 201)


