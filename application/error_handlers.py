from flask import Blueprint
from flask import jsonify
<<<<<<< HEAD
=======
from requests import HTTPError
from application.utils.exceptions import InvalidTemplateObject, RasError
>>>>>>> Adds Post Comms Template endpoint

from structlog import get_logger


logger = get_logger()

blueprint = Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(Exception)
def exception_error(error):
    logger.exception("Unhandled Exception: ", error)
    response = jsonify({'error': "Internal Server error"})
    response.status_code = 500
    return response


@blueprint.app_errorhandler(InvalidTemplateObject)
def invalid_template_error(error):
    logger.info("Attempted to upload invalid template", error)
    response = jsonify({'error': "Attempted to upload invalid template"})
    response.status_code = error.status_code
    return response
