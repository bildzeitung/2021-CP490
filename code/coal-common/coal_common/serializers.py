from marshmallow_sqlalchemy.fields import Nested
from marshmallow import missing


class AttributeSerializer(Nested):
    """
        Attributes come in as:
            { "key1": "value1",
              "key2": "value2",
              ...
            }
        
        but, in the database, each attribute is a table row, and is
        represented as:
            [ { "title": "key1", "value": "value1"},
              { "title": "key2", "value": "value2"},
              { "title": "key3", "value": "value3"},
              ...
            ]

        This class manages the translation.
    """
    def serialize(self, attr, obj, accessor=None):
        return {p.title: p.value for p in obj.attributes}

    def deserialize(self, value, attr, data, **kwargs):
        if value != missing:
            value = [ {"title":k, "value":v} for k, v in value.items() ] 
        return super().deserialize(value, attr=attr, data=data, **kwargs)