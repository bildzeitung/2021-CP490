from coal_game_server.models.game import TurnDetailSchema
from ....models import TurnSubmitSchema, TurnStatusEnum
from ....config import db


def post(game_id, character_id, body):
  # process command
  body["status"] = TurnStatusEnum.OK.name
  body["game_id"] = game_id
  body["character_id"] = character_id
  body["text"] = "OUTPUT"

  # serialize into DB
  t = TurnSubmitSchema()
  new_turn = t.load(body, session=db.session)
  db.session.add(new_turn)
  db.session.commit()

  # return output
  return TurnDetailSchema().dump(new_turn), 201
