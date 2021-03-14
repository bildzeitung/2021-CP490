import pytest

from coal_content_server.models.room import RoomExit, Room


def test_post_of_two_rooms(testapp):
    """Validate that a post of two rooms with an exit works"""
    room1 = {
        "title": "first",
        "description": "first room",
        "exits": [],
        "game_id": "00000000-0000-0000-0000-000000000000",
    }
    rv1 = testapp.post("/v1/room", json=room1)
    assert rv1.status_code == 200
    assert rv1.json["id"]

    room2 = {
        "title": "second",
        "description": "second room",
        "exits": [{"to_room_id": rv1.json["id"], "direction": "north"}],
        "game_id": "00000000-0000-0000-0000-000000000000",
    }
    rv = testapp.post("/v1/room", json=room2)
    assert rv.status_code == 200
    assert len(rv.json["exits"]) == 1
    assert rv.json["exits"][0]["to_room_id"] == rv1.json["id"]


@pytest.fixture
def room(testapp):
    def make_room(title):
        room = {
            "title": title,
            "description": "Room",
            "exits": [],
            "game_id": "00000000-0000-0000-0000-000000000000",
        }
        rv = testapp.post("/v1/room", json=room)
        assert rv.status_code == 200
        assert rv.json["id"]
        return rv.json

    return make_room


def test_delete_of_room_with_exits(testapp, room):
    """
    r1 -(north)-> r2
    r1 <-(south)- r2

    Removing r2 should remove the child DB row in RoomExits
    """
    r1 = room("room1")
    r2 = room("room2")

    exit = {"to_room_id": r2["id"], "direction": "north"}
    rv = testapp.post(f'/v1/room/{r1["id"]}/exit', json=exit)
    assert rv.status_code == 200
    assert rv.json["id"]

    exit = {"to_room_id": r1["id"], "direction": "south"}
    rv = testapp.post(f'/v1/room/{r2["id"]}/exit', json=exit)
    assert rv.status_code == 200
    assert rv.json["id"]

    # only 2 room exits were added, so validate
    assert Room.query.count() == 2
    assert RoomExit.query.count() == 2

    rv = testapp.delete(f'/v1/room/{r2["id"]}')
    assert rv.status_code == 204
    # no exits are valid now, so validate that they are removed
    assert Room.query.count() == 1
    assert RoomExit.query.count() == 0
