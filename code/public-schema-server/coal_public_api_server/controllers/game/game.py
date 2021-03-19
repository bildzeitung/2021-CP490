import requests
from flask import abort, make_response, current_app


def search():
    try:
        rv = requests.get(f"{current_app.config['GAME_SERVER_URL']}/game")
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Could not contact game server: {str(e)}")

    return rv.json(), rv.status_code


def get(game_id):
    try:
        rv = requests.get(f"{current_app.config['GAME_SERVER_URL']}/game/{game_id}")
        rv.raise_for_status()
    except Exception:
        abort(rv.status_code, rv.json()["detail"])

    return rv.json(), rv.status_code


def post(body):
    try:
        rv = requests.post(f"{current_app.config['GAME_SERVER_URL']}/game", json=body)
        rv.raise_for_status()
    except Exception:
        abort(rv.status_code, rv.json()["detail"])

    return rv.json(), rv.status_code


def put(game_id, body):
    # submit request to game server
    try:
        rv = requests.put(
            f"{current_app.config['GAME_SERVER_URL']}/game/{game_id}", json=body
        )
        rv.raise_for_status()
    except Exception:
        abort(rv.status_code, rv.json()["detail"])

    return rv.json(), rv.status_code


def delete(game_id):
    try:
        rv = requests.delete(f"{current_app.config['GAME_SERVER_URL']}/game/{game_id}")
        rv.raise_for_status()
    except Exception:
        abort(rv.status_code, rv.json()["detail"])

    return make_response(rv.content, rv.status_code)
