from flask import Blueprint, make_response, request, jsonify
from application.controllers.template_controller import TemplateController

template_view = Blueprint('template_view', __name__)


@template_view.route('/template/<template_id>', methods=['POST'])
def upload_template(template_id):
    template = request.get_json()
    msg = TemplateController.upload_comms_template(template_id, template)
    return make_response(msg, 201)


@template_view.route('/template/<template_id>', methods=['GET'])
def get_template_by_id(template_id):
    template = TemplateController.get_comms_template_by_id(template_id)

    http_code = 200 if template else 404

    return make_response(jsonify(template), http_code)
