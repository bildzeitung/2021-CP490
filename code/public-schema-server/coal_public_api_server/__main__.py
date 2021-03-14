from pathlib import Path

import attr
import click
import toml

from .config import connex_app


@attr.s(auto_attribs=True)
class Config:
    GAME_SERVER_URL: str
    CONTENT_SERVER_URL: str


def load_config(config_path, profile):
    """Read TOML file from the given path; use the given profile"""
    with open(config_path) as f:
        config = toml.load(f)
    return Config(**{k.upper(): v for k, v in config[profile].items()})


@click.command()
@click.option(
    "--config",
    "-c",
    default=Path().home() / ".config" / "coal-apiserver.conf",
    show_default=True,
)
@click.option(
    "--profile",
    "-p",
    help="Which server profile to use",
    default="DEFAULT",
    show_default=True,
)
def main(config, profile):
    connex_app.add_api(
        "openapi.yaml", arguments={"title": "Concurrent Online Adventure Land, or MUD"}
    )
    app = connex_app.app
    app.config.from_object(load_config(config, profile))
    connex_app.run(host="0.0.0.0", port=8000, debug=True)
