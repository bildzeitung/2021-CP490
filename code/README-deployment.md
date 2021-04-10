# Deploying COAL

COAL can be deployed as a monolithic Docker container. Download the most recent version of the container from Docker Hub:

https://hub.docker.com/r/bildzeitung/cp490

## Running

Use something like this:

```
#!/bin/bash -ex

sudo docker run --rm \
        -d \
        --name coal \
        -p 8000:8000 \
        -p 3000:3000 \
        -v $(pwd)/dbs:/data \
        -u "$(id -u):$(id -g)" \
        --env-file /home/user/.env \
        coal
```

* port 8000 is the proxy (API) server
* port 3000 is the Slack integration bot
* virtual directory mount /data is for SQLite DBs and slack cache

## Secrets

The `.env` file contains all of the secrets for Slack and Discord integration.
Fields are as follows:

| Field | Mandatory? | Description |
|-------|-------------|
| SLACK_SIGNING_SECRET | Yes | Signing secret for Slack App |
| SLACK_BOT_TOKEN | Yes | e.g. xoxb-... token |
| CONFIG_FILEPATH | No | (default is `config.json`, in container filesystem. Recommend: `/data/slackbot.cache` |
| COAL_API_SERVER | No | Default is: `http://localhost:8000/v1`, which is correct for the server in the container |
| DISCORD_TOKEN | Yes | Discord bot secret |
| DISCORD_GUILD_ID | Yes | Guild ID where bot is active (number) |
| DISCORD_CONFIG_FILEPATH | No | /data/discord.cache (in the container filesystem) |

The `CONFIG_FILEPATH` and `DISCORD_CONFIG_FILEPATH` are caches where player data is cache. When a users messages the Slackboth or talks to the Discord bot, the user ID from those systems creates a player account on COAL automatically.

Sign-up (joining) a game begins, in this case, with the automatic creation of a `character`, as needed.

## Usage

As a player, COAL is most easily used as a Slack bot or via CLI client (TBD: link to coal-cli).

From the content creation side, a loader script (TBD: see example) or CLI client (TBD: to coal-cli) would be best.

API calls can be made to port 8000 on the Docker container:

```
; curl http://localhost:8000/v1/game
[]
```
