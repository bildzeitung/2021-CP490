from flask import abort

from ...models import Player, PlayerSchema, PlayerSubmitSchema, PlayerDetailSchema
from ...db import db


def search():
    players = Player.query.all()
    return PlayerSchema(many=True).dump(players)


def get(player_id):
    player = Player.query.filter(Player.id == player_id).one_or_none()

    if not player:
        abort(404, f"Player {player_id} not found")

    return PlayerDetailSchema().dump(player), 200


def post(body):
    title = body.get("title")
    existing = Player.query.filter(Player.title == title).one_or_none()

    if existing is not None:
        abort(409, f"A player with this title: '{title}' already exists.")

    schema = PlayerSubmitSchema()
    new = schema.load(body, session=db.session)
    db.session.add(new)
    db.session.commit()

    return schema.dump(new), 201


def put():
    pass


def delete():
    pass
