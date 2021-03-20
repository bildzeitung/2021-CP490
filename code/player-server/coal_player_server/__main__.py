from .config import create_app, DefaultConfig


def main():
    connex_app = create_app(DefaultConfig())
    connex_app.add_api("openapi.yaml", arguments={"title": "COAL Player Server"})
    connex_app.run(host="0.0.0.0", port=8300, debug=True)