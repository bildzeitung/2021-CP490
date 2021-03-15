import requests
from flask import current_app, abort


def search():
  pass

def get():
  pass

def delete():
  pass

def post(game_id, room_id, body):
  try:
      rv = requests.post(f"{current_app.config['CONTENT_SERVER_URL']}/room/{room_id}/exit", json=body)
      rv.raise_for_status()
  except Exception:
      abort(rv.status_code, rv.json()['detail'])

  return rv.json(), 201
