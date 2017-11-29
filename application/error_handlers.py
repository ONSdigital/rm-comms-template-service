import flask
from flask import jsonify
from requests import HTTPError


blueprint = flask.Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(Exception)
def exception_error(error):
    response = jsonify({'errors': error if type(error) is list else [error]})
    response.status_code = 500
    return response


@blueprint.app_errorhandler(HTTPError)
def http_error(error):
    detail = error.response.json().get('detail', "No further detail.")
    response = jsonify({'errors': [str(error), detail]})
    response.status_code = 500
    return response