import json
import logging
import os
import sys
from os import path
from typing import List

from fvttmv.exceptions import FvttmvException, FvttmvInternalException
from fvttmv.move.mover import Mover
from fvttmv.move.override_confirm import OverrideConfirm
from fvttmv.path_tools import PathTools
from fvttmv.program_config import ProgramConfig, ProgramConfigImpl
from fvttmv.run_config import RunConfig
from fvttmv.search.references_searcher import ReferencesSearcher
from fvttmv.update.references_updater import ReferencesUpdater

version = "0.2.0"

app_name = "fvttmv"
config_file_name = "{0}.conf".format(app_name)
path_to_config_file_linux = "/etc/{0}".format(config_file_name)
version_option = "--version"
verbose_info_option = "--verbose-info"
verbose_debug_option = "--verbose-debug"
no_move_option = "--no-move"
check_option = "--check"
force_option = "--force"
allowed_args = [
    version_option,
    verbose_info_option,
    verbose_debug_option,
    no_move_option,
    check_option,
    force_option
]


def get_path_to_config_file():
    if sys.platform == "linux":
        return path_to_config_file_linux
    elif sys.platform == "win32":
        dir_of_script: str
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # running in a PyInstaller bundle
            # TODO fix: this doesn't work in cmd only in powershell
            dir_of_script = os.path.dirname(sys.argv[0])
        else:
            # running in normal python environment
            dir_of_script = path.abspath(path.dirname(__file__))
        return os.path.join(dir_of_script, config_file_name)
    else:
        raise FvttmvException("Unsupported OS: {0}".format(sys.platform))


def read_config_file() -> ProgramConfig:
    path_to_config_file = get_path_to_config_file()

    logging.debug("Reading config from: %s", path_to_config_file)

    if not os.path.exists(path_to_config_file):
        raise FvttmvException("Missing config file. Could not find {0}".format(path_to_config_file))

    # noinspection PyBroadException
    try:
        with open(path_to_config_file, encoding="utf-8") as config_file:
            config_dict = json.load(config_file)
    except BaseException as ex:
        raise FvttmvException("Exception while reading config file: " + str(ex))

    return ProgramConfigImpl(config_dict)


def perform_move_with(
        src_list: List[str],
        dst: str,
        config: RunConfig) -> None:
    logging.debug("Running with src_list='%s', dst='%s', config='%s'",
                  src_list,
                  dst,
                  config)

    # abs_path removes trailing \ and / but doesn't fail on illegal characters
    abs_dst = path.abspath(dst)
    abs_src_list = []

    for src in src_list:
        abs_src_list.append(
            path.abspath(src))

    references_updater = ReferencesUpdater(config.get_absolute_path_to_foundry_data())
    override_confirm = OverrideConfirm()

    mover = Mover(config,
                  references_updater,
                  override_confirm)

    mover.move(abs_src_list,
               abs_dst)


def perform_search_with(
        search_list: List[str],
        config: RunConfig) -> None:
    logging.debug("Running with search_list='%s', config='%s'",
                  search_list,
                  config)

    abs_search_list = []

    for src in search_list:
        abs_search_list.append(
            path.abspath(src))

    path_tools = PathTools(config.get_absolute_path_to_foundry_data())

    searcher = ReferencesSearcher(path_tools)

    searcher.search(abs_search_list)


def check_option_args(args: List[str]) -> None:
    for arg in args:
        if arg.startswith("-"):
            if arg not in allowed_args:
                raise FvttmvException("Unknown argument: {0}".format(arg))

    combination_error_msg = "Combining '{0}' and '{1}' is not allowed"

    if check_option in args and no_move_option in args:
        msg = combination_error_msg.format(no_move_option, check_option)
        raise FvttmvException(msg)

    if verbose_debug_option in args and verbose_info_option in args:
        msg = combination_error_msg.format(verbose_info_option, verbose_debug_option)
        raise FvttmvException(msg)


def add_logging_stream_handler(level: int):
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    root.addHandler(handler)


def process_and_remove_config_neutral_args(
        args: List[str]) -> None:
    """
    Processes all args which don't affect the run config
    """
    if verbose_debug_option in args:
        add_logging_stream_handler(logging.DEBUG)
        logging.debug("Got arguments %s",
                      args)
        args.remove(verbose_debug_option)
    elif verbose_info_option in args:
        add_logging_stream_handler(logging.INFO)
        logging.debug("Got arguments %s",
                      args)
        args.remove(verbose_info_option)
    else:
        logging.disable(logging.CRITICAL)
        logging.disable(logging.ERROR)

    if version_option in args:
        print("{0} version: {1}".format(app_name, version))
        sys.exit(0)

    # remove program name
    args.pop(0)


def process_and_remove_config_args(
        config: RunConfig,
        args: List[str]) -> None:
    """
    Processes all args which affect the run config
    """
    if no_move_option in args:
        config.no_move = True
        args.remove(no_move_option)

    if check_option in args:
        config.check_only = True
        args.remove(check_option)

    if force_option in args:
        config.force = True


def do_run() -> None:
    src_list: list
    dst: str

    args = sys.argv[:]

    check_option_args(args)

    process_and_remove_config_neutral_args(args)

    config = RunConfig(read_config_file())

    process_and_remove_config_args(config,
                                   args)

    if config.check_only:
        if len(args) < 1:
            raise Exception("Search argument missing")

        perform_search_with(args,
                            config)
    else:
        if len(args) < 1:
            raise Exception("Source argument missing")
        if len(args) < 2:
            raise Exception("Destination argument missing")

        source_files = args[0:-1]
        destination = args[-1]  # last arg is destination arg

        perform_move_with(source_files,
                          destination,
                          config)


def main() -> None:
    try:
        do_run()
    except FvttmvInternalException as internal_exception:
        logging.error(internal_exception)
        print("An internal error occurred: " + str(internal_exception))
    except FvttmvException as exception:
        logging.error(exception)
        print(str(exception))
    except SystemExit:
        pass
    except BaseException as unexpected_exception:
        logging.error(unexpected_exception)
        print("An unexpected error occurred: " + str(unexpected_exception))


if __name__ == "__main__":
    main()
