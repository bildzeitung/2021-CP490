import uuid
from datetime import datetime
from marshmallow_sqlalchemy import field_for
from sqlalchemy_utils import UUIDType
from ..config import db, ma


class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(32), index=True)
    description = db.Column(db.String(2048))
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


class GameDetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Game
        load_instance = True
        exclude = ("timestamp",)
