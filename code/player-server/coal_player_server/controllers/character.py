from flask import abort
from ..models import Character, CharacterDetailSchema, CharacterAttributes
from ..config import db


def get(character_id):
    c = Character().query.filter(Character.id == character_id).one_or_none()
    if not c:
        return abort(404, f"Cannot find {character_id}")

    return CharacterDetailSchema().dump(c)


def put(character_id, body):
    c = Character.query.filter(Character.id == character_id).one_or_none()
    if not c:
        abort(404, f"Could not find character {character_id}")
    attributes = body.get("attributes")
    if attributes is not None:
        # delete existing properties
        c.attributes.clear()
        # replace with incoming
        c.attributes.extend(
            CharacterAttributes(title=k, value=v, character_id=character_id)
            for k, v in attributes.items()
        )
        db.session.commit()

    return CharacterDetailSchema().dump(c), 200
