from coal_game_server.models.game import EventItemFalseArgument, Game, GameProperty
from .common import get_character, update_character_properties


def set_key(command, key, value):
  """ Set a character key to a value
  """
  c = get_character(command.character_id)
  c["properties"][key] = value

  update_character_properties(c)


def message(command, key):
  """ Add a message to the buffer
  """
  g : Game = Game.query.filter(Game.id == command.game_id).one_or_none()
  p : GameProperty
  for p in g.properties:
    if p.title == key:
      command.buffer.append(p.value)
      return