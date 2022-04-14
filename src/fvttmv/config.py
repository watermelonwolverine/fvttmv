import json
import logging
import os.path
from typing import List

from fvttmv import config_file_encoding
from fvttmv.exceptions import FvttmvException
from fvttmv.path_tools import PathTools


class Keys:
    absolute_path_to_foundry_data_key = "absolute_path_to_foundry_data"
    additional_targets_to_update = "additional_targets_to_update"


class ProgramConfig:

    def get_absolute_path_to_foundry_data(self) -> str:
        raise NotImplementedError("Not implemented")

    def get_additional_targets_to_update(self) -> List[str]:
        raise NotImplementedError("Not implemented")


class ProgramConfigImpl(ProgramConfig):
    # given
    __abs_path_to_foundry_data: str
    __additional_targets_to_update: List[str]

    def __init__(self,
                 abs_path_to_foundry_data: str,
                 additional_targets_to_update: List[str]):
        self.__abs_path_to_foundry_data = abs_path_to_foundry_data
        self.__additional_targets_to_update = additional_targets_to_update

        ProgramConfigChecker.assert_config_is_ok(self)

    def get_absolute_path_to_foundry_data(self) -> str:
        return self.__abs_path_to_foundry_data

    def get_additional_targets_to_update(self) -> List[str]:
        return self.__additional_targets_to_update

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return str(self)


class ConfigFileReader:

    @staticmethod
    def read_config_file(path_to_config_file) -> ProgramConfig:

        logging.debug("Reading config from: %s", path_to_config_file)

        if not os.path.exists(path_to_config_file):
            raise FvttmvException("Missing config file. Could not find {0}".format(path_to_config_file))

        # noinspection PyBroadException
        try:
            with open(path_to_config_file, encoding=config_file_encoding) as config_file:
                config_dict = json.load(config_file)
        except BaseException as ex:
            raise FvttmvException("Exception while reading config file: " + str(ex))

        return ConfigFileReader.parse_dict(config_dict)

    @staticmethod
    def parse_dict(config_dict: dict) -> ProgramConfig:

        abs_path_to_foundry_data: str = config_dict[Keys.absolute_path_to_foundry_data_key]

        additional_targets_to_update: List[str]

        if Keys.additional_targets_to_update in config_dict:
            additional_targets_to_update = config_dict[Keys.additional_targets_to_update]
        else:
            additional_targets_to_update = []

        return ProgramConfigImpl(abs_path_to_foundry_data,
                                 additional_targets_to_update)


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

    def get_additional_targets_to_update(self) -> List[str]:
        return self._program_config.get_additional_targets_to_update()

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return str(self)


class ProgramConfigChecker:
    error_message = "{0} is not configured correctly. Reason: {1}"

    @staticmethod
    def assert_config_is_ok(program_config: ProgramConfig):

        ProgramConfigChecker.__assert_path_to_foundry_data_is_ok(program_config)

        ProgramConfigChecker.__assert_additional_targets_are_ok(program_config)

    @staticmethod
    def __assert_path_to_foundry_data_is_ok(program_config: ProgramConfig) -> None:

        abs_path_to_foundry_data = program_config.get_absolute_path_to_foundry_data()

        ProgramConfigChecker.assert_path_to_foundry_data_is_ok(abs_path_to_foundry_data)

    @staticmethod
    def assert_path_to_foundry_data_is_ok(abs_path_to_foundry_data: str) -> None:
        try:
            PathTools.assert_path_format_is_ok(abs_path_to_foundry_data)
        except FvttmvException as ex:
            error_msg = ProgramConfigChecker.error_message.format(
                Keys.absolute_path_to_foundry_data_key,
                ex)
            raise FvttmvException(error_msg)

        if not os.path.isdir(abs_path_to_foundry_data):
            error_msg = ProgramConfigChecker.error_message.format(
                Keys.absolute_path_to_foundry_data_key,
                "{0} is not absolute".format(abs_path_to_foundry_data))
            raise FvttmvException(error_msg)

    @staticmethod
    def __assert_additional_targets_are_ok(program_config: ProgramConfig):

        additional_targets_to_update = program_config.get_additional_targets_to_update()

        ProgramConfigChecker.assert_additional_targets_to_update_are_ok(additional_targets_to_update)

    @staticmethod
    def assert_additional_targets_to_update_are_ok(additional_targets_to_update: List[str]):

        if type(additional_targets_to_update) is not list:
            error_msg = ProgramConfigChecker.error_message.format(
                Keys.additional_targets_to_update,
                "Not a list.")

            raise FvttmvException(error_msg)

        for additional_target in additional_targets_to_update:
            if not ProgramConfigChecker.assert_additional_target_is_ok(additional_target):
                ProgramConfigChecker.assert_additional_target_is_ok(additional_target)

    @staticmethod
    def assert_additional_target_is_ok(abs_path_to_target: str) -> None:

        if type(abs_path_to_target) is not str:
            error_msg = ProgramConfigChecker.error_message.format(
                Keys.additional_targets_to_update,
                "Not a string.")
            raise FvttmvException(error_msg)

        try:
            PathTools.assert_path_format_is_ok(abs_path_to_target)
        except FvttmvException as ex:
            ProgramConfigChecker.error_message.format(Keys.additional_targets_to_update,
                                                      ex)

        if not os.path.isfile(abs_path_to_target) \
                and not os.path.isdir(abs_path_to_target):
            error_msg = ProgramConfigChecker.error_message.format(
                Keys.additional_targets_to_update,
                "{0} is neither a file nor a directory.".format(abs_path_to_target))
            raise FvttmvException(error_msg)
