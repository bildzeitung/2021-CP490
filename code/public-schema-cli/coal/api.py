from contextlib import contextmanager

import attr

from coal_public_api_client import Configuration, ApiClient
from coal_public_api_client.api.default_api import DefaultApi


@attr.s
class Api:
    """Wrapper for using the API Client

    - contains configuration
    - makes use a little easier with a contextmanager
    """

    config = attr.ib()
    game = attr.ib()
    player = attr.ib()
    character = attr.ib()

    @contextmanager
    def api(self):
        with ApiClient(self.config) as api_client:
            yield DefaultApi(api_client)

    @classmethod
    def from_config(cls, incoming_config):
        config = Configuration(incoming_config.url)
        game = incoming_config.game
        player = incoming_config.player
        character = incoming_config.character
        return cls(config, game, player, character)
