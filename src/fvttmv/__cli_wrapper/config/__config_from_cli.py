from typing import List

from fvttmv.__cli_wrapper.__args import data_dir_option


def get_config_from_cli(args: List[str]):
    if data_dir_option in args:
        # TODO
        pass
    raise NotImplementedError()
