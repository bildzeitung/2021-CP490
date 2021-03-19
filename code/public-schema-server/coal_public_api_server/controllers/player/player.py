import requests
from flask import abort, current_app


def search():
    try:
        rv = requests.get(f"{current_app.config['PLAYER_SERVER_URL']}/player")
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Could not contact player server: {str(e)}")

    return rv.json(), 200


def post(body):
    # get a list of games
    try:
        rv = requests.get(f"{current_app.config['PLAYER_SERVER_URL']}/player")
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Could not contact player server: {str(e)}")

    # submit request to game server
    try:
        rv = requests.post(
            f"{current_app.config['PLAYER_SERVER_URL']}/player", json=body
        )
        rv.raise_for_status()
    except Exception:
        abort(rv.status_code, rv.json()["detail"])

    return rv.json(), 200


def get():
    pass


def put():
    pass


def delete():
    pass
