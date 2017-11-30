import flask
from flask import jsonify
from requests import HTTPError

import logging
from structlog import wrap_logger


logger = wrap_logger(logging.getLogger(__name__))

blueprint = flask.Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(Exception)
def exception_error(error):
    logger.error("Unhandled Exception: ", error)
    response = jsonify({'error': "Internal Server error"})
    response.status_code = 500
    return response


@blueprint.app_errorhandler(HTTPError)
def http_error(error):
    logger.info("Unexpected HTTP error: ", error)
    response = jsonify({'errors': 'Unexpected HTTP error'})
    response.status_code = 500
    return response
