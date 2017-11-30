from flask import Blueprint, jsonify
from application.utils.exceptions import InvalidTemplateException, DatabaseError

from structlog import get_logger


logger = get_logger()

blueprint = Blueprint('error_handlers', __name__)

INVALID_TEMPLATE_MESSAGE = "Attempted to upload invalid template"


@blueprint.app_errorhandler(InvalidTemplateException)
def invalid_template_error(exception):
    logger.exception(INVALID_TEMPLATE_MESSAGE)
    response = jsonify({'error': INVALID_TEMPLATE_MESSAGE})
    response.status_code = exception.status_code
    return response


@blueprint.app_errorhandler(DatabaseError)
def database_error(exception):
    logger.exception("Error whilst interacting with database")
    response = jsonify({'error': "There was an error uploading the template"})
    response.status_code = exception.status_code or 500
    return response


@blueprint.app_errorhandler(Exception)
def exception_error(exception):
    logger.exception("Unhandled Exception")
    response = jsonify({'error': "Internal Server error"})
    response.status_code = 500
    return response
