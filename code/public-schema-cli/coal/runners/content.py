import attr
from tabulate import tabulate

from coal_public_api_client.models import RoomSubmit, ExitSubmit
from coal_public_api_client.exceptions import ApiException, ServiceException

@attr.s
class ContentRunner:
    """ Prefix commands to add content to the game
    """
    api = attr.ib()
    state = attr.ib()

    def _cmd_list_room(self, *_):
        with self.api.api() as api:
            try:
                rv = api.game_game_id_room_get(self.state.game)
                print(tabulate([r.id, r.title] for r in rv.value))
            except ServiceException:
                print("Problem with API server (is the content server up?)")

    def _cmd_add_room(self, *args):
        if not args:
            print("Need a title")
        title = args[0]
        desc = " ".join(args[1:])
        if not desc:
            print("Need a room description")
            return

        with self.api.api() as api:
            try:
                room = RoomSubmit(title=title, description=desc)
                api.game_game_id_room_post(self.state.game, room)
                print(f"Created '{title}'")
            except ApiException as e:
                print(f"Cannot create '{title}': {e.body}")

    def _get_room_id_from_title(self, title):
        with self.api.api() as api:
            try:
                rv = api.game_game_id_room_get(self.state.game)
                for r in rv.value:
                    if r.title == title:
                        return r.id
            except ServiceException:
                print("Problem with API server (is the content server up?)")

    def _cmd_get_room(self, *args):
        if not args:
            print("Need a room title")
        title = args[0]

        room_id = self._get_room_id_from_title(title)
        if not room_id:
            print(f"Cannot find room: 'title'")
            return
        with self.api.api() as api:
            try:
                rv = api.game_game_id_room_room_id_get(self.state.game, room_id)
                print(tabulate([k, v] for k, v in rv.to_dict().items()))
            except ApiException as e:
                print(f"Cannot get room details: {e.body}")

    def _cmd_add_exit(self, *args):
        if not args or len(args) < 4:
            print("Need: <direction> <from> -> <to>")
            return
        d, from_room, _, to_room = args
        from_rid = self._get_room_id_from_title(from_room)
        to_rid = self._get_room_id_from_title(to_room)

        with self.api.api() as api:
            try:
                es = ExitSubmit(to_room_id=to_rid, direction=d)
                rv = api.game_game_id_room_room_id_exit_post(self.state.game, from_rid, es)
                print(rv)
            except ApiException as e:
                print(f"Cannot add exit: {e.body}")

    def _cmd_rm_room(self, *args):
        if not args:
            print("Need a room title")
        title = args[0]

        room_id = self._get_room_id_from_title(title)
        if not room_id:
            print(f"Cannot find room: |{title}|")
            return
        with self.api.api() as api:
            try:
                api.game_game_id_room_room_id_delete(self.state.game, room_id)
            except ApiException as e:
                print(f"Cannot delete room: {e.body}")

    def run(self, command):
        if not self.state.game:
            print("Please /join a game before using content commands")
            return

        args = command.split()
        if len(args) < 2:
            print("Need at least: <noun> <verb>")
            return

        (verb, noun, *args) = command.split()

        cls_cmd = f"_cmd_{noun}_{verb}"
        if hasattr(self, cls_cmd):
            getattr(self, cls_cmd)(*args)
        else:
            print("I don't know that command")
            return
