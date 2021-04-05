"""
  Broker requests from Discord -> COAL

  https://realpython.com/how-to-make-a-discord-bot-python/#how-to-make-a-discord-bot-in-python
  https://discordpy.readthedocs.io/en/stable/

"""
import os

import discord
import requests
from discord_slash import SlashCommand
from dotenv import load_dotenv

load_dotenv()

SERVER = "http://localhost:8000/v1"
GUILD = [int(os.getenv("DISCORD_GUILD_ID"))]

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(
    client, sync_commands=True
)  # Declares slash commands through the client.


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )


@slash.slash(name="games", guild_ids=GUILD, description="List all available COAL games")
async def _games(ctx):
    rv = requests.get(f"{SERVER}/game")
    rv.raise_for_status()
    titles = ", ".join(g["title"] for g in rv.json())
    await ctx.send(f"You can play: {titles}")


def main():
    client.run(os.getenv("DISCORD_TOKEN"))
