from coal_game_server.models import GameAttribute, Location
from .common import (
    get_character,
    update_character_properties,
    get_room_by_title,
    get_current_room,
)
from ..config import db


def set_key(command, obj, key, value):
    """Set a character key to a value"""
    if obj == "character":
        c = get_character(command.character_id)
        c["attributes"][key] = value
        update_character_properties(c)


def go(command, obj, key):
    """Set the room for the current character"""
    if obj == "game":
        p: GameAttribute = GameAttribute.query.filter(
            GameAttribute.game_id == command.game_id, GameAttribute.title == key
        ).one_or_none()
        r = get_room_by_title(command.game_id, p.value)

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


def message(command, obj, key):
    """Add a message to the buffer"""
    if obj == "game":
        p: GameAttribute = GameAttribute.query.filter(
            GameAttribute.game_id == command.game_id, GameAttribute.title == key
        ).one_or_none()
        command.buffer.append(p.value)


def look(command):
    """Show the description of the character's current room"""
    r = get_current_room(command.game_id, command.character_id)

    # header
    command.buffer.append(r["title"].capitalize())

    # description
    command.buffer.append(f"\t{r['description']}")

    # exits
    if r["exits"]:
        exit_list = ", ".join(e["direction"] for e in r["exits"])
        command.buffer.append(f"\nYou see exits to the {exit_list}.")

    # TODO: items
    # TODO: other characters


def go_via_exit(command, direction):
    r = get_current_room(command.game_id, command.character_id)
    for e in r["exits"]:
        if e["direction"] == direction:
            l: Location = Location.query.filter(
                Location.game_id == command.game_id,
                Location.character_id == command.character_id,
            ).one_or_none()
            l.room_id = e["to_room_id"]
            db.session.commit()
            return look(command)

    command.buffer.append("I'm sorry, but I can't go there.")
