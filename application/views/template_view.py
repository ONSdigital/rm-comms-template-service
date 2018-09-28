from flask import Blueprint, make_response, request, jsonify, Response
from application.controllers import template_controller
from application.utils.basic_auth import auth

template_view = Blueprint('template_view', __name__)


@template_view.route('/templates', methods=['POST'])
@auth.login_required
def create_template():
    template_controller.create_comms_template(template=request.get_json())
    return Response(status=201)


@template_view.route('/templates/<template_id>', methods=['PUT'])
@auth.login_required
def update_template(template_id):
    is_created = template_controller.update_comms_template(template_id, template=request.get_json())
    http_code = 201 if is_created else 200
    return Response(status=http_code)


@template_view.route('/templates/<template_id>', methods=['GET'])
@auth.login_required
def get_template_by_id(template_id):
    template = template_controller.get_comms_template_by_id(template_id)
    http_code = 200 if template else 404
    return make_response(jsonify(template), http_code)


@template_view.route('/templates', methods=['GET'])
@auth.login_required
def get_template_by_classifiers():
    template = template_controller.get_comms_template_by_classifiers(classifiers=request.args)
    http_code = 200 if template else 404
    return make_response(jsonify(template), http_code)


@template_view.route('/templates/<template_id>', methods=['DELETE'])
@auth.login_required
def delete_template(template_id):
    is_deleted = template_controller.delete_comms_template(template_id)
    http_code = 200 if is_deleted else 404
    return Response(status=http_code)
