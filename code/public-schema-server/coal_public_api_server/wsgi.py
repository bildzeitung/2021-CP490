from .config import connex_app, load_config


def main(*args, **kwargs):
    connex_app.add_api(
        "openapi.yaml", arguments={"title": "Concurrent Online Adventure Land, or MUD"}
    )
    app = connex_app.app
    app.config.from_object(
        load_config(kwargs["config"], kwargs.get("profile", "DEFAULT"))
    )

    return app
