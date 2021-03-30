from coal_game_server.models import Game, GameAttribute, Location
from .common import (
    get_character,
    update_character_properties,
    get_room,
    get_room_by_title,
)
from ..config import db


def set_key(command, key, value):
    """Set a character key to a value"""
    c = get_character(command.character_id)
    c["attributes"][key] = value

    update_character_properties(c)


def set_room(command, key):
    """Set the room for the current character"""
    p: GameAttribute = GameAttribute.query.filter(
        GameAttribute.game_id == command.game_id, GameAttribute.title == key
    ).one_or_none()
    c = get_character(command.character_id)["id"]
    r = get_room_by_title(command.game_id, p.value)

    l: Location = Location.query.filter(
        Location.game_id == command.game_id, Location.character_id == c
    ).one_or_none()
    if not l:
        l = Location(game_id=command.game_id, character_id=c, room_id=r)
        db.session.add(l)
    else:
        l.room_id = r
    db.session.commit()


def message(command, key):
    """Add a message to the buffer"""
    g: Game = Game.query.filter(Game.id == command.game_id).one_or_none()
    p: GameAttribute
    for p in g.attributes:
        if p.title == key:
            command.buffer.append(p.value)
            return


def look(command):
    """Show the description of the character's current room"""
    c = get_character(command.character_id)["id"]

    l: Location = Location.query.filter(
        Location.game_id == command.game_id, Location.character_id == c
    ).one_or_none()
    r = get_room(l.room_id)

    # header
    command.buffer.append(r["title"].capitalize())

    # description
    command.buffer.append(f"\t{r['description']}")

    # exits
    if r["exits"]:
        exit_list = ", ".join(e["direction"] for e in r["exits"])
        command.buffer.append(f"\nYou see exits to the {exit_list}.")

    # items
