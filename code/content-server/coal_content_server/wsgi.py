from pathlib import Path
from .config import create_app, DefaultConfig, load_config, CONNEXION_ARGS, DBNAME


def main(*args, **kwargs):
    server_config = load_config(kwargs["config"], kwargs.get("profile", "DEFAULT"))
    dbpath = "sqlite:///" + str(Path(server_config.DB_PATH) / DBNAME)
    connex_app = create_app(DefaultConfig(SQLALCHEMY_DATABASE_URI=dbpath))
    connex_app.add_api("openapi.yaml", arguments=CONNEXION_ARGS)

    return connex_app.app
