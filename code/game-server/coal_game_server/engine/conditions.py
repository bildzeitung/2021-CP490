from .common import get_character

def has_key(command, key):
  """ Does the player have the given key as a property?
  """
  c = get_character(command.character_id)
  return key in c['properties']
