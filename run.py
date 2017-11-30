from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(config_path):
    # create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(config_path)

    # set up DB
    SQLAlchemy(app)

    # register view blueprints
    from application.views.info_view import info_view
    from application import error_handlers
    app.register_blueprint(info_view)
    app.register_blueprint(error_handlers.blueprint)

    CORS(app)
    return app


if __name__ == '__main__':
    config_path = "config.Config"

    app = create_app(config_path)

    host, port = app.config['HOST'], int(app.config['PORT'])

    app.run(debug=app.config['DEBUG'], host=host, port=port)
