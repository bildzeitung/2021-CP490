from flask import abort
from ...db import db
from ...models import Room, ExitSubmitSchema


def search():
    pass


def post(room_id, body):
    room = Room.query.filter(Room.id == room_id).one_or_none()
    if not room:
        abort(404, f"Could not find room {room_id}")

    body["from_room_id"] = room_id
    schema = ExitSubmitSchema()
    new = schema.load(body, session=db.session)
    db.session.add(new)
    db.session.commit()

    return schema.dump(new), 200


def get():
    pass


def delete():
    pass
