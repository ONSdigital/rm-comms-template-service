from flask_cors import CORS
from flask import Flask
from application.utils.logging import configure_structlogger
from application.models.models import db


def create_app(config_path):
    # create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(config_path)

    from application.models.models import CommunicationTemplate, ClassificationType, CommunicationType # NOQA  # pylint: disable=wrong-import-position

    # Set up database
    with app.app_context():
        db.init_app(app)
        db.create_all()

    app.db = db

    # register view blueprints
    from application.views.info_view import info_view
    from application.views.template_view import template_view
    from application import error_handlers
    app.register_blueprint(info_view)
    app.register_blueprint(template_view)
    app.register_blueprint(error_handlers.blueprint)

    CORS(app)
    return app


if __name__ == '__main__':
    config_path = "config.Config"

    app = create_app(config_path)

    configure_structlogger(app.config)

    host, port = app.config['HOST'], int(app.config['PORT'])

    app.run(debug=app.config['DEBUG'], host=host, port=port)
