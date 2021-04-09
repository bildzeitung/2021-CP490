from pathlib import Path
import click

from .config import create_app, DefaultConfig, load_config, CONNEXION_ARGS


@click.command()
@click.option(
    "--config",
    "-c",
    default=Path().home() / ".config" / "coal-gameserver.conf",
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
    server_config = load_config(config, profile)
    dbpath = "sqlite:///" + str(Path(server_config.DB_PATH) / "coal-game.db")
    connex_app = create_app(DefaultConfig(SQLALCHEMY_DATABASE_URI=dbpath))
    connex_app.add_api("openapi.yaml", arguments=CONNEXION_ARGS)
    app = connex_app.app
    app.config.from_object(server_config)
    connex_app.run(host="0.0.0.0", port=8100, debug=True)
