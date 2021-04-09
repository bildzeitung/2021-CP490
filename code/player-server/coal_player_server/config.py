import attr
import connexion
import toml
from connexion.resolver import RestyResolver
from .db import db


CONNEXION_ARGS = {"title": "COAL Player Server"}
DBNAME = "coal-player.db"


@attr.s(auto_attribs=True)
class ServerConfig:
    DB_PATH: str


def load_config(config_path, profile):
    """Read TOML file from the given path; use the given profile"""
    with open(config_path) as f:
        config = toml.load(f)
    return ServerConfig(**{k.upper(): v for k, v in config[profile].items()})


@attr.s()
class DefaultConfig:
    SQLALCHEMY_ECHO = attr.ib(default=True)
    SQLALCHEMY_DATABASE_URI = attr.ib(default="sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = attr.ib(default=False)


def create_app(config_object):  # Create the Connexion application instance
    connex_options = {"swagger_ui": False}
    connex_app = connexion.App(
        __name__,
        specification_dir="./openapi",
        options=connex_options,
        resolver=RestyResolver("coal_player_server.controllers"),
    )

    # Get & configure the underlying Flask app instance
    app = connex_app.app
    app.config.from_object(config_object)
    db.init_app(app)

    return connex_app
