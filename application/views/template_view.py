from flask import Blueprint, make_response, request, jsonify, Response
from application.controllers import template_controller

template_view = Blueprint('template_view', __name__)


@template_view.route('/template/<template_id>', methods=['POST'])
def upload_template(template_id):
    template_controller.create_comms_template(template_id, template=request.get_json())
    return Response(status=201)


@template_view.route('/template/<template_id>', methods=['PUT'])
def update_template(template_id):
    is_created = template_controller.update_comms_template(template_id, template=request.get_json())
    http_code = 201 if is_created else 200
    return Response(status=http_code)


@template_view.route('/template/<template_id>', methods=['GET'])
def get_template_by_id(template_id):
    template = template_controller.get_comms_template_by_id(template_id)
    http_code = 200 if template else 404
    return make_response(jsonify(template), http_code)
