import requests
from flask import current_app, abort


def search():
    raise Exception("not implemented")


def get():
    raise Exception("not implemented")


def post(game_id, body):
    try:
        rv = requests.post(
            f"{current_app.config['GAME_SERVER_URL']}/game/{game_id}/event", json=body
        )
        rv.raise_for_status()
    except Exception:
        abort(rv.status_code, rv.json()["detail"])

    return rv.json(), rv.status_code


def put():
    raise Exception("not implemented")


def delete():
    raise Exception("not implemented")
