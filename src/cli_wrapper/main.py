import glob
import logging
import os
import sys
import traceback
from typing import List

import fvttmv
from cli_wrapper.__constants import app_name, config_file_name, path_to_config_file_linux, issues_url
from cli_wrapper.__help_provider import tell_user_how_to_use_the_program
from cli_wrapper.__help_texts import help_text_windows, help_text_ubuntu
from fvttmv.config import RunConfig, ProgramConfig, ConfigFileReader
from fvttmv.exceptions import FvttmvException, FvttmvInternalException
from fvttmv.move.mover import Mover
from fvttmv.move.override_confirm import OverrideConfirm
from fvttmv.search.references_searcher import ReferencesSearcher
from fvttmv.update.references_updater import ReferencesUpdater

version_option = "--version"
verbose_info_option = "--verbose-info"
verbose_debug_option = "--verbose-debug"
no_move_option = "--no-move"
check_option = "--check"
force_option = "--force"
help_option = "--help"
allowed_args = [
    version_option,
    verbose_info_option,
    verbose_debug_option,
    no_move_option,
    check_option,
    force_option,
    help_option
]

win32 = "win32"
linux = "linux"
supported_platforms = [win32, linux]

bug_report_message = "Please file a bug report on %s" % issues_url
unsupported_os_error_msg = "Unsupported OS: {0}"


def __get_path_to_config_file_windows():
    dir_of_script: str
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # running in a PyInstaller bundle
        # TODO fix: this doesn't work in cmd only in powershell
        dir_of_script = os.path.dirname(sys.argv[0])
    else:
        # running in normal python environment
        dir_of_script = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(dir_of_script, config_file_name)


def __get_path_to_config_file():
    if sys.platform == linux:
        return path_to_config_file_linux
    elif sys.platform == win32:
        return __get_path_to_config_file_windows()
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


def __check_for_unknown_args(args: List[str]) -> None:
    for arg in args:
        if arg.startswith("-"):
            if arg not in allowed_args:
                raise FvttmvException("Unknown argument: {0}".format(arg))


def __check_for_illegal_arg_combos(args: List[str]) -> None:
    combination_error_msg = "Combining '{0}' and '{1}' is not allowed"

    if check_option in args and no_move_option in args:
        msg = combination_error_msg.format(no_move_option, check_option)
        raise FvttmvException(msg)

    if verbose_debug_option in args and verbose_info_option in args:
        msg = combination_error_msg.format(verbose_info_option, verbose_debug_option)
        raise FvttmvException(msg)


def __check_for_duplicate_args(args: List[str]) -> None:
    for allowed_arg in allowed_args:
        if args.count(allowed_arg) > 1:
            raise FvttmvException("Only one occurrence per option is allowed")


def __check_args(args: List[str]) -> None:
    __check_for_unknown_args(args)
    __check_for_illegal_arg_combos(args)
    __check_for_duplicate_args(args)


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


def __read_bool_arg(arg: str,
                    args: List[str],
                    default: bool = False):
    if arg in args:
        args.remove(arg)
        return True
    else:
        return default


def __process_and_remove_config_args(
        config: RunConfig,
        args: List[str]) -> None:
    """
    Processes all args which affect the run config
    """

    config.no_move = __read_bool_arg(no_move_option,
                                     args)
    config.check_only = __read_bool_arg(check_option,
                                        args)
    config.force = __read_bool_arg(force_option,
                                   args)


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

    __check_args(args)

    configure_logging(args)

    logging.debug("Got arguments %s",
                  sys.argv)

    if help_option in args:
        __print_help_text()
        return

    if version_option in args:
        print("{0} version: {1}".format(app_name, fvttmv.__version__))
        return

    config = RunConfig(__read_config_file())

    __process_and_remove_config_args(config,
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


if __name__ == "__main__":
    main()
