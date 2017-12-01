from flask import Blueprint
from flask import jsonify

from structlog import get_logger


logger = get_logger()

blueprint = Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(Exception)
def exception_error(error):
    logger.exception("Unhandled Exception: ", error)
    response = jsonify({'error': "Internal Server error"})
    response.status_code = 500
    return response
