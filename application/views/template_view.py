from flask import Blueprint, make_response, request, jsonify, Response
from application.controllers import template_controller

template_view = Blueprint('template_view', __name__)


@template_view.route('/template/<template_id>', methods=['POST'])
def upload_template(template_id):
    template = request.get_json()
    template_controller.upload_comms_template(template_id, template)
    return Response(status=201)


@template_view.route('/template/<template_id>', methods=['GET'])
def get_template_by_id(template_id):
    template = template_controller.get_comms_template_by_id(template_id)

    http_code = 200 if template else 404

    return make_response(jsonify(template), http_code)
