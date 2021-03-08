import attr

from coal_public_api_client import Configuration, ApiClient
from coal_public_api_client.api.default_api import DefaultApi
from coal_public_api_client.model.game import Game

@attr.s
class MetaRunner:
  config = attr.ib()

  def run(self, command):
    (cmd, name, *args) = command.split()
    if cmd == 'create':
      with ApiClient(Configuration(host=self.config.url)) as api_client:
        api = DefaultApi(api_client)
        game = Game(id="", title=name, description=" ".join(args))
        rv = api.game_post(game)
        print(rv)
