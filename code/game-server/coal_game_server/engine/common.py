import requests
from flask import current_app, abort

from ..models import Location


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


def get_current_room(game_id, character_id):
    l: Location = Location.query.filter(
        Location.game_id == game_id, Location.character_id == character_id
    ).one_or_none()
    return get_room(l.room_id)


def get_item(item_id):
    try:
        rv = requests.get(f"{current_app.config['CONTENT_SERVER_URL']}/item/{item_id}")
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Could not contact game server: {str(e)}")

    return rv.json()

def get_item_by_title(game_id, title):
    try:
        rv = requests.get(f"{current_app.config['CONTENT_SERVER_URL']}/item", params={"title":title, "game_id": game_id})
        rv.raise_for_status()
        rv = requests.get(f"{current_app.config['CONTENT_SERVER_URL']}/item/{rv.json()[0]['id']}")
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Could not contact game server: {str(e)}")

    return rv.json()
