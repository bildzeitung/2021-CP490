import requests

from flask import current_app, abort


def search(game_id):
    try:
        rv = requests.get(
            f"{current_app.config['CONTENT_SERVER_URL']}/item?game_id={game_id}"
        )
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Could not contact content server: {str(e)}")

    return rv.json(), 200


def get():
    pass


def post(game_id, body):
    body["game_id"] = game_id
    try:
        rv = requests.post(
            f"{current_app.config['CONTENT_SERVER_URL']}/item", json=body
        )
        rv.raise_for_status()
    except Exception:
        abort(rv.status_code, rv.json()["detail"])

    return rv.json(), 201


def put():
    pass


def delete():
    pass
