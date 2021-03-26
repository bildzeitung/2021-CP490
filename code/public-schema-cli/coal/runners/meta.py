import attr
from tabulate import tabulate

from coal_public_api_client.exceptions import (
    ApiException,
    ServiceException,
)
from coal_public_api_client.model.game_submit import GameSubmit
from coal_public_api_client.model.player_submit import PlayerSubmit
from coal_public_api_client.model.character_submit import CharacterSubmit
from coal_public_api_client.model.turn_submit import TurnSubmit


@attr.s
class MetaRunner:
    api = attr.ib()
    state = attr.ib()

    def _cmd_help(self, *_):
        """Show a list of available commands"""
        print(
            "\n".join(
                [
                    f'/{g.replace("_cmd_", "")}: '
                    + (getattr(self, g).__doc__ or "").strip()
                    for g in dir(self)
                    if g.startswith("_cmd_")
                ]
            )
        )

    def _cmd_list(self, game=None, *_):
        """Display a list of games, or details of a given game"""
        with self.api.api() as api:
            if game:
                try:
                    rv = api.game_get()
                except ServiceException as e:
                    print("Problem with API server (is the game server up?)")
                    return
                for g in rv.value:
                    if g.title == game:
                        rv = api.game_game_id_get(g.id)
                        print(tabulate([k, v] for k, v in rv.to_dict().items()))
                        return
                print(f"Cannot find '{game}'")
                return
            try:
                rv = api.game_get()
                print(tabulate([game.id, game.title] for game in rv.value))
            except ServiceException:
                print("Problem with API server (is the game server up?)")

    def _cmd_create(self, title=None, *description):
        """Add a new game to the server"""
        if not title:
            print("Need more than just a /create")
            return

        if not description:
            print("Need a description along with the name")
            return

        with self.api.api() as api:
            try:
                game = GameSubmit(title=title, description=" ".join(description))
                rv = api.game_post(game)
                print(f"Created '{title}'")
                self.state.game = rv.id
                self.state.character = None
            except ApiException as e:
                print(f"Cannot create '{title}'': {e.body}")

    def _cmd_signup(self, *_):
        """Signup with a new server"""
        with self.api.player_api() as api:
            try:
                p = PlayerSubmit(title=self.api.player)
                api.player_post(p)
                print(f"Create '{self.api.player}'")
            except ApiException as e:
                print(f"Cannot create '{self.api.player}': {e.body}")

    def _cmd_delete(self, title=None, *_):
        """Remove a game from the server"""
        if not title:
            print("Need more than just a /delete")
            return

        with self.api.api() as api:
            rv = api.game_get()
            # Delete the game, if we have the title right
            for game in rv.value:
                if game.title == title:
                    rv = api.game_game_id_delete(game.id)
                    print(f"'{title}'' is deleted.")
                    return
            print(f"Game {title} not found!")

    def _get_game_id(self):
        with self.api.api() as api:
            rv = api.game_get()
            for game in rv.value:
                if game.title == self.api.game:
                    return game.id

    def _get_player_id(self):
        with self.api.player_api() as api:
            rv = api.player_get()
            for p in rv.value:
                if p.title == self.api.player:
                    return p.id

    def _get_character_id(self):
        with self.api.character_api() as api:
            rv = api.player_player_id_character_get(self.state.player)
            for c in rv.value:
                if c.title == self.api.character:
                    return c.id

    def _create_character(self):
        with self.api.character_api() as api:
            c = CharacterSubmit(title=self.api.character)
            rv = api.game_game_id_player_player_id_character_post(
                self.state.game, self.state.player, c
            )
            return rv.id

    def _cmd_join(self):
        """Join the game in your configuration"""

        # get game id from server
        try:
            gid = self._get_game_id()
            if gid:
                self.state.game = gid
                print(f"Found game '{self.api.game}' [{gid}]")
            else:
                print(f"Could not find '{self.api.game}' on server")

            # get player id from server
            pid = self._get_player_id()
            if pid:
                self.state.player = pid
                print(f"Found player '{self.api.player}' [{pid}]")
            else:
                print(f"Could not find '{self.api.player}' on server")
                return

            # get character id from server
            cid = self._get_character_id()
            if not cid:
                print(
                    f"Could not find '{self.api.character}' on server; gonna create it.."
                )
                cid = self._create_character()
            print(f"Found character '{self.api.character}' [{cid}]")
            self.state.character = cid

            # run a blank turn to get a LOOK
            body = TurnSubmit(command="")
            with self.api.turn_api() as api:
                rv = api.game_game_id_character_character_id_turn_post(
                    self.state.game, self.state.character, body
                )
                if rv.text:
                    print()
                    print(rv.text)

        except Exception as e:
            print(f"Cannot join :(\n\t{e}")

    def _cmd_kill(self):
        """Delete current character from game"""
        if not self.state.character:
            print("Please /join first")
            return

        with self.api.character_api() as api:
            api.player_player_id_character_character_id_delete(
                self.state.player, self.state.character
            )
            print("Character is deleted.")

    def _cmd_newprop(self, *args):
        """Add a new property to a game"""
        if len(args) < 2:
            print("Need /newprop <key> <value>")
            return

        if not self.state.game:
            print("Please /join first")
            return

        with self.api.api() as api:
            props = api.game_game_id_get(self.state.game)
            props.properties[args[0]] = args[1]
            props = props.to_dict()
            del props["id"]
            api.game_game_id_put(self.state.game, GameSubmit(**props))

    def _cmd_delprop(self, *args):
        """Remove a property from a game"""
        if len(args) < 1:
            print("Need /delprop <key>")
            return

        if not self.state.game:
            print("Please /join first")
            return

        with self.api.api() as api:
            props = api.game_game_id_get(self.state.game).to_dict()
            del props["id"]
            if args[0] in props["properties"]:
                del props["properties"][args[0]]
            else:
                print(f"Cannot find property '{args[0]}'")
                return
            api.game_game_id_put(self.state.game, GameSubmit(**props))

    def run(self, command):
        (cmd, *args) = command.split()

        cls_cmd = f"_cmd_{cmd}"
        if hasattr(self, cls_cmd):
            getattr(self, cls_cmd)(*args)
        else:
            print("I don't know that command")
            return
