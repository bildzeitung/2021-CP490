from coal_game_server.models import GameAttribute, Location
from .common import (
    get_character,
    get_item,
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

    # items
    l: Location = Location.query.filter(
        Location.game_id == command.game_id,
        Location.character_id == None,
        Location.room_id == r["id"],
    ).all()
    if len(l) > 0:
        item_list = "\n".join(get_item(i.item_id)["description"] for i in l)
        command.buffer.append(f"\n{item_list}")

    # exits
    if r["exits"]:
        if len(r["exits"]) == 1:
            command.buffer.append(
                f"\nYou see an exit to the {r['exits'][0]['direction']}."
            )
        else:
            exit_list = ", ".join(e["direction"] for e in r["exits"])
            command.buffer.append(f"\nYou see exits to the {exit_list}.")

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
