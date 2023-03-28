from typing import List

from fvttmv.config import RunConfig
from fvttmv.exceptions import FvttmvException

version_option = "--version"
verbose_info_option = "--verbose-info"
verbose_debug_option = "--verbose-debug"
no_move_option = "--no-move"
check_option = "--check"
force_option = "--force"
help_option = "--help"
setup_option = "--config"

data_dir_option = "--data-dir"

allowed_args = [
    version_option,
    verbose_info_option,
    verbose_debug_option,
    no_move_option,
    check_option,
    force_option,
    help_option,
    setup_option
]


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


def check_args(args: List[str]) -> None:
    __check_for_unknown_args(args)
    __check_for_illegal_arg_combos(args)
    __check_for_duplicate_args(args)


def __read_bool_arg(arg: str,
                    args: List[str],
                    default: bool = False):
    if arg in args:
        args.remove(arg)
        return True
    else:
        return default


def process_and_remove_config_args(
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
