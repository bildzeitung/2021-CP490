import uuid
from datetime import datetime
from marshmallow_sqlalchemy import field_for, SQLAlchemyAutoSchema

from sqlalchemy_utils import UUIDType

from ..config import db


class Location(db.Model):
    __tablename__ = "location"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    game_id = db.Column(UUIDType(binary=False), db.ForeignKey("game.id"))
    room_id = db.Column(UUIDType(binary=False))
    item_id = db.Column(UUIDType(binary=False))
    character_id = db.Column(UUIDType(binary=False))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class LocationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True
        exclude = ("timestamp",)
