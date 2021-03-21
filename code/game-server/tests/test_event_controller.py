import pytest

from coal_game_server.models.game import (
    EventConditionTrueItem,
    GameEvent,
    EventConditionItem,
    EventItemConditionArgument,
    EventItemTrueArgument,
    EventItemFalseArgument,
    EventConditionFalseItem,
)


@pytest.fixture
def game(testapp):
    def make_game(title):
        game = {
            "title": title,
            "description": f"Game {title}",
        }
        rv = testapp.post("/v1/game", json=game)
        assert rv.status_code == 201
        assert rv.json["id"]
        return rv.json

    return make_game


def test_post_of_event(testapp, game):
    """Validate that a post of event works"""
    g = game("mud")
    event = {
        "command": "GO !DIRECTION",
        "conditions": [
            {"primitive": "first", "arguments": ["first-string1", "first-string2"]},
            {"primitive": "second", "arguments": ["second-string1", "second-string2"]},
        ],
        "true_part": [
            {"primitive": "true-first", "arguments": ["true-first-1", "true-first-2"]}
        ],
        "false_part": [
            {
                "primitive": "false-first",
                "arguments": ["false-first-1", "false-first-2"],
            }
        ],
    }
    rv1 = testapp.post(f"/v1/game/{g['id']}/event", json=event)
    assert rv1.status_code == 201
    assert rv1.json["id"]

    print(rv1.json)
    assert GameEvent.query.count() == 1
    assert EventConditionItem.query.count() == 2
    assert EventItemConditionArgument.query.count() == 4

    assert EventConditionTrueItem.query.count() == 1
    assert EventItemTrueArgument.query.count() == 2

    assert EventConditionFalseItem.query.count() == 1
    assert EventItemFalseArgument.query.count() == 2


@pytest.fixture
def event(testapp, game):
    g = game("mud")
    event = {
        "command": "GO !DIRECTION",
        "conditions": [
            {"primitive": "first", "arguments": ["first-string1", "first-string2"]},
            {"primitive": "second", "arguments": ["second-string1", "second-string2"]},
        ],
        "true_part": [
            {"primitive": "true-first", "arguments": ["true-first-1", "true-first-2"]}
        ],
        "false_part": [
            {
                "primitive": "false-first",
                "arguments": ["false-first-1", "false-first-2"],
            }
        ],
    }
    rv = testapp.post(f"/v1/game/{g['id']}/event", json=event)
    assert rv.status_code == 201
    return rv.json


def test_delete_of_event(testapp, event):
    rv = testapp.delete(f"/v1/game/{event['game_id']}/event/{event['id']}")
    assert rv.status_code == 204

    assert GameEvent.query.count() == 0
    assert EventConditionItem.query.count() == 0
    assert EventItemConditionArgument.query.count() == 0

    assert EventConditionTrueItem.query.count() == 0
    assert EventItemTrueArgument.query.count() == 0

    assert EventConditionFalseItem.query.count() == 0
    assert EventItemFalseArgument.query.count() == 0
