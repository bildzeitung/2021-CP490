import requests
from flask import abort, current_app

from ....models import Game


def post(game_id, player_id, body):
    game = Game.query.filter(Game.id == game_id).one_or_none()
    if not game:
        abort(404, f"Could not find game {game_id}")

    starting_room = [p.value for p in game.attributes if p.title == "starting-room"]
    if not starting_room:
        abort(400, f"Could not create a character -- need a starting room")

    body["location"] = starting_room[0]

    try:
        rv = requests.post(
            f"{current_app.config['PLAYER_SERVER_URL']}/game/{game_id}/player/{player_id}/character",
            json=body,
        )
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Could not contact player server: {str(e)}")

    return rv.json(), rv.status_code
