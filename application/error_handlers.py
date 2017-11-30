from flask import Blueprint
from flask import jsonify

import logging
from structlog import wrap_logger


logger = wrap_logger(logging.getLogger(__name__))

blueprint = Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(Exception)
def exception_error(error):
    logger.exception("Unhandled Exception: ", error)
    response = jsonify({'error': "Internal Server error"})
    response.status_code = 500
    return response
