from .common import get_character


def has_key(command, obj, key):
    """Does the player have the given key as a property?"""
    if obj == "character":
        o = get_character(command.character_id)
    
    return key in o["attributes"]
