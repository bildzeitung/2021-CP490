from coal_game_server.models.game import TurnDetailSchema
from ....models import TurnSubmitSchema
from ....config import db
from ....engine import GameCommand


def post(game_id, character_id, body):
    # process command
    gc = GameCommand(game_id, character_id, body["command"])

    # serialize into DB
    t = TurnSubmitSchema()
    r = gc.result
    new_turn = t.load(body | r, session=db.session)

    db.session.add(new_turn)
    db.session.commit()

    # return output
    return TurnDetailSchema().dump(new_turn), 201
