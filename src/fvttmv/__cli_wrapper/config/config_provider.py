from typing import List

from .__config_from_cli import get_config_from_cli
from .__config_from_env import get_config_from_env
from .__config_from_file import get_config_from_file


def get_config(args: List[str]):
    return get_config_from_cli(args) \
           or get_config_from_env() \
           or get_config_from_file()
