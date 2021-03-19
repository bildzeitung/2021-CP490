import requests
from flask import current_app, abort, make_response


def search(player_id):
    try:
        rv = requests.get(
            f"{current_app.config['PLAYER_SERVER_URL']}/player/{player_id}/character"
        )
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Could not contact player server: {str(e)}")

    return rv.json(), rv.status_code


def get():
    pass


def delete(player_id, character_id):
    try:
        rv = requests.delete(
            f"{current_app.config['PLAYER_SERVER_URL']}/player/{player_id}/character/{character_id}"
        )
    except Exception as e:
        abort(500, f"Could not contact player server: {str(e)}")

    return make_response(rv.content, rv.status_code)
