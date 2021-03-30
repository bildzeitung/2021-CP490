import uuid
from datetime import datetime

from coal_common.mixins import AttributeMixin
from coal_common.serializers import AttributeSerializer
from marshmallow_sqlalchemy import field_for, SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy_utils import UUIDType

from ..db import db


class CharacterAttributes(AttributeMixin, db.Model):
    __tablename__ = "character_attribute"
    character_id = db.Column(
        UUIDType(binary=False), db.ForeignKey("player_characters.id")
    )


class Character(db.Model):
    __tablename__ = "player_characters"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    player_id = db.Column(UUIDType(binary=False), db.ForeignKey("player.id"))
    game_id = db.Column(UUIDType(binary=False))
    attributes = db.relationship(
        "CharacterAttributes", backref="player_characters", cascade="all, delete"
    )
    title = db.Column(db.String(32), index=True)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class PlayerAttributes(AttributeMixin, db.Model):
    __tablename__ = "player_attributes"
    player_id = db.Column(UUIDType(binary=False), db.ForeignKey("player.id"))


class Player(db.Model):
    __tablename__ = "player"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(32), index=True)
    characters = db.relationship("Character", cascade="all, delete")
    attributes = db.relationship(
        "PlayerAttributes", backref="player_attributes", cascade="all, delete"
    )
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class PlayerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        load_instance = True
        exclude = ("timestamp",)


class PlayerAttributeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PlayerAttributes
        load_instance = True
        exclude = ("timestamp",)


class PlayerSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        load_instance = True
        exclude = ("timestamp",)

    attributes = AttributeSerializer(PlayerAttributeSchema, many=True)
    id = field_for(Player, "id", dump_only=True)


class PlayerDetailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        load_instance = True
        exclude = ("timestamp",)

    attributes = AttributeSerializer(PlayerAttributeSchema, many=True)


class CharacterSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Character
        load_instance = True
        exclude = ("timestamp", "player_id", "game_id")


class CharacterAttributeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CharacterAttributes
        load_instance = True
        exclude = ("timestamp",)


class CharacterDetailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Character
        load_instance = True
        exclude = ("timestamp",)

    attributes = AttributeSerializer(CharacterAttributeSchema, many=True)


class CharacterSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Character
        load_instance = True
        exclude = ("timestamp",)
        include_fk = True

    id = field_for(Character, "id", dump_only=True)
    attributes = AttributeSerializer(CharacterAttributeSchema, many=True)
