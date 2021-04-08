from coal_game_server.models import GameAttribute, Location
from .common import (
    get_character,
    get_item,
    get_item_by_title,
    update_character_properties,
    get_room_by_title,
    get_current_room,
)
from ..config import db


def set_key(command, obj, title, key, value):
    """Set a character key to a value"""
    if obj == "character":
        c = get_character(command, title)
        c["attributes"][key] = value
        update_character_properties(c)


# | go                 | object, title, key        | move the character to the room given by `object[title][key]` |
def go(command, obj, title, key):
    """Set the room for the current character"""
    if obj == "game" and title == "#":
        p: GameAttribute = GameAttribute.query.filter(
            GameAttribute.game_id == command.game_id, GameAttribute.title == key
        ).one_or_none()
        r = get_room_by_title(command.game_id, p.value)["id"]
    elif obj == "room" and title == "#":
        r = get_current_room(command.game_id, command.character_id)["attributes"].get(
            key
        )
        if r:
            r = get_room_by_title(command.game_id, r)["id"]
        else:
            command.buffer.append("I'm sorry, but I can't go there.")
            return

    l: Location = Location.query.filter(
        Location.game_id == command.game_id,
        Location.character_id == command.character_id,
    ).one_or_none()

    if not l:
        l = Location(
            game_id=command.game_id, character_id=command.character_id, room_id=r
        )
        db.session.add(l)
    else:
        l.room_id = r

    db.session.commit()
    look(command)


def message(command, obj, title, key):
    """Add a message to the buffer"""
    if obj == "game" and title == "#":
        p: GameAttribute = GameAttribute.query.filter(
            GameAttribute.game_id == command.game_id, GameAttribute.title == key
        ).one_or_none()
        command.buffer.append(p.value)


def look(command):
    """Show the description of the character's current room"""
    r = get_current_room(command.game_id, command.character_id)

    # header
    command.buffer.append(r["title"].capitalize().replace("-", " "))

    # description
    command.buffer.append(f"\t{r['description']}")

    # items
    l: Location = Location.query.filter(
        Location.game_id == command.game_id,
        Location.character_id == None,
        Location.room_id == r["id"],
    ).all()
    if len(l) > 0:
        item_list = "\n".join(get_item(i.item_id)["description"] for i in l)
        command.buffer.append(f"\n{item_list}")

    # TODO: other characters


# | mv-item-to-char    | title                     | move `item[title]` to character's inventory                  |
def mv_item_to_char(command, title):
    """ Move item to character inventory"""
    i = get_item_by_title(command.game_id, title)
    l: Location = Location.query.filter(
        Location.game_id == command.game_id, Location.item_id == i["id"]
    ).one_or_none()
    l.room_id = None
    l.character_id = command.character_id
    db.session.commit()


# | mv-item-to-room    | title1, title2            | move `item[title2]` to `room[title1]`                        |
def mv_item_to_room(command, room_title, item_title):
    """Move item from character inventory to room"""
    if room_title == "#":  # current room
        r = get_current_room(command.game_id, command.character_id)
    elif room_title == "":  # just remove the room
        r = {"id": None}
    else:
        raise Exception("Not handled")
    i = get_item_by_title(command.game_id, item_title)["id"]
    l: Location = Location.query.filter(
        Location.game_id == command.game_id, Location.item_id == i
    ).one_or_none()
    l.room_id = r["id"]
    l.character_id = None
    db.session.commit()


# | inventory          |                           | list items located with the character (and not in a room)    |
def inventory(command):
    """Show what the character is holding"""
    l: Location = Location.query.filter(
        Location.game_id == command.game_id,
        Location.character_id == command.character_id,
        Location.room_id == None,
    ).all()
    msg_parts = []
    for i in l:
        d = get_item(i.item_id)["description"]
        msg_parts.append(d)
    if not msg_parts:
        command.buffer.append("You're not carrying anything.")
        return

    msg = "\n\t".join(msg_parts)
    command.buffer.append(f"You're carrying:\n\t{msg}")


# | dec                | object, title, key        | `object[title][key]` <- `object[title][key]` - 1             |
def dec(command, object, title, key):
    """Decrement an integer key value """
    if object == "character":
        c = get_character(command, title)
        c["attributes"][key] = str(int(c["attributes"][key]) - 1)
        update_character_properties(c)
    else:
        raise Exception("Unhandled dec")
