from .config import db, create_app, DefaultConfig, load_config, DBNAME
from pathlib import Path
import click
from .models import Player


@click.command()
@click.option(
    "--config",
    "-c",
    default=Path().home() / ".config" / "coal-playerserver.conf",
    show_default=True,
)
@click.option(
    "--profile",
    "-p",
    help="Which server profile to use",
    default="DEFAULT",
    show_default=True,
)
def build_database(config, profile):
    server_config = load_config(config, profile)
    dbpath = "sqlite:///" + str(Path(server_config.DB_PATH) / DBNAME)
    app = create_app(DefaultConfig(SQLALCHEMY_DATABASE_URI=dbpath))
    with app.app.app_context():
        # Create the database
        print("Creating all tables...")
        db.create_all()
