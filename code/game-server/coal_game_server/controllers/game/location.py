from flask import make_response, abort
from ...config import db
from ...models import Location, LocationSchema, LocationSubmitSchema


def search(game_id):
    locations = Location.query.filter(Location.game_id == game_id).all()
    return LocationSchema(many=True).dump(locations)


def get(game_id):
    return
    game = Game.query.filter(Game.id == game_id).one_or_none()
    if not game:
        abort(404, f"Could not find game {game_id}")

    return GameDetailSchema().dump(game)


def post(game_id, body):
    body["game_id"] = game_id

    schema = LocationSubmitSchema()
    new_schema = schema.load(body, session=db.session)
    db.session.add(new_schema)
    db.session.commit()

    return schema.dump(new_schema), 201


def put(game_id, body):
    return
    game = Game.query.filter(Game.id == game_id).one_or_none()
    if not game:
        abort(404, f"Could not find game {game_id}")

    props = body.get("attributes")
    if props is not None:
        # delete existing properties
        game.attributes.clear()
        # replace with incoming
        game.attributes.extend(
            GameAttribute(title=k, value=v, game_id=game_id) for k, v in props.items()
        )
        db.session.commit()

    return GameDetailSchema().dump(game), 200


def delete(game_id):
    return
    game = Game.query.filter(Game.id == game_id).one_or_none()
    if not game:
        abort(404, f"Could not find game {game_id}")

    db.session.delete(game)
    db.session.commit()

    return make_response(f"Deleted {game_id}", 204)
