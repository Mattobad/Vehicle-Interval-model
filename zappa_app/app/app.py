from flask import Flask
from app.controller import prediction_app


# factory functions
def create_app(config_object) -> Flask:
    """
    Create a flask app instance
    """

    flask_app = Flask('ml_api')
    flask_app.config.from_object(config_object)

    # register blueprints
    flask_app.register_blueprint(prediction_app)


    return flask_app