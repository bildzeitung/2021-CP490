import attr


@attr.s
class ContentRunner:
    config = attr.ib()
    state = attr.ib()

    def run(self, command):
        (cmd, *args) = command.split()
        if cmd == "add":
            if len(args) < 3:
                print("Need at least: <object> <key> <params ...>")
                return
            self._add(args[2:], obj=args[0], key=args[1])

    def _add(self, *args, obj, key):
        if obj == "room":
            pass
        print(f"OBJ: {obj} KEY: {key} REST: {args}")
