import requests
from flask import current_app, abort, make_response


def search(game_id):
    try:
        rv = requests.get(f"{current_app.config['GAME_SERVER_URL']}/game/{game_id}/event")
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Could not contact game server: {str(e)}")

    return rv.json(), rv.status_code


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


def delete(game_id, event_id):
    try:
        rv = requests.delete(
            f"{current_app.config['GAME_SERVER_URL']}/game/{game_id}/event/{event_id}"
        )
        rv.raise_for_status()
    except Exception:
        abort(rv.status_code, rv.json()["detail"])

    return make_response(rv.content, rv.status_code)
