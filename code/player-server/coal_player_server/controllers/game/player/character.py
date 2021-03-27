from flask import abort

from ....config import db
from ....models import Character, CharacterSubmitSchema

def post(game_id, player_id, body):
    title = body.get("title")
    existing = (
        Character.query.filter(Character.player_id == player_id)
        .filter(Character.title == title)
        .one_or_none()
    )
    if existing is not None:
        abort(409, f"A player with this title: '{title}' already exists.")

    body["player_id"] = player_id
    body["game_id"] = game_id

    schema = CharacterSubmitSchema()
    new = schema.load(body, session=db.session)
    db.session.add(new)
    db.session.commit()

    return schema.dump(new), 201