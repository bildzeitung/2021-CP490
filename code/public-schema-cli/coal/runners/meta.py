from contextlib import contextmanager

import attr

from coal_public_api_client import Configuration, ApiClient
from coal_public_api_client.api.default_api import DefaultApi
from coal_public_api_client.exceptions import ApiAttributeError, ApiException, ServiceException
from coal_public_api_client.model.game_submit import GameSubmit


def help():
  commands = {
    "list": "Display a list of games",
    "list <title>": "Display details for a particular one",
    "create <title> <description>": "Create a new game",
    "delete <title>": "Delete a game entirely (careful!)",
    "join": "Join your configured game and character",
  }
  print("Available Metacommands\n")
  for k, v in commands.items():
    print(f"{k}: {v}")


@attr.s
class MetaRunner:
  config = attr.ib()
  game = attr.ib()
  state = attr.ib()

  @contextmanager
  def defaultapiclient(self):
    with ApiClient(self.config) as api_client:
      yield DefaultApi(api_client)

  @classmethod
  def from_config(cls, incoming_config, state):
    config = Configuration(incoming_config.url)
    game = incoming_config.game
    return cls(config, game, state)

  def run(self, command):
    (cmd, *args) = command.split()

    if cmd == "help":
      help()
    elif cmd == 'create':  # create a new game
      if not args:
        print("Need more than just a /create")
        return
      with self.defaultapiclient() as api:
        try:
          game = GameSubmit(title=args[0], description=" ".join(args[1:]))
          rv = api.game_post(game)
          print(rv)
        except ApiAttributeError as e:
          print(f"Need a description! {e}")
        except ApiException as e:
          print(f"Cannot create |{args[0]}|: {e.body}")
    elif cmd == "delete":  # Delete a game
      with self.defaultapiclient() as api:
        name = args[0]
        rv = api.game_get()
        # Delete the game, if we have the title right
        for game in rv.value:
          if game.title == name:
            rv = api.game_game_id_delete(game.id)
            print("Game deleted.")
            return
        print(f"Game {name} not found!")
    elif cmd == "list":  # list all games
      with self.defaultapiclient() as api:
        if args:
          try:
            rv = api.game_get()
          except ServiceException as e:
            print("Problem with API server (is the game server up?)")
            return
          # Delete the game, if we have the title right
          for game in rv.value:
            if game.title == args[0]:
              rv = api.game_game_id_get(game.id)
              print(f"ID   : {rv.id}:\nTITLE: {rv.title}\nDESC : {rv.description}")
              return
          print(f"Cannot find |{args[0]}|")
          return
        try:
          rv = api.game_get()
          for game in rv.value:
            print(f"{game.id}: {game.title}")
        except ServiceException:
          print("Problem with API server (is the game server up?)")
    elif cmd == "join":  # join a game on the server with the player
      with self.defaultapiclient() as api:
        rv = api.game_get()
        for game in rv.value:
          if game.title == self.game:
            self.state['game_id'] = game.id
            print(f"Joined {game.title}")
            return
        print(f"Could not find '{self.game}' on server")
