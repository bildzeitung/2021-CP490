from contextlib import contextmanager

import attr

from coal_public_api_client import Configuration, ApiClient
from coal_public_api_client.api.default_api import DefaultApi
from coal_public_api_client.exceptions import ApiAttributeError, ApiException
from coal_public_api_client.model.game_submit import GameSubmit


@contextmanager
def defaultapiclient(config):
  with ApiClient(config) as api_client:
    yield DefaultApi(api_client)

@attr.s
class MetaRunner:
  config = attr.ib()
  state = attr.ib()

  def run(self, command):
    (cmd, *args) = command.split()

    config = Configuration(host=self.config.url)
    if cmd == 'create':  # create a new game
      if not args:
        print("Need more than just a /create")
        return
      with defaultapiclient(config) as api:
        try:
          game = GameSubmit(title=args[0], description=" ".join(args[1:]))
          rv = api.game_post(game)
          print(rv)
        except ApiAttributeError as e:
          print(f"Need a description! {e}")
        except ApiException as e:
          print(f"Cannot create |{args[0]}|: {e.body}")
    elif cmd == "delete":  # Delete a game
      with ApiClient(config) as api_client:
        name = args[0]
        api = DefaultApi(api_client)
        rv = api.game_get()
        # Delete the game, if we have the title right
        for game in rv.value:
          if game.title == name:
            rv = api.game_game_id_delete(game.id)
            print("Game deleted.")
            return
        print(f"Game {name} not found!")
    elif cmd == "list":  # list all games
      with defaultapiclient(config) as api:
        if args:
          rv = api.game_get()
          # Delete the game, if we have the title right
          for game in rv.value:
            if game.title == args[0]:
              rv = api.game_game_id_get(game.id)
              print(f"ID   : {rv.id}:\nTITLE: {rv.title}\nDESC : {rv.description}")
              return
          print(f"Cannot find |{args[0]}|")
          return
        rv = api.game_get()
        for game in rv.value:
          print(f"{game.id}: {game.title}")
    elif cmd == "join":  # join a game on the server with the player
      with ApiClient(config) as api_client:
        api = DefaultApi(api_client)
        rv = api.game_get()
        for game in rv.value:
          if game.title == self.config.game:
            self.state['game_id'] = game.id
            print(f"Joined {game.title}")
            return
        print(f"Could not find '{self.config.game}' on server {self.config.url}")
