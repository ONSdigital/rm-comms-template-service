from flask import Blueprint, jsonify
from application.utils.exceptions import InvalidTemplateException, DatabaseError

from structlog import get_logger


logger = get_logger()

blueprint = Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(InvalidTemplateException)
def invalid_template_error(error):
    logger.info("Attempted to upload invalid template", error)
    response = jsonify({'error': "Attempted to upload invalid template"})
    response.status_code = error.status_code
    return response


@blueprint.app_errorhandler(DatabaseError)
def database_error(error):
    logger.info("Error whilst interacting with database", error)
    response = jsonify({'error': "There was an error uploading the template"})
    response.status_code = error.status_code or 500
    return response


@blueprint.app_errorhandler(Exception)
def exception_error(error):
    logger.exception("Unhandled Exception: ", error)
    response = jsonify({'error': "Internal Server error"})
    response.status_code = 500
    return response
