from contextlib import contextmanager

import attr

from coal_public_api_client import Configuration, ApiClient
from coal_public_api_client.api.game_api import GameApi
from coal_public_api_client.api.player_api import PlayerApi
from coal_public_api_client.api.character_api import CharacterApi
from coal_public_api_client.api.turn_api import TurnApi
from coal_public_api_client.api.room_api import RoomApi
from coal_public_api_client.api.exit_api import ExitApi


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
            yield GameApi(api_client)

    @contextmanager
    def player_api(self):
        with ApiClient(self.config) as api_client:
            yield PlayerApi(api_client)

    @contextmanager
    def character_api(self):
        with ApiClient(self.config) as api_client:
            yield CharacterApi(api_client)

    @contextmanager
    def turn_api(self):
        with ApiClient(self.config) as api_client:
            yield TurnApi(api_client)

    @contextmanager
    def room_api(self):
        with ApiClient(self.config) as api_client:
            yield RoomApi(api_client)

    @contextmanager
    def exit_api(self):
        with ApiClient(self.config) as api_client:
            yield ExitApi(api_client)

    @classmethod
    def from_config(cls, incoming_config):
        config = Configuration(incoming_config.url)
        game = incoming_config.game
        player = incoming_config.player
        character = incoming_config.character
        return cls(config, game, player, character)
