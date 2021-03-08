from pathlib import Path

import click
from prompt_toolkit import PromptSession

from coal_public_api_client.coal_public_api_client import Client

from .config import load_config


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
    print(f"Config: {config}")
    client = Client(config.url)

    while True:
        cmd = session.prompt("> ")
        print(f"COMMAND: |{cmd}|")


if __name__ == "__main__":
    main()