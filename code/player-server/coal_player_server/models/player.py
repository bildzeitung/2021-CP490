import uuid
from datetime import datetime
from marshmallow_sqlalchemy import field_for, SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy_utils import UUIDType
from ..db import db


class Item(db.Model):
    __tablename__ = "character_items"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    character_id = db.Column(
        UUIDType(binary=False), db.ForeignKey("player_characters.id")
    )
    item_id = db.Column(UUIDType(binary=False), default=uuid.uuid4)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class CharacterProperty(db.Model):
    __tablename__ = "character_property"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    character_id = db.Column(
        UUIDType(binary=False), db.ForeignKey("player_characters.id")
    )
    title = db.Column(db.String(64), index=True)
    value = db.Column(db.String(2048))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Character(db.Model):
    __tablename__ = "player_characters"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    player_id = db.Column(UUIDType(binary=False), db.ForeignKey("player.id"))
    game_id = db.Column(UUIDType(binary=False))
    properties = db.relationship(
        "CharacterProperty", backref="player_characters", cascade="all, delete"
    )
    title = db.Column(db.String(32), index=True)
    items = db.relationship("Item", cascade="all, delete")
    location = db.Column(UUIDType(binary=False))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Player(db.Model):
    __tablename__ = "player"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(32), index=True)
    characters = db.relationship("Character", cascade="all, delete")
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class PlayerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        load_instance = True
        exclude = ("timestamp",)


class PlayerSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        load_instance = True
        exclude = ("timestamp",)

    id = field_for(Player, "id", dump_only=True)


class PlayerDetailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        load_instance = True
        exclude = ("timestamp",)


class CharacterSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Character
        load_instance = True
        exclude = ("timestamp", "player_id", "items", "location", "game_id")


class PropertySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CharacterProperty
        load_instance = True
        exclude = ("timestamp",)


class PropertySerializer(Nested):
    def serialize(self, attr, obj, accessor=None):
        return {p.title: p.value for p in obj.properties}


class CharacterDetailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Character
        load_instance = True
        exclude = ("timestamp",)

    properties = PropertySerializer(PropertySchema, many=True)


class CharacterSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Character
        load_instance = True
        exclude = (
            "timestamp",
            "items",
        )
        include_fk = True

    id = field_for(Character, "id", dump_only=True)
