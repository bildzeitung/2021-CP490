from pathlib import Path

import click
from prompt_toolkit import PromptSession

from .config import load_config
from .runners import MetaRunner, ContentRunner, GameRunner
from .api import Api
from .state import State

session = PromptSession()


@click.command()
@click.option(
    "--config",
    "-c",
    help="Config TOML file",
    default=Path().home() / ".config" / "coal.toml",
    show_default=True,
)
@click.option(
    "--profile",
    "-p",
    help="Which server profile to use",
    default="DEFAULT",
    show_default=True,
)
def main(config, profile):
    config = load_config(config, profile)
    state = State()
    print(f"Config: {config}")

    api = Api.from_config(config)
    mr = MetaRunner(api, state)
    cr = ContentRunner(api, state)
    gr = GameRunner(api, state)
    while True:
        cmd = session.prompt("> ")
        if cmd.startswith("/"):
            mr.run(cmd[1:])
        elif cmd.startswith(";"):
            cr.run(cmd[1:])
        else:  # tell the game engine!
            gr.run(cmd.strip())


if __name__ == "__main__":
    main()
