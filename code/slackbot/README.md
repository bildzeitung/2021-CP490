# Slack Integration

## Deployment

Create a `.env` file with:

```
#
# Bot integration
#
SLACK_SIGNING_SECRET=f0000000000000000000000000000009
SLACK_BOT_TOKEN=xoxb-0000000000000-...
#
# COAL details
CONFIG_FILEPATH=/config/slackbot.cache
COAL_API_SERVER=http://localhost:8000/v1
```

The `CONFIG_FILEPATH` is where the player (user) cache is stored.

Point `COAL_API_SERVER` to the COAL instance to use.


## Integration

The following commands are listened for:

| Command                   | Description |
|---------------------------|-------------|
| /games                    | List all games on COAL instance |
| /play  <game> <character> | Play <game>. Use <character> (create <character> if necessary)|

Regular DMs are listened to as well, and are passed to:

```
POST /{SERVER}/game/{gid}/character/{cid}/turn"
```

where:
* **gid**: Game identifier resolved from `/play <game>`
* **cid**: Character identifier from `/play <game> <character>`

The data for the POST is a JSON document:

```
{
  "command": <user message>
}
```

The output from COAL in responses to the command is sent back as a chat message.