"""
  Client Configuration
"""

import attr
import toml


@attr.s(auto_attribs=True)
class Config:
    """Enough configuration for CLI to play a game"""

    url: str
    game: str
    player: str
    character: str


def load_config(config_path, profile):
    """Read TOML file from the given path; use the given profile"""
    with open(config_path) as f:
        config = toml.load(f)
    return Config(**config[profile])
