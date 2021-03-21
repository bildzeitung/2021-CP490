from flask import make_response, abort
from coal_game_server.models.game import GameEvent
from ...models import EventSubmitSchema, EventSchema
from ...config import db


def search():
    events = GameEvent.query.all()
    return EventSchema(many=True).dump(events)


def get():
    pass


def post(game_id, body):
    body["game_id"] = game_id

    # marshal the nested items
    for item in ("conditions", "true_part", "false_part"):
        for c in body.get(item, []):
            arguments = [{"title": t} for t in c["arguments"]]
            c["arguments"] = arguments

    schema = EventSubmitSchema()
    new = schema.load(body, session=db.session)
    db.session.add(new)
    db.session.commit()

    return EventSchema().dump(new), 201


def put():
    pass


def delete(game_id, event_id):
    event = GameEvent.query.filter(GameEvent.id == event_id).one_or_none()
    if not event:
        abort(404, f"Could not find event {event_id}")

    db.session.delete(event)
    db.session.commit()

    return make_response(f"Deleted {event_id}", 204)
