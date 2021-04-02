from re import L
from .common import get_character, get_item_by_title, get_current_room
from ..models import Location


def has_key(command, obj, key):
    """Does the player have the given key as a property?"""
    if obj == "character":
        o = get_character(command.character_id)

    return key in o["attributes"]


def is_true(command, obj, name, key):
    if obj == "item":
        o = get_item_by_title(command.game_id, name)
        return key in o["attributes"] and o["attributes"][key] == "true"

def item_in_room(command, item_title):
    r = get_current_room(command.game_id, command.character_id)["id"]
    i = get_item_by_title(command.game_id, item_title)["id"]
    l: Location = Location.query.filter(
        Location.game_id == command.game_id,
        Location.item_id == i,
        Location.room_id == r
        ).one_or_none()
    return l is not None