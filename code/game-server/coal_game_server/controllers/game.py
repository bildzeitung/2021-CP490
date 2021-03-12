from flask import make_response, abort
from ..config import db
from ..models import Game, GameSchema, GameSubmitSchema, GameDetailSchema

def search():
  games = Game.query.all()
  return GameSchema(many=True).dump(games)

def get(game_id):
  game = Game.query.filter(Game.id == game_id).one_or_none()
  if not game:
    abort(404, f"Could not find game {game_id}")
  
  return GameDetailSchema().dump(game)

def post(body):
  title = body.get("title")
  existing_game = (
    Game.query.filter(Game.title == title).one_or_none()
  )

  if existing_game is not None:
    abort(409, f"A game with this title: '{title}' already exists.")

  schema = GameSubmitSchema()
  new_game = schema.load(body, session=db.session)
  db.session.add(new_game)
  db.session.commit()

  data = schema.dump(new_game)

  return data, 200


def put():
  pass


def delete(game_id):
  game = Game.query.filter(Game.id == game_id).one_or_none()
  if not game:
    abort(404, f"Could not find game {game_id}")
  
  db.session.delete(game)
  db.session.commit()

  return make_response(f"Deleted {game_id}", 200)