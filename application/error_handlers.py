from flask import Blueprint, jsonify
from application.utils.exceptions import InvalidTemplateException, DatabaseError

from structlog import get_logger


logger = get_logger()

blueprint = Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(InvalidTemplateException)
def invalid_template_error(exception):
    logger.exception(exception.error)
    response = jsonify({'error': exception.error})
    response.status_code = exception.status_code
    return response


@blueprint.app_errorhandler(DatabaseError)
def database_error(exception):
    logger.exception(exception.error)
    response = jsonify({'error': exception.error})
    response.status_code = exception.status_code
    return response


@blueprint.app_errorhandler(Exception)
def exception_error(exception):
    logger.exception("Unhandled Exception")
    response = jsonify({'error': "Internal Server error"})
    response.status_code = 500
    return response
