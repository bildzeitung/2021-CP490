from flask import make_response, abort
from ...config import db
from ...models import Location, LocationSchema


def search(game_id):
    locations = Location.query.filter(Location.game_id == game_id).all()
    return LocationSchema(many=True).dump(locations)


def get(game_id):
    return
    game = Game.query.filter(Game.id == game_id).one_or_none()
    if not game:
        abort(404, f"Could not find game {game_id}")

    return GameDetailSchema().dump(game)


def post(body):
    return
    title = body.get("title")
    existing_game = Game.query.filter(Game.title == title).one_or_none()

    if existing_game is not None:
        abort(409, f"A game with this title: '{title}' already exists.")

    if body.get("attributes"):
        body["attributes"] = [
            {"title": k, "value": v} for k, v in body["properties"].items()
        ]

    schema = GameSubmitSchema()
    new_game = schema.load(body, session=db.session)
    db.session.add(new_game)
    db.session.commit()

    data = schema.dump(new_game)

    return data, 201


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
