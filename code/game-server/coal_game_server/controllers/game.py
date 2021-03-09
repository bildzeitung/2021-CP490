from flask import make_response, abort
from ..config import db
from ..models import Game, GameSchema

def search():
  games = Game.query.all()
  return GameSchema(many=True).dump(games)


def post(body):
  if body.get("id") != "":
    abort(
      409, "Please pass and empty id"
    )
  del body["id"]

  title = body.get("title")
  existing_game = (
    Game.query.filter(Game.title == title).one_or_none()
  )

  if existing_game is not None:
    abort(409, f"A game with this title: '{title}' already exists.")

  schema = GameSchema()
  new_game = schema.load(body, session=db.session)
  db.session.add(new_game)
  db.session.commit()

  data = schema.dump(new_game)

  return data, 200


def put():
  pass