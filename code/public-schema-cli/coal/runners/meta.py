import attr

from coal_public_api_client.exceptions import (
    ApiException,
    ServiceException,
)
from coal_public_api_client.model.game_submit import GameSubmit
from coal_public_api_server.controllers.game.room.room import get


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
                        print(
                            f"ID   : {rv.id}:\nTITLE: {rv.title}\nDESC : {rv.description}"
                        )
                        return
                print(f"Cannot find |{game}|")
                return
            try:
                rv = api.game_get()
                for game in rv.value:
                    print(f"{game.id}: {game.title}")
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
                api.game_post(game)
                print(f"Created |{title}|")
            except ApiException as e:
                print(f"Cannot create |{title}|: {e.body}")

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
                    print(f"|{title}| is deleted.")
                    return
            print(f"Game {title} not found!")

    def run(self, command):
        (cmd, *args) = command.split()

        cls_cmd = f"_cmd_{cmd}"
        if hasattr(self, cls_cmd):
            getattr(self, cls_cmd)(*args)
        else:
            print("I don't know that command")
            return
        """
    if cmd == "join":  # join a game on the server with the player
      with self.api.api() as api:
        rv = api.game_get()
        for game in rv.value:
          if game.title == self.api.game:
            self.state['game_id'] = game.id
            print(f"Joined {game.title}")
            return
        print(f"Could not find '{self.game}' on server")
    """
