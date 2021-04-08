"""
  Broker requests from Discord -> COAL

  https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-python
  https://discordpy.readthedocs.io/en/stable/

"""
import json
import logging
import os

from discord.ext import commands
import requests
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
from dotenv import load_dotenv

load_dotenv()

SERVER = os.environ.get("COAL_API_SERVER", "http://localhost:8000/v1")
GUILD = [int(os.getenv("DISCORD_GUILD_ID"))]
CONFIG = os.environ.get("DISCORD_CONFIG_FILEPATH", "config.json")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord")


try:
    with open(CONFIG) as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            config = {}
except FileNotFoundError:
    config = {}


client = commands.Bot(command_prefix="?")


slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_command_error(ctx, error):
    # basically, all input will be run through here as a fallthrough
    msg = "I'm sorry, but I don't think you're playing a game right now."
    pid = str(ctx.message.author.id)
    if pid in config:
        c = config[pid]
        gid = c["game"]
        cid = c["character"]
        rv = requests.post(
            f"{SERVER}/game/{gid}/character/{cid}/turn",
            json={"command": ctx.message.content[1:]},
        )
        rv.raise_for_status()
        msg = rv.json()["text"]
    await ctx.send(msg)


@slash.slash(name="games", guild_ids=GUILD, description="List all available COAL games")
async def _games(ctx):
    rv = requests.get(f"{SERVER}/game")
    rv.raise_for_status()
    titles = ", ".join(g["title"] for g in rv.json())
    await ctx.send(f"You can play: {titles}")


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


@slash.slash(
    name="play",
    guild_ids=GUILD,
    description="Play a COAL game",
    options=[
        create_option(
            name="game",
            description="Name of COAL game to play",
            option_type=3,
            required=True,
        ),
        create_option(
            name="character",
            description="Name of COAL character in that game to play",
            option_type=3,
            required=True,
        ),
    ],
)
async def _play(ctx, game, character):
    uid = str(ctx.author_id)
    # first, check that the requested game exists
    gid = _get_game_id(game)
    if not gid:
        await ctx.send(f"I'm sorry, but I can't play '{game}'")
        return

    # next, see if the player exists
    pid = _get_player_id(uid)
    if not pid:
        await ctx.send(f"Looks like you're new; signing you up")
        pid = _create_player(uid)

    # last, cache or create the character
    cid = _get_character_id(pid)
    if not cid:
        await ctx.send(f"Creating '{character}' in '{game}' for you.")
        cid = _create_character(gid, pid, character)

    # save out everything
    config[uid] = {"game": gid, "player": pid, "character": cid}
    with open(CONFIG, "w") as f:
        json.dump(config, f)

    # Run an empty command for any first-turn things
    rv = requests.post(
        f"{SERVER}/game/{gid}/character/{cid}/turn", json={"command": ""}
    )
    rv.raise_for_status()
    await ctx.send(rv.json()["text"])


def main():
    client.run(os.getenv("DISCORD_TOKEN"))
