from pathlib import Path

import connexion
from connexion.resolver import RestyResolver
from .db import db


class DefaultConfig:
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////" + str(
        Path(__file__).parent / "coal-content.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app(config_object):  # Create the Connexion application instance
    connex_options = {"swagger_ui": False}
    connex_app = connexion.App(
        __name__,
        specification_dir="./openapi",
        options=connex_options,
        resolver=RestyResolver("coal_content_server.controllers"),
    )

    # Get & configure the underlying Flask app instance
    app = connex_app.app
    app.config.from_object(config_object)
    db.init_app(app)

    return connex_app
