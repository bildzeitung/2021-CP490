import uuid
from datetime import datetime

from coal_common.mixins import AttributeMixin
from coal_common.serializers import AttributeSerializer
from marshmallow_sqlalchemy import field_for, SQLAlchemyAutoSchema, fields
from sqlalchemy_utils import UUIDType
from ..db import db


class ItemAttribute(AttributeMixin, db.Model):
    __tablename__ = "item_attribute"
    room_id = db.Column(UUIDType(binary=False), db.ForeignKey("item.id"))


class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    game_id = db.Column(UUIDType(binary=False))
    title = db.Column(db.String(32), index=True)
    description = db.Column(db.String(2048))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    attributes = db.relationship("ItemAttribute", backref="item", cascade="all, delete")


class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True
        exclude = (
            "timestamp",
            "description",
            "game_id",
        )


class ItemAttributeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ItemAttribute
        load_instance = True
        exclude = ("timestamp",)


class ItemSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True
        exclude = ("timestamp",)

    id = field_for(Item, "id", dump_only=True)
    attributes = AttributeSerializer(ItemAttributeSchema, many=True)


class ItemDetailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        load_instance = True
        include_relationships = True
        exclude = ("timestamp",)

    attributes = AttributeSerializer(ItemAttributeSchema, many=True)
