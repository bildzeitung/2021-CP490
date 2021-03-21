import attr

from coal_public_api_client.model.turn_submit import TurnSubmit

@attr.s
class GameRunner:
    """Runner for game play commands"""

    api = attr.ib()
    state = attr.ib()

    def run(self, command):
        if not (self.state.game and self.state.character):
            print("Please /join a game before trying to play!")
            return

        with self.api.api() as api:
          body = TurnSubmit(command=command)
          try:
            rv = api.game_game_id_character_character_id_turn_post(self.state.game, self.state.character, body)
          except Exception as e:
            print(f"Did not run turn:\n\t{e}")
            return
        if rv['text']:
          print(rv['text'])