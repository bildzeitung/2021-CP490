import requests
from flask import current_app, abort


def post(game_id, player_id, body):
    try:
        rv = requests.post(
            f"{current_app.config['GAME_SERVER_URL']}/game/{game_id}/player/{player_id}/character",
            json=body,
        )
        rv.raise_for_status()
    except Exception:
        abort(rv.status_code, rv.json()["detail"])

    return rv.json(), rv.status_code
