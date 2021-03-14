from pathlib import Path

import click
from prompt_toolkit import PromptSession

from .config import load_config
from .runners import MetaRunner, ContentRunner

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
    state = {}
    print(f"Config: {config}")

    mr = MetaRunner.from_config(config, state)
    cr = ContentRunner(config, state)
    while True:
        cmd = session.prompt("> ")
        if cmd.startswith('/'):
            mr.run(cmd[1:])
        elif cmd.startswith(";"):
            cr.run(cmd[1:])
        else:
            print("UNHANDLED")
            


if __name__ == "__main__":
    main()