from pathlib import Path

import click
from .config import connex_app, load_config


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
