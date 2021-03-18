from flask import abort, make_response

from ...db import db
from ...models import Player, CharacterSchema, CharacterSubmitSchema, Character


def search(player_id):
    player = Player.query.filter(Player.id == player_id).one_or_none()

    return CharacterSchema(many=True).dump(player.characters)


def get():
    pass


def post(player_id, body):
    title = body.get("title")
    existing = Character.query.filter(Character.player_id == player_id).filter(Character.title == title).one_or_none()

    if existing is not None:
        abort(409, f"A player with this title: '{title}' already exists.")

    schema = CharacterSubmitSchema()
    new = schema.load(body, session=db.session)
    db.session.add(new)
    db.session.commit()

    return schema.dump(new), 201


def put():
    pass


def delete(player_id, character_id):
    c = Character.query.filter(Character.id == character_id).one_or_none()
    if not c:
        abort(404, f"Could not find character {character_id}")

    db.session.delete(c)
    db.session.commit()

    return make_response(f"Deleted {character_id}", 204)

