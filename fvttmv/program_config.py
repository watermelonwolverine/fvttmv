import os.path
from os import path
from typing import Dict

from fvttmv.exceptions import FvttmvException
from fvttmv.path_tools import PathTools

absolute_path_to_foundry_data_key = "absolute_path_to_foundry_data"


class ProgramConfig:

    def get_absolute_path_to_foundry_data(self) -> str:
        raise NotImplementedError("Not implemented")


class ProgramConfigImpl(ProgramConfig):
    # given
    _config_dict: Dict[str, str]

    def __init__(self, config_dict: Dict[str, str]):
        self.config_dict = config_dict
        self._check_config_dict()

    def _check_config_dict(self):
        self._check_absolute_path_to_foundry_data()

    def _check_absolute_path_to_foundry_data(self):
        value: str = self.config_dict[absolute_path_to_foundry_data_key]

        if value == "" \
                or not os.path.isabs(value) \
                or not PathTools.is_normalized_path(value) \
                or not path.isdir(value) \
                or not path.exists(value):
            raise FvttmvException("{0} has to be a normalized absolute path pointing to an existing folder"
                                  .format(absolute_path_to_foundry_data_key))

    def get_absolute_path_to_foundry_data(self) -> str:
        return self.config_dict[absolute_path_to_foundry_data_key]

    def __str__(self):
        return str(self.config_dict)
