import json
import logging
import os.path

from fvttmv.__checks import check_path_to_foundry_data
from fvttmv.exceptions import FvttmvException


class Keys:
    absolute_path_to_foundry_data_key = "absolute_path_to_foundry_data"


class ProgramConfig:

    def get_absolute_path_to_foundry_data(self) -> str:
        raise NotImplementedError("Not implemented")


class ProgramConfigImpl(ProgramConfig):
    # given
    __abs_path_to_foundry_data: str

    def __init__(self,
                 abs_path_to_foundry_data: str):
        if not check_path_to_foundry_data(abs_path_to_foundry_data):
            raise FvttmvException("Absolute path to foundry data is not configures correctly.")

        self.__abs_path_to_foundry_data = abs_path_to_foundry_data

    def get_absolute_path_to_foundry_data(self) -> str:
        return self.__abs_path_to_foundry_data

    def __str__(self):
        return json.dumps(self.__dict__)


class ConfigFileReader:

    @staticmethod
    def read_config_file(path_to_config_file) -> ProgramConfig:

        logging.debug("Reading config from: %s", path_to_config_file)

        if not os.path.exists(path_to_config_file):
            raise FvttmvException("Missing config file. Could not find {0}".format(path_to_config_file))

        # noinspection PyBroadException
        try:
            with open(path_to_config_file, encoding="utf-8") as config_file:
                config_dict = json.load(config_file)
        except BaseException as ex:
            raise FvttmvException("Exception while reading config file: " + str(ex))

        return ConfigFileReader.parse_dict(config_dict)

    @staticmethod
    def parse_dict(config_dict: dict) -> ProgramConfig:

        abs_path_to_foundry_data: str = config_dict[Keys.absolute_path_to_foundry_data_key]

        return ProgramConfigImpl(abs_path_to_foundry_data)


class RunConfig(ProgramConfig):
    # If this is set to true no files will be moved, only the references will be updated
    no_move: bool = False

    # If this is set to true all files given as args are handled as src files and all the program does is look for
    # references and print some information
    check_only: bool = False

    # Do not prompt before overriding
    force: bool = False

    _program_config: ProgramConfig

    def __init__(self,
                 program_config: ProgramConfig):
        self._program_config = program_config

    def get_absolute_path_to_foundry_data(self) -> str:
        return self._program_config.get_absolute_path_to_foundry_data()

    def __str__(self):
        return "RunConfig: ProgramConfig:{0}, no_move={1}, check_only={2}".format(
            str(self._program_config),
            self.no_move,
            self.check_only)


class ProgramConfigChecker:

    @staticmethod
    def check_config(program_config: ProgramConfig):
        abs_path_to_foundry_data = program_config.get_absolute_path_to_foundry_data()

        if not check_path_to_foundry_data(abs_path_to_foundry_data):
            raise FvttmvException("{0} is not configured correctly.".format(Keys.absolute_path_to_foundry_data_key))
