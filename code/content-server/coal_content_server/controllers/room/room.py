from flask import make_response, abort
from ...db import db
from ...models import Room, RoomSchema, RoomDetailSchema, RoomSubmitSchema, RoomExit


def search(game_id=None, title=None):
    rooms = Room.query
    if game_id:
        rooms = rooms.filter(Room.game_id == game_id)

    if title:
        rooms = rooms.filter(Room.title == title)

    return RoomSchema(many=True).dump(rooms.all())


def get(room_id):
    room = Room.query.filter(Room.id == room_id).one_or_none()
    if not room:
        abort(404, f"Could not find room {room_id}")

    return RoomDetailSchema().dump(room)


def post(body):
    title = body.get("title")
    game_id = body.get("game_id")
    existing = (
        Room.query.filter(Room.title == title)
        .filter(Room.game_id == game_id)
        .one_or_none()
    )

    if existing is not None:
        abort(409, f"A room with this title: '{title}' already exists.")

    exits = body.get("exits", [])
    body["exits"] = []

    schema = RoomSubmitSchema()
    new = schema.load(body, session=db.session)
    db.session.add(new)
    db.session.commit()

    for e in exits:
        new.exits.append(RoomExit(direction=e["direction"], to_room_id=e["to_room_id"]))
    db.session.commit()

    return schema.dump(new), 201


def put():
    pass


def delete(room_id):
    room = Room.query.filter(Room.id == room_id).one_or_none()
    if not room:
        abort(404, f"Could not find game {room_id}")

    db.session.delete(room)
    db.session.commit()

    return make_response(f"Deleted {room_id}", 204)
