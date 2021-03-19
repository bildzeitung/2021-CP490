import enum
import uuid
from datetime import datetime
from marshmallow_sqlalchemy import field_for
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy_utils import UUIDType
from ..config import db, ma


class GameProperty(db.Model):
    __tablename__ = "game_property"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    game_id = db.Column(UUIDType(binary=False), db.ForeignKey("game.id"))
    title = db.Column(db.String(64), index=True)
    value = db.Column(db.String(2048))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    properties = db.relationship("GameProperty", backref="game", cascade="all, delete")
    title = db.Column(db.String(32), index=True)
    description = db.Column(db.String(2048))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class TurnStatusEnum(enum.Enum):
    OK = 1
    ERROR = 2


class Turn(db.Model):
    __tablename__ = "turn"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    character_id = db.Column(UUIDType(binary=False))
    game_id = db.Column(UUIDType(binary=False), db.ForeignKey("game.id"))
    status = db.Column(db.String(32))
    text = db.Column(db.String(2048))
    command = db.Column(db.String(2048))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class GameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Game
        load_instance = True
        exclude = ("timestamp", "description")


class GameSubmitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Game
        load_instance = True
        exclude = ("timestamp",)
        id = field_for(Game, "id", dump_only=True)


class PropertySerializer(Nested):
    def serialize(self, attr, obj, accessor=None):
        return {p.title: p.value for p in obj.properties}


class PropertySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GameProperty
        load_instance = True
        exclude = ("timestamp",)


class GameDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Game
        load_instance = True
        exclude = ("timestamp",)

    properties = PropertySerializer(PropertySchema, many=True)


class TurnSubmitSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Turn
        load_instance = True
        include_fk = True
        exclude = ("timestamp", "id")


class TurnDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Turn
        load_instance = True
        exclude = ("timestamp", "id", "game_id", "character_id", "command")
