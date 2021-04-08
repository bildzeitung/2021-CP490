import pytest


def test_post_of_two_rooms(testapp):
    """Validate that a post of two rooms with an exit works"""
    room1 = {
        "title": "first",
        "description": "first room",
        "game_id": "00000000-0000-0000-0000-000000000000",
    }
    rv1 = testapp.post("/v1/room", json=room1)
    assert rv1.status_code == 201
    assert rv1.json["id"]

    room2 = {
        "title": "second",
        "description": "second room",
        "game_id": "00000000-0000-0000-0000-000000000000",
    }
    rv = testapp.post("/v1/room", json=room2)
    assert rv.status_code == 201


@pytest.fixture
def room(testapp):
    def make_room(title):
        room = {
            "title": title,
            "description": "Room",
            "game_id": "00000000-0000-0000-0000-000000000000",
        }
        rv = testapp.post("/v1/room", json=room)
        assert rv.status_code == 201
        assert rv.json["id"]
        return rv.json

    return make_room
