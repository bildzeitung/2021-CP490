from flask import abort
from ..config import db
from ..models import Item, ItemSchema, ItemSubmitSchema, ItemDetailSchema


def search(game_id=None, title=None):
    items = Item.query
    if game_id:
        items = items.filter(Item.game_id == game_id)

    if title:
        items = items.filter(Item.title == title)

    return ItemSchema(many=True).dump(items.all())


def get(item_id):
    item = Item.query.filter(Item.id == item_id).one_or_none()
    if not item:
        abort(404, f"Could not find room {item_id}")

    return ItemDetailSchema().dump(item)


def post(body):
    title = body.get("title")
    game_id = body.get("game_id")
    existing = (
        Item.query.filter(Item.title == title)
        .filter(Item.game_id == game_id)
        .one_or_none()
    )

    if existing is not None:
        abort(409, f"An item with this title: '{title}' already exists.")

    schema = ItemSubmitSchema()
    new = schema.load(body, session=db.session)
    db.session.add(new)
    db.session.commit()

    return schema.dump(new), 201


def put():
    pass


def delete():
    pass
