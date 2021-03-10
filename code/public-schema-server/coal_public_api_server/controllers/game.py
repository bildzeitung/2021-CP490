import requests
from flask import abort, make_response, current_app


def search():
    try:
        rv = requests.get(f"{current_app.config['GAME_SERVER_URL']}/game")
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Could not contact game server: {str(e)}")

    return rv.json(), 200


def post(body):
    body["id"] = ""

    # get a list of games
    try:
        rv = requests.get(f"{current_app.config['GAME_SERVER_URL']}/game")
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Could not contact game server: {str(e)}")

    # check for duplicate titles
    title = body.get("title")
    for g in rv.json():
        if g["title"] == title:
            abort(409, f"Already have a game with the title |{title}|")

    # submit request to game server
    try:
        rv = requests.post(f"{current_app.config['GAME_SERVER_URL']}/game", json=body)
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Bad POST: {str(e)}")

    return rv.json(), 200


def put():
    pass


def delete(id):
    try:
        rv = requests.delete(f"{current_app.config['GAME_SERVER_URL']}/game/{id}")
        rv.raise_for_status()
    except Exception as e:
        abort(500, f"Game server problem: {str(e)}")

    return make_response(rv.content, 200)
