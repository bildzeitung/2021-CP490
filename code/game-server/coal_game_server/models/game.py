import enum
import uuid
from datetime import datetime
from marshmallow_sqlalchemy import field_for, SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_utils import UUIDType
from ..config import db


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
    command = db.Column(db.String(2048))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class EventItemConditionArgument(db.Model):
    __tablename__ = "game_event_item_condition_argument"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    event_item_id = db.Column(
        UUIDType(binary=False), db.ForeignKey("game_event_condition_item.id")
    )
    position = db.Column(db.Integer)
    title = db.Column(db.String(2048))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class EventConditionItem(db.Model):
    __tablename__ = "game_event_condition_item"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    event_id = db.Column(UUIDType(binary=False), db.ForeignKey("game_event.id"))
    position = db.Column(db.Integer)
    primitive = db.Column(db.String(64))
    arguments = db.relationship(
        EventItemConditionArgument,
        collection_class=ordering_list("position"),
        cascade="all, delete",
    )
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class EventItemTrueArgument(db.Model):
    __tablename__ = "game_event_item_true_argument"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    event_item_id = db.Column(
        UUIDType(binary=False), db.ForeignKey("game_event_true_item.id")
    )
    position = db.Column(db.Integer)
    title = db.Column(db.String(2048))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class EventConditionTrueItem(db.Model):
    __tablename__ = "game_event_true_item"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    event_id = db.Column(UUIDType(binary=False), db.ForeignKey("game_event.id"))
    position = db.Column(db.Integer)
    primitive = db.Column(db.String(64))
    arguments = db.relationship(
        EventItemTrueArgument,
        collection_class=ordering_list("position"),
        cascade="all, delete",
    )
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class EventItemFalseArgument(db.Model):
    __tablename__ = "game_event_item_false_argument"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    event_item_id = db.Column(
        UUIDType(binary=False), db.ForeignKey("game_event_false_item.id")
    )
    position = db.Column(db.Integer)
    title = db.Column(db.String(2048))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class EventConditionFalseItem(db.Model):
    __tablename__ = "game_event_false_item"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    event_id = db.Column(UUIDType(binary=False), db.ForeignKey("game_event.id"))
    position = db.Column(db.Integer)
    primitive = db.Column(db.String(64))
    arguments = db.relationship(
        EventItemFalseArgument,
        collection_class=ordering_list("position"),
        cascade="all, delete",
    )
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class GameEvent(db.Model):
    __tablename__ = "game_event"
    id = db.Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    game_id = db.Column(UUIDType(binary=False), db.ForeignKey("game.id"))
    command = db.Column(db.String(2048))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    conditions = db.relationship(
        EventConditionItem,
        collection_class=ordering_list("position"),
        cascade="all, delete",
    )
    true_part = db.relationship(
        EventConditionTrueItem,
        collection_class=ordering_list("position"),
        cascade="all, delete",
    )
    false_part = db.relationship(
        EventConditionFalseItem,
        collection_class=ordering_list("position"),
        cascade="all, delete",
    )


class GameSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Game
        load_instance = True
        exclude = ("timestamp", "description")


class GameSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Game
        load_instance = True
        exclude = ("timestamp",)
        id = field_for(Game, "id", dump_only=True)


class PropertySerializer(Nested):
    def serialize(self, attr, obj, accessor=None):
        return {p.title: p.value for p in obj.properties}


class PropertySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GameProperty
        load_instance = True
        exclude = ("timestamp",)


class GameDetailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Game
        load_instance = True
        exclude = ("timestamp",)

    properties = PropertySerializer(PropertySchema, many=True)


class TurnSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Turn
        load_instance = True
        include_fk = True
        exclude = ("timestamp", "id")


class TurnDetailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Turn
        load_instance = True
        exclude = ("timestamp", "id", "game_id", "character_id", "command")


class SmartNested(Nested):
    def serialize(self, attr, obj, accessor=None):
        if attr == "arguments":
            return [x.title for x in obj.arguments]
        return super(SmartNested, self).serialize(attr, obj, accessor)


class EventConditionArgumentSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EventItemConditionArgument
        load_instance = True
        exclude = ("timestamp",)


class EventConditionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EventConditionItem
        load_instance = True
        exclude = ("timestamp",)

    arguments = SmartNested(
        EventConditionArgumentSubmitSchema, many=True, exclude=("id", "position")
    )


class EventTrueSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EventConditionTrueItem
        load_instance = True
        exclude = ("timestamp",)

    arguments = SmartNested(
        EventItemTrueArgument, many=True, exclude=("id", "position")
    )


class EventFalseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EventConditionFalseItem
        load_instance = True
        exclude = ("timestamp",)

    arguments = SmartNested(
        EventItemFalseArgument, many=True, exclude=("id", "position")
    )


class EventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GameEvent
        load_instance = True
        exclude = ("timestamp",)
        include_fk = True

    conditions = Nested(EventConditionSchema, many=True, exclude=("id", "position"))
    true_part = Nested(EventTrueSchema, many=True, exclude=("id", "position"))
    false_part = Nested(EventFalseSchema, many=True, exclude=("id", "position"))


class EventConditionArgumentSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EventItemConditionArgument
        load_instance = True
        exclude = ("timestamp",)

    id = field_for(EventItemConditionArgument, "id", dump_only=True)


class EventConditionSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EventConditionItem
        load_instance = True
        exclude = ("timestamp",)

    id = field_for(EventConditionItem, "id", dump_only=True)
    arguments = Nested(EventConditionArgumentSubmitSchema, many=True)


class EventConditionTrueArgumentSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EventItemTrueArgument
        load_instance = True
        exclude = ("timestamp",)

    id = field_for(EventItemTrueArgument, "id", dump_only=True)


class EventTrueSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EventConditionTrueItem
        load_instance = True
        exclude = ("timestamp",)

    id = field_for(EventConditionTrueItem, "id", dump_only=True)
    arguments = Nested(EventConditionTrueArgumentSubmitSchema, many=True)


class EventConditionFalseArgumentSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EventItemFalseArgument
        load_instance = True
        exclude = ("timestamp",)

    id = field_for(EventItemFalseArgument, "id", dump_only=True)


class EventFalseSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = EventConditionFalseItem
        load_instance = True
        exclude = ("timestamp",)

    id = field_for(EventConditionFalseItem, "id", dump_only=True)
    arguments = Nested(EventConditionFalseArgumentSubmitSchema, many=True)


class EventSubmitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GameEvent
        load_instance = True
        exclude = ("timestamp",)
        include_fk = True

    id = field_for(GameEvent, "id", dump_only=True)
    conditions = Nested(EventConditionSubmitSchema, many=True)
    true_part = Nested(EventTrueSubmitSchema, many=True)
    false_part = Nested(EventFalseSubmitSchema, many=True)
