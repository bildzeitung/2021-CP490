from flask import abort

from ...models import Player, PlayerSchema, PlayerSubmitSchema
from ...db import db


def search():
    players = Player.query.all()
    return PlayerSchema(many=True).dump(players)


def get():
    pass


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
