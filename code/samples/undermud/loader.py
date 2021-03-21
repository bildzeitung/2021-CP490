#!/usr/bin/env python
"""
  Load content for UnderMud
"""
import json
from pathlib import Path

import requests

API_SERVER = "http://localhost:8000/v1"
GAME_SERVER = "http://localhost:8100/v1"
# CONTENT_SERVER = "http://localhost:8200/v1"

EVENT_FILE = Path(__file__).parent / "events.json"
ROOMS_FILE = Path(__file__).parent / "rooms.json"
EXITS_FILE = Path(__file__).parent / "exits.txt"


def create_game():
  game = {
    "title": "undermud",
    "description": "MUD for all"
  }
  rv = requests.post(f"{GAME_SERVER}/game", json=game)
  rv.raise_for_status()
  return rv.json()["id"]


def create_event(game_id, event):
  rv = requests.post(f"{GAME_SERVER}/game/{game_id}/event", json=event)
  rv.raise_for_status()


def create_room(game_id, room):
  rv = requests.post(f"{API_SERVER}/game/{game_id}/room", json=room)
  rv.raise_for_status()
  return rv.json()["id"]


def create_exit(game_id, rooms, from_room, _, to_room, direction):
  doc = {
    "to_room_id": rooms[to_room],
    "direction": direction,
  }
  rv = requests.post(f"{API_SERVER}/game/{game_id}/room/{rooms[from_room]}/exit", json=doc)
  rv.raise_for_status()


def create_properties(game_id, rooms):
  doc = {
    "properties": {
      "starting-room": rooms["meadow"],
      "starting-message": "Welcome to UnderMUD!\n\tBe nice and enjoy.",
    }
  }
  rv = requests.put(f"{API_SERVER}/game/{game_id}", json=doc)
  rv.raise_for_status()


def main():
  game_id = create_game()
  print(f"Game id: {game_id}")

  with EVENT_FILE.open() as f:
    events = json.load(f)
    for e in events:
      create_event(game_id, e)

  with ROOMS_FILE.open() as f:
    rooms = { r["title"] : create_room(game_id, r) for r in json.load(f)}

  with EXITS_FILE.open() as f:
    for line in f:
      print(line)
      create_exit(game_id, rooms, *line.strip().split())

  create_properties(game_id, rooms)

  rv = requests.get(f"{GAME_SERVER}/game/{game_id}/event")
  rv.raise_for_status()
  print (json.dumps(rv.json(), indent=4, sort_keys=True))


if __name__ == "__main__":
  main()