import attr

from coal_public_api_client import Configuration, ApiClient
from coal_public_api_client.api.default_api import DefaultApi
from coal_public_api_client.model.game import Game

@attr.s
class MetaRunner:
  config = attr.ib()

  def run(self, command):
    (cmd, *args) = command.split()

    config = Configuration(host=self.config.url)
    if cmd == 'create':
      with ApiClient(config) as api_client:
        api = DefaultApi(api_client)
        game = Game(id="", title=args[0], description=" ".join(args[1:]))
        rv = api.game_post(game)
        print(rv)
    elif cmd == "delete":
      with ApiClient(config) as api_client:
        name = args[0]
        api = DefaultApi(api_client)
        rv = api.game_get()
        # Delete the game, if we have the title right
        for game in rv.value:
          if game.title == name:
            rv = api.game_id_delete(game.id)
            print("Game deleted.")
            return
        print(f"Game {name} not found!")
    elif cmd == "list":
      with ApiClient(config) as api_client:
        api = DefaultApi(api_client)
        rv = api.game_get()
        for game in rv.value:
          print(f"{game.id}: {game.title}")
