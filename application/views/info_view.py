from flask import Blueprint, make_response, jsonify

from application.controllers import info_controller

info_view = Blueprint('info_view', __name__)


@info_view.route('/info', methods=['GET'])
@log_route
def get_info():
    response = info_controller.get_info()
    return make_response(jsonify(response), 200)