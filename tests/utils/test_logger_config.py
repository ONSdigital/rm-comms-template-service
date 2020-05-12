import pytest
from application.utils.logging import configure_structlogger
from run import create_app

config_path = "config.Config"
app = create_app(config_path)


class TestLoggerConfig():
    """ Logging unit tests"""

    @pytest.fixture(scope="module")
    def test_logger_config(self):

        structlogger = configure_structlogger(app.config)

        # Check structlog processors contains "severity" for GC Logging
        assert 'add_severity_level' in structlogger.processors
