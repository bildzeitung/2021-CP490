import uuid
from datetime import datetime

from coal_common.mixins import AttributeMixin
from coal_common.serializers import AttributeSerializer
from marshmallow_sqlalchemy import field_for, SQLAlchemyAutoSchema
from sqlalchemy_utils import UUIDType
from ..db import db


class RoomAttribute(AttributeMixin, db.Model):
    __tablename__ = "room_attribute"
    room_id = db.Column(UUIDType(binary=False), db.ForeignKey("room.id"))


class Room(db.Model):
    __tablename__ = "room"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    game_id = db.Column(UUIDType(binary=False))
    title = db.Column(db.String(32), index=True)
    description = db.Column(db.String(2048))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    attributes = db.relationship("RoomAttribute", backref="room", cascade="all, delete")


class RoomSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        load_instance = True
        exclude = (
            "timestamp",
            "description",
            "game_id",
        )


class RoomAttributeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RoomAttribute
        load_instance = True
        exclude = ("timestamp",)


class RoomSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        load_instance = True
        exclude = ("timestamp",)

    id = field_for(Room, "id", dump_only=True)
    attributes = AttributeSerializer(RoomAttributeSchema, many=True)


class RoomDetailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        load_instance = True
        include_relationships = True
        exclude = ("timestamp",)

    attributes = AttributeSerializer(RoomAttributeSchema, many=True)
