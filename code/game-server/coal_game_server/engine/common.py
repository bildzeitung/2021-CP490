import requests
from flask import current_app, abort


def get_character(character_id):
    try:
        rv = requests.get(
            f"{current_app.config['PLAYER_SERVER_URL']}/character/{character_id}"
        )
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Could not contact player server: {str(e)}")

    return rv.json()


def get_room(room_id):
    try:
        rv = requests.get(f"{current_app.config['CONTENT_SERVER_URL']}/room/{room_id}")
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Could not contact game server: {str(e)}")

    return rv.json()


def get_room_by_title(game_id, title):
    try:
        rv = requests.get(
            f"{current_app.config['CONTENT_SERVER_URL']}/room",
            params={"game_id": game_id, "title": title},
        )
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Could not contact game server: {str(e)}")

    room_id = rv.json()[0]["id"]
    return room_id


def update_character_properties(character):
    body = {"attributes": character["attributes"]}
    try:
        rv = requests.put(
            f"{current_app.config['PLAYER_SERVER_URL']}/character/{character['id']}",
            json=body,
        )
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Could not contact player server: {str(e)}")
