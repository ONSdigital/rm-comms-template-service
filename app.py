import logging
import structlog

from retrying import RetryError
from run import create_app, configure_structlogger, initialise_db

# This is a duplicate of run.py, with minor modifications to support gunicorn execution.

logger = structlog.wrap_logger(logging.getLogger(__name__))

config_path = "config.Config"

app = create_app(config_path)

configure_structlogger(app.config)

try:
    initialise_db(app)
except RetryError:
    logger.exception('Failed to initialise database')
    exit(1)
