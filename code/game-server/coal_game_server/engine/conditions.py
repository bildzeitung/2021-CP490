from .common import resolve_object, get_item_by_title, get_room, get_room_by_title
from ..models import Location


# | is-equal           | object, title, key, value | True if `object[title][key]` == `value`                      |
def is_equal(command, object, title, key, value):
    o = resolve_object(command, object, title)
    return key in o["attributes"] and o["attributes"][key] == value


# | is-gt              | object, title, key, value | True if `object[title][key]` & `object[title][key]` > `value`|
def is_gt(command, object, title, key, value):
    o = resolve_object(command, object, title)
    return key in o["attributes"] and int(o["attributes"][key]) > int(value)


# | obj-loc-is-equal   | object, title, value      | True if `object[title]` location == `value`                  |
def obj_loc_is_equal(command, object, title, value):
    if value == "#":  # character's current room
        l: Location = Location.query.filter(
            Location.game_id == command.game_id,
            Location.character_id == command.character_id,
        ).one_or_none()
        r = get_room(l.room_id)["id"]
    elif value == "character":  # is the character holding the item?
        i = get_item_by_title(command.game_id, title)
        if not i:
            return False
        l: Location = Location.query.filter(
            Location.game_id == command.game_id,
            Location.character_id == command.character_id,
            Location.item_id == i["id"],
        ).one_or_none()
        return l is not None
    else:
        raise Exception("Unsupported obj_loc_is_equal")

    if object == "item":
        i = get_item_by_title(command.game_id, title)["id"]
        l: Location = Location.query.filter(
            Location.game_id == command.game_id,
            Location.item_id == i,
            Location.room_id == r,
        ).one_or_none()
        return l is not None

    raise Exception("Cannot handle this case")
