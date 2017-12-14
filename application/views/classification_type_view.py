from flask import Blueprint, make_response, jsonify, Response
from application.utils.basic_auth import auth

from application.controllers import classification_type_controller

classification_type_view = Blueprint('classification_type_view', __name__)


@classification_type_view.route('/classificationtype', methods=['GET'])
def get_classification_types():
    classification_types = classification_type_controller.get_classification_types()
    http_code = 200 if classification_types else 404
    return make_response(jsonify(classification_types), http_code)


@classification_type_view.route('/classificationtype/<classification_type>', methods=['GET'])
def get_classification_type(classification_type):
    classification = classification_type_controller.get_classification_type(classification_type)
    http_code = 200 if classification else 404
    return make_response(jsonify(classification), http_code)


@classification_type_view.route('/classificationtype/<classification_type>', methods=['POST'])
@auth.login_required
def upload_classification_type(classification_type):
    classification_type_controller.create_classification_type(classification_type)
    return Response(status=201)


@classification_type_view.route('/classificationtype/<classification_type>', methods=['DELETE'])
def delete_classification_type(classification_type):
    is_deleted = classification_type_controller.delete_classification_type(classification_type)
    http_code = 200 if is_deleted else 404
    return Response(status=http_code)
