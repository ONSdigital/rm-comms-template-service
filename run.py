from flask_cors import CORS
from ras_common_utils.ras_config import ras_config
from ras_common_utils.ras_config.flask_extended import Flask
from ras_common_utils.ras_database.ras_database import RasDatabase
from ras_common_utils.ras_logger.ras_logger import configure_logger


def create_app(config):
    # create and configure the Flask app
    app = Flask(__name__)
    app.config.from_ras_config(config)

    # register view blueprints

    CORS(app)
    return app


def initialise_db(app):
    # Initialise the database with the specified SQLAlchemy model
    comms_template_database = RasDatabase.make(model_paths=['application.models.models'])
    db = comms_template_database('rm-comms-template-db', app.config)
    app.db = db


if __name__ == '__main__':
    config_path = 'config/config.yml'

    config = ras_config.from_yaml_file(config_path)
    configure_logger(config.service)

    app = create_app(config)

    initialise_db(app)

    scheme, host, port = app.config['SCHEME'], app.config['HOST'], int(app.config['PORT'])

    app.run(debug=app.config['DEBUG'], host=host, port=port)
