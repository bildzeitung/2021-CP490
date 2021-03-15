import uuid
from datetime import datetime
from marshmallow_sqlalchemy import field_for, SQLAlchemyAutoSchema, fields
from sqlalchemy_utils import UUIDType
from ..db import db


class RoomExit(db.Model):
    __tablename__ = "room_exit"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    from_room_id = db.Column(UUIDType(binary=False), db.ForeignKey("room.id"))
    to_room_id = db.Column(UUIDType(binary=False), db.ForeignKey("room.id"))
    direction = db.Column(db.String(16))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Room(db.Model):
    __tablename__ = "room"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    game_id = db.Column(UUIDType(binary=False))
    title = db.Column(db.String(32), index=True)
    description = db.Column(db.String(2048))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    exits = db.relationship(
        "RoomExit", foreign_keys=[RoomExit.from_room_id], cascade="all, delete"
    )
    exit_to_me = db.relationship(
        "RoomExit", foreign_keys=[RoomExit.to_room_id], cascade="all, delete"
    )


class ExitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RoomExit
        load_instance = True
        include_fk = True
        exclude = ("timestamp", "from_room_id")


class ExitSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = RoomExit
        load_instance = True
        include_fk = True
        exclude = ("timestamp", )


class RoomSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        load_instance = True
        exclude = ("timestamp", "description", "game_id")


class RoomSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        load_instance = True
        exclude = ("timestamp",)

    id = field_for(Room, "id", dump_only=True)
    exits = fields.Nested(ExitSchema, many=True)


class RoomDetailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        load_instance = True
        include_relationships = True
        exclude = ("timestamp",)

    exits = fields.Nested(ExitSchema, many=True)