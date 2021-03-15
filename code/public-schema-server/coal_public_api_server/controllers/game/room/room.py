import requests
from flask import current_app, abort, make_response


def search(game_id):
  try:
      rv = requests.get(f"{current_app.config['CONTENT_SERVER_URL']}/room?game_id={game_id}")
      rv.raise_for_status()
  except Exception as e:
      abort(500, f"Could not contact content server: {str(e)}")

  return rv.json(), 200


def post(game_id, body):
  body['game_id'] = game_id
  try:
      rv = requests.post(f"{current_app.config['CONTENT_SERVER_URL']}/room", json=body)
      rv.raise_for_status()
  except Exception:
      abort(rv.status_code, rv.json()['detail'])

  return rv.json(), 201


def get(game_id, room_id):
  try:
      rv = requests.get(f"{current_app.config['CONTENT_SERVER_URL']}/room/{room_id}")
      rv.raise_for_status()
  except Exception:
      abort(rv.status_code, rv.json()['detail'])

  return rv.json(), 200


def put():
  pass


def delete(game_id, room_id):
  try:
    rv = requests.delete(f"{current_app.config['CONTENT_SERVER_URL']}/room/{room_id}")
  except Exception:
    abort(rv.status_code, rv.json()['detail'])

  return make_response(rv.content, 204)