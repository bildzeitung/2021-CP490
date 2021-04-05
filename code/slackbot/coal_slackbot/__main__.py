"""
  Broker requests from Slack -> COAL

  Slack commands:
    /play
	- create character, if necessary, and cache the context
    /games
	- list available

"""
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from slack_bolt import App


SERVER = "http://localhost:8000/v1"
CONFIG = Path("config.json")

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

config = None


@app.event("message")
def received_im(event, say):
    if event["user"] in config:
        c = config[event["user"]]
        gid = c["game"]
        cid = c["character"]
        rv = requests.post(
            f"{SERVER}/game/{gid}/character/{cid}/turn", json={"command": event["text"]}
        )
        rv.raise_for_status()
        say(rv.json())
        return
    say("I'm sorry, but I don't think you're playing a game right now.")


def _get_player_id(uid):
    rv = requests.get(f"{SERVER}/player")
    rv.raise_for_status()
    for r in rv.json():
        if r["title"] == uid:
            return r["id"]


def _get_character_id(pid):
    rv = requests.get(f"{SERVER}/player/{pid}/character")
    rv.raise_for_status()
    for r in rv.json():
        if r["title"] == pid:
            return r["id"]


def _get_game_id(gid):
    rv = requests.get(f"{SERVER}/game")
    rv.raise_for_status()
    for r in rv.json():
        if r["title"] == gid:
            return r["id"]


def _create_player(uid):
    rv = requests.post(f"{SERVER}/player", json={"title": uid})
    rv.raise_for_status()
    return rv.json()["id"]


def _create_character(gid, pid, name):
    rv = requests.post(
        f"{SERVER}/game/{gid}/player/{pid}/character", json={"title": name}
    )
    rv.raise_for_status()
    return rv.json()["id"]


@app.command("/play")
def play(ack, say, command):
    ack()
    cmd = command.get("text", "")
    args = [x.strip() for x in cmd.split()]
    if len(args) < 2:
        say(f"I need a <game> and a <player>, not '{cmd}'")
        return
    # use user_id as the player
    uid = command["user_id"]

    # first, check that the requested game exists
    gid = _get_game_id(args[0])
    if not gid:
        say(f"I'm sorry, but I can't play '{args[0]}'")
        return

    # next, see if the player exists
    pid = _get_player_id(uid)
    if not pid:
        say(f"Looks like you're new; signing you up")
        pid = _create_player(uid)

    # last, cache or create the character
    cid = _get_character_id(pid)
    if not cid:
        say(f"Creating '{args[1]}' in '{args[0]}' for you.")
        cid = _create_character(gid, pid, args[1])

    # save out everything
    config[uid] = {"game": gid, "player": pid, "character": cid}
    with os.environ.get("CONFIG_FILEPATH", CONFIG).open("w") as f:
        json.dump(config, f)

    # Run an empty command for any first-turn things
    rv = requests.post(
        f"{SERVER}/game/{gid}/character/{cid}/turn", json={"command": ""}
    )
    rv.raise_for_status()
    say(rv.json())


@app.command("/games")
def list_games(ack, say, command):
    ack()
    rv = requests.get(f"{SERVER}/game")
    rv.raise_for_status()
    titles = ", ".join(g["title"] for g in rv.json())
    say(f"You can play: {titles}")


def main():
    load_dotenv()
    SERVER = os.environ.get("COAL_API_SERVER", SERVER)
    try:
        with os.environ.get("CONFIG_FILEPATH", CONFIG).open() as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                config = {}
    except FileNotFoundError:
        config = {}
    app.start(port=int(os.environ.get("PORT", 3000)))
