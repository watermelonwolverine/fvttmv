import glob
import logging
import os
import sys
import traceback
from typing import List

import fvttmv
from cli_wrapper.__args import version_option, verbose_info_option, verbose_debug_option, help_option, setup_option, \
    check_args, process_and_remove_config_args
from cli_wrapper.__constants import app_name, path_to_config_file_linux, issues_url, win32, linux, \
    path_to_config_file_windows
from cli_wrapper.__help_provider import tell_user_how_to_use_the_program
from cli_wrapper.__help_texts import help_text_windows, help_text_ubuntu
from cli_wrapper.__setup import setup
from fvttmv.config import RunConfig, ProgramConfig, ConfigFileReader
from fvttmv.exceptions import FvttmvException, FvttmvInternalException
from fvttmv.move.mover import Mover
from fvttmv.move.override_confirm import OverrideConfirm
from fvttmv.search.references_searcher import ReferencesSearcher
from fvttmv.update.references_updater import ReferencesUpdater

supported_platforms = [win32, linux]

bug_report_message = "Please file a bug report on %s" % issues_url
unsupported_os_error_msg = "Unsupported OS: {0}"


def __get_path_to_config_file():
    if sys.platform == linux:
        return os.path.abspath(path_to_config_file_linux)
    elif sys.platform == win32:
        return os.path.expandvars(path_to_config_file_windows)
    else:
        raise FvttmvException(unsupported_os_error_msg.format(sys.platform))


def __read_config_file() -> ProgramConfig:
    path_to_config_file = __get_path_to_config_file()

    program_config = ConfigFileReader.read_config_file(path_to_config_file)

    return program_config


def __perform_move_with(
        src_list: List[str],
        dst: str,
        config: RunConfig) -> None:
    logging.debug("Running with working_dir='%s', src_list='%s', dst='%s', config='%s'",
                  os.path.abspath("."),
                  src_list,
                  dst,
                  config)

    # abs_path removes trailing \ and / but doesn't fail on illegal characters
    abs_dst = os.path.abspath(dst)
    abs_src_list = []

    for src in src_list:
        abs_src_list.append(
            os.path.abspath(src))

    references_updater = ReferencesUpdater(config.get_absolute_path_to_foundry_data(),
                                           config.get_additional_targets_to_update())
    override_confirm = OverrideConfirm()

    mover = Mover(config,
                  references_updater,
                  override_confirm)

    mover.move(abs_src_list,
               abs_dst)


def __perform_search_with(
        search_list: List[str],
        config: RunConfig) -> None:
    logging.debug("Running with search_list='%s', config='%s'",
                  search_list,
                  config)

    abs_search_list = []

    for src in search_list:
        abs_search_list.append(
            os.path.abspath(src))

    searcher = ReferencesSearcher(config.get_absolute_path_to_foundry_data(),
                                  config.get_additional_targets_to_update())

    searcher.search(abs_search_list)


def __add_logging_stream_handler(level: int):
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    root.addHandler(handler)


def configure_logging(
        args: List[str]) -> None:
    """
    Processes all args which don't affect the run config
    """
    if verbose_debug_option in args:
        __add_logging_stream_handler(logging.DEBUG)
        args.remove(verbose_debug_option)
    elif verbose_info_option in args:
        __add_logging_stream_handler(logging.INFO)
        args.remove(verbose_info_option)
    else:
        logging.disable(logging.CRITICAL)
        logging.disable(logging.ERROR)


def __check_platform():
    if sys.platform not in supported_platforms:
        raise FvttmvException(unsupported_os_error_msg.format(sys.platform))


def __print_help_text():
    platform = sys.platform

    if platform == win32:
        print(help_text_windows)
    elif platform == linux:
        print(help_text_ubuntu)
    else:
        raise FvttmvException(unsupported_os_error_msg.format(platform))


def __glob_paths(paths: List[str]):
    result = []

    for path in paths:
        result += glob.glob(path)

    return result


def __maybe_glob_paths(paths: List[str]):
    platform = sys.platform

    if platform == linux:
        # bash: paths are already globbed before passed as argument
        return paths
    elif platform == win32:
        result = __glob_paths(paths)
        logging.debug("Globbed args: {0}".format(result))
        return result
    else:
        raise FvttmvException(unsupported_os_error_msg.format(platform))


def __do_run() -> None:
    __check_platform()

    args = sys.argv[1:]

    if len(args) == 0:
        tell_user_how_to_use_the_program()
        return

    check_args(args)

    configure_logging(args)

    logging.debug("Got arguments %s",
                  sys.argv)

    if setup_option in args:
        setup()
        return

    if help_option in args:
        __print_help_text()
        return

    if version_option in args:
        print("{0} version: {1}".format(app_name, fvttmv.__version__))
        return

    if os.path.exists(__get_path_to_config_file()):
        config = RunConfig(__read_config_file())
    else:
        raise FvttmvException("Missing config file. Use the --config option to create one.")

    process_and_remove_config_args(config,
                                   args)

    # globbing arguments here to achieve consistent behavior across Windows and Ubuntu even though it might not be
    # the best location to do it
    args = __maybe_glob_paths(args)

    if config.check_only:
        if len(args) < 1:
            raise FvttmvException("Search argument missing")

        __perform_search_with(args,
                              config)
    else:
        if len(args) < 1:
            raise FvttmvException("Source argument missing")
        if len(args) < 2:
            raise FvttmvException("Destination argument missing")

        source_paths = args[0:-1]

        destination_path = args[-1]  # last arg is destination arg

        __perform_move_with(source_paths,
                            destination_path,
                            config)


def main() -> None:
    try:
        __do_run()
    except FvttmvInternalException:
        formatted = traceback.format_exc()
        logging.error(formatted)
        print("An internal error occurred: " + str(formatted))
        print(bug_report_message)
    except FvttmvException as exception:
        # these are expected to happen sometimes - don't print the whole stack
        logging.error(exception)
        print(str(exception))
    except SystemExit:
        pass
    except BaseException:
        formatted = traceback.format_exc()
        logging.error(formatted)
        print("An unexpected error occurred: " + str(formatted))
        print(bug_report_message)
