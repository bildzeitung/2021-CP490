#!/usr/bin/env python
"""
  Load content for UnderMud
"""
import json
from pathlib import Path

import attr
import click
import requests
import toml

API_SERVER = ""

EVENT_FILE = Path(__file__).parent / "events.json"
ROOMS_FILE = Path(__file__).parent / "rooms.json"
EXITS_FILE = Path(__file__).parent / "exits.json"
PROPS_FILE = Path(__file__).parent / "properties.json"

GAME_TITLE = "undermud"


@attr.s(auto_attribs=True)
class LoaderConfig:
    API_SERVER: str



def load_config(config_path, profile):
    """Read TOML file from the given path; use the given profile"""
    with open(config_path) as f:
        config = toml.load(f)
    return LoaderConfig(**{k.upper(): v for k, v in config[profile].items()})


def create_game():
    game = {"title": GAME_TITLE, "description": "MUD for all"}
    rv = requests.post(f"{API_SERVER}/game", json=game)
    rv.raise_for_status()
    return rv.json()["id"]


def get_game_id():
    rv = requests.get(f"{API_SERVER}/game")
    rv.raise_for_status()

    for g in rv.json():
        if g["title"] == GAME_TITLE:
            return g["id"]


def create_event(game_id, event):
    rv = requests.post(f"{API_SERVER}/game/{game_id}/event", json=event)
    rv.raise_for_status()


def create_room(game_id, room):
    rv = requests.post(f"{API_SERVER}/game/{game_id}/room", json=room)
    rv.raise_for_status()
    return rv.json()["id"]


def load_exits(game_id, rooms):
    with EXITS_FILE.open() as f:
        exits = json.load(f)

    for e in exits:
        doc = {
            "to_room_id": rooms[e["to"]],
            "direction": e["direction"],
        }
        rv = requests.post(
            f"{API_SERVER}/game/{game_id}/room/{rooms[e['from']]}/exit", json=doc
        )
        rv.raise_for_status()


def create_properties(game_id, rooms):
    with PROPS_FILE.open() as f:
        properties = json.load(f)

    doc = {"properties": {}}
    for k, v in properties.items():
        doc["properties"][k] = eval(f"f'{v}'")

    rv = requests.put(f"{API_SERVER}/game/{game_id}", json=doc)
    rv.raise_for_status()


def clear_events(game_id):
    """Delete all of the Events from a game"""
    rv = requests.get(f"{API_SERVER}/game/{game_id}/event")
    rv.raise_for_status()
    for e in rv.json():
        requests.delete(f"{API_SERVER}/game/{game_id}/event/{e['id']}")
        rv.raise_for_status()


def load_events(game_id):
    """Add all of the events from the file into the game"""
    with EVENT_FILE.open() as f:
        events = json.load(f)
        for e in events:
            create_event(game_id, e)


def load_rooms(game_id):
    with ROOMS_FILE.open() as f:
        rooms = {r["title"]: create_room(game_id, r) for r in json.load(f)}
    return rooms


def get_room_ids(game_id):
    rv = requests.get(f"{API_SERVER}/game/{game_id}/room")
    rv.raise_for_status()
    return {r["title"]: r["id"] for r in rv.json()}


@click.command(help="Data loader for UnderMUD sample game")
@click.option("--events-only", "-e", help="Reload only the Events", is_flag=True)
@click.option(
    "--properties-only", "-p", help="Reload only the game properties", is_flag=True
)
@click.option(
    "--config",
    "-c",
    default=Path().home() / ".config" / "coal-sample-loader.conf",
    show_default=True,
)
@click.option(
    "--profile",
    "-p",
    help="Which server profile to use",
    default="DEFAULT",
    show_default=True,
)
def main(events_only, properties_only, config, profile):
    global API_SERVER
    config = load_config(config, profile)
    API_SERVER = config.API_SERVER

    if events_only:
        game_id = get_game_id()
        clear_events(game_id)
        load_events(game_id)
        return

    if properties_only:
        game_id = get_game_id()
        rooms = get_room_ids(game_id)
        create_properties(game_id, rooms)
        return

    game_id = create_game()
    print(f"Game id: {game_id}")

    load_events(game_id)
    rooms = load_rooms(game_id)
    load_exits(game_id, rooms)

    create_properties(game_id, rooms)


if __name__ == "__main__":
    main()
