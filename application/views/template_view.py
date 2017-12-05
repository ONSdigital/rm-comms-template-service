from flask import Blueprint, make_response, request, jsonify
from application.controllers.template_controller import TemplateController

template_view = Blueprint('template_view', __name__)


@template_view.route('/template/<template_id>', methods=['POST', 'PUT'])
def upload_template(template_id):
    template = request.get_json()
    request_method = request.method

    msg, is_created = TemplateController.upload_comms_template(template_id, template, request_method)
    http_code = 201 if is_created else 200

    return make_response(msg, http_code)


@template_view.route('/template/<template_id>', methods=['GET'])
def get_template_by_id(template_id):
    template = TemplateController.get_comms_template_by_id(template_id)

    http_code = 200 if template else 404

    return make_response(jsonify(template), http_code)
