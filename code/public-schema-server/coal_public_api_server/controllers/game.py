from typing import Text
import requests
from flask import abort


def search():
  pass

def post(body):
  body["id"] = ""

  # get a list of games
  try:
    rv = requests.get("http://localhost:8100/v1/game")
    rv.raise_for_status()
  except Exception as e:
    abort(500, f"Could not contact game server: {str(e)}")

  # check for duplicate titles
  title = body.get("title")
  for g in rv.json():
    if g["title"] == title:
      abort(409, f"Already have a game with the title |{title}|")
  
  # submit request to game server
  try:
    rv = requests.post("http://localhost:8100/v1/game", json=body)
    rv.raise_for_status()
  except Exception as e:
    abort(500, f"Bad POST: {str(e)}")
  
  return rv.json(), 200


def put():
  pass