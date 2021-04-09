import attr
import connexion
import toml


@attr.s(auto_attribs=True)
class Config:
    GAME_SERVER_URL: str
    CONTENT_SERVER_URL: str
    PLAYER_SERVER_URL: str


def load_config(config_path, profile):
    """Read TOML file from the given path; use the given profile"""
    with open(config_path) as f:
        config = toml.load(f)
    return Config(**{k.upper(): v for k, v in config[profile].items()})



# Create the Connexion application instance
options = {"swagger_ui": False}
connex_app = connexion.App(
    __name__,
    specification_dir="./openapi",
    options=options,
    resolver=connexion.RestyResolver("coal_public_api_server.controllers"),
)
