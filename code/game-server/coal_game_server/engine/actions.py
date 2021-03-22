from coal_game_server.models.game import Game, GameProperty
from .common import get_character, update_character_properties, get_room


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


def look(command):
  """ Show the description of the character's current room
  """
  c = get_character(command.character_id)
  r = get_room(c['location'])
  
  # header
  command.buffer.append(r['title'].capitalize())

  # description
  command.buffer.append(f"\t{r['description']}")

  # exits
  if r['exits']:
    exit_list = ", ".join(e['direction'] for e in r['exits'])
    command.buffer.append(f"\nYou see exits to the {exit_list}.")

  # items