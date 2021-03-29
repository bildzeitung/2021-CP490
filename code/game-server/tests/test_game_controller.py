import pytest
from coal_game_server.models.game import (
  Game,
  GameAttribute
  )

#
# x GET /game
# x POST /game
#   GET /game/{game_id}
#   PUT /game/{game_id}
#   DELETE /game/{game_id}
#
#   POST /game/{game_id}/character/{character_id}/turn
#   POST /game/{game_id}/player/{player_id}/character
#
#   GET /game/{game_id}/event
#   POST /game/{game_id}/event
#   GET /game/{game_id}/event/{event_id}
#   PUT /game/{game_id}/event/{event_id}
#   DELETE /game/{game_id}/event/{event_id}

#
# POST /game
#
def test_post_game(testapp):
  doc = {
  "title": "title-string",
  "description": "description-string",
  "properties": {
    "additionalProp1": "string1",
    "additionalProp2": "string2",
    "additionalProp3": "string3"
    }
  }
  rv = testapp.post(f"/v1/game", json=doc)
  assert rv.status_code == 201

  assert rv.json["id"]
  doc["id"] = rv.json["id"]  # add the DB-provided ID
  assert doc == rv.json

  assert Game.query.count() == 1
  assert GameAttribute.query.count() == 3


@pytest.fixture()
def game(session):
  new_game = Game(title="title-string", description="description-string", properties=[GameAttribute(title="starting-room", value="room-id")])
  session.add(new_game)
  session.commit()
  yield new_game

#
# GET /game
#
def test_get_game(testapp, game):
  rv = testapp.get("/v1/game")
  assert rv.status_code == 200
  assert Game.query.count() == len(rv.json)

  g = rv.json[0]
  assert str(game.id) == g["id"]
  assert game.title == g["title"]

