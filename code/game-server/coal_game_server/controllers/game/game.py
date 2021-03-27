from flask import make_response, abort
from ...config import db
from ...models import Game, GameSchema, GameSubmitSchema, GameDetailSchema, GameProperty


def search():
    games = Game.query.all()
    return GameSchema(many=True).dump(games)


def get(game_id):
    game = Game.query.filter(Game.id == game_id).one_or_none()
    if not game:
        abort(404, f"Could not find game {game_id}")

    return GameDetailSchema().dump(game)


def post(body):
    title = body.get("title")
    existing_game = Game.query.filter(Game.title == title).one_or_none()

    if existing_game is not None:
        abort(409, f"A game with this title: '{title}' already exists.")

    if body.get("properties"):
        body["properties"] = [{"title": k, "value":v} for k, v in body["properties"].items()]

    schema = GameSubmitSchema()
    new_game = schema.load(body, session=db.session)
    db.session.add(new_game)
    db.session.commit()

    data = schema.dump(new_game)

    return data, 201


def put(game_id, body):
    game = Game.query.filter(Game.id == game_id).one_or_none()
    if not game:
        abort(404, f"Could not find game {game_id}")

    props = body.get("properties")
    if props is not None:
        # delete existing properties
        game.properties.clear()
        # replace with incoming
        game.properties.extend(
            GameProperty(title=k, value=v, game_id=game_id) for k, v in props.items()
        )
        db.session.commit()

    return GameDetailSchema().dump(game), 200


def delete(game_id):
    game = Game.query.filter(Game.id == game_id).one_or_none()
    if not game:
        abort(404, f"Could not find game {game_id}")

    db.session.delete(game)
    db.session.commit()

    return make_response(f"Deleted {game_id}", 204)
