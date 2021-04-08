import requests
from flask import current_app, abort

from ..models import Location


def resolve_object(command, object, title):
    """Fetch an object (character, item, room)

    :dict: Object's JSON representation
    """
    if object == "character":
        return get_character(command, title)

    if object == "item":
        return get_item_by_title(command.game_id, title)

    raise Exception("Can't handle this")


def get_character(command, title):
    character = command.character_id
    if title != "#":
        raise Exception("I can't handle that")

    try:
        rv = requests.get(
            f"{current_app.config['PLAYER_SERVER_URL']}/character/{character}"
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
        abort(500, f"Game server error: {str(e)}")

    return rv.json()[0]


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
        Location.game_id == game_id,
        Location.character_id == character_id,
        Location.item_id == None,
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
        rv = requests.get(
            f"{current_app.config['CONTENT_SERVER_URL']}/item",
            params={"title": title, "game_id": game_id},
        )
        rv.raise_for_status()
        if not rv.json():
            return None
        rv = requests.get(
            f"{current_app.config['CONTENT_SERVER_URL']}/item/{rv.json()[0]['id']}"
        )
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Game server error: {str(e)}")

    return rv.json()
