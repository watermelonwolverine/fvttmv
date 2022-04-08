import os

from fvttmv.path_tools import PathTools


def check_path_to_foundry_data(abs_path_to_foundry_data: str) -> bool:
    if not os.path.isabs(abs_path_to_foundry_data) \
            or not PathTools.is_normalized_path(abs_path_to_foundry_data) \
            or not os.path.isdir(abs_path_to_foundry_data):
        return False

    return True
