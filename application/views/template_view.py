from flask import Blueprint, make_response, request, jsonify, Response
from application.controllers import template_controller
from application.utils.basic_auth import auth

template_view = Blueprint('template_view', __name__)


@template_view.route('/template/<template_id>', methods=['POST'])
@auth.login_required
def upload_template(template_id):
    template_controller.create_comms_template(template_id, template=request.get_json())
    return Response(status=201)


@template_view.route('/template/<template_id>', methods=['PUT'])
@auth.login_required
def update_template(template_id):
    is_created = template_controller.update_comms_template(template_id, template=request.get_json())
    http_code = 201 if is_created else 200
    return Response(status=http_code)


@template_view.route('/template/<template_id>', methods=['GET'])
def get_template_by_id(template_id):
    template = template_controller.get_comms_template_by_id(template_id)
    http_code = 200 if template else 404
    return make_response(jsonify(template), http_code)


@template_view.route('/template', methods=['GET'])
def get_templates_by_classifiers():
    templates = template_controller.get_comms_templates_by_classifiers(classifiers=request.args)
    http_code = 200 if templates else 404
    return make_response(jsonify(templates), http_code)


@template_view.route('/template/<template_id>', methods=['DELETE'])
@auth.login_required
def delete_template(template_id):
    is_deleted = template_controller.delete_comms_template(template_id)
    http_code = 200 if is_deleted else 404
    return Response(status=http_code)
