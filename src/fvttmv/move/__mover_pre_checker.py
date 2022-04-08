import os
import sys
from typing import List

from fvttmv.exceptions import FvttmvException, FvttmvInternalException
from fvttmv.path_tools import PathTools

# some directories shouldn't be moved
_moving_not_allowed_rel_paths = \
    ["worlds",
     "systems",
     "modules"]


class PreMoveChecker:
    _moving_not_allowed_abs_paths: List[str]

    # given
    path_tools: PathTools

    def __init__(self,
                 path_tools: PathTools):

        if sys.platform not in ["win32", "linux"]:
            raise FvttmvException("Unsupported platform")

        self.path_tools = path_tools

        self._moving_not_allowed_abs_paths = []
        for rel_path in _moving_not_allowed_rel_paths:
            abs_path = os.path.join(path_tools.abs_path_to_foundry_data, rel_path)
            self._moving_not_allowed_abs_paths.append(abs_path)

    def perform_pre_checks(self,
                           src_list: List[str],
                           dst: str) -> None:
        """
        A few common checks that apply to files as well as directories
        """

        if not type(src_list) == list:
            raise FvttmvInternalException("Wrong type for argument src_list: {0}".format(type(src_list)))
        if not type(dst) == str:
            raise FvttmvInternalException("Wrong type for argument dst: {0}".format(type(dst)))

        # also checks if path is ok
        if not self.path_tools.is_in_foundry_data(dst):
            raise FvttmvException("Destination path has to be inside the configured foundry Data directory")

        # if more than one src then the dst must be a folder
        if len(src_list) > 1 \
                and not os.path.isdir(dst):
            raise FvttmvException("Cannot move multiple files or directories to '{0}': Not a directory"
                                  .format(dst))

        for src in src_list:
            self.check_src(src)

    def check_src(self,
                  src: str) -> None:

        if src.endswith(os.path.sep):
            raise FvttmvInternalException()

        # also checks if path is ok
        if not self.path_tools.is_in_foundry_data(src):
            raise FvttmvException("Source paths have to be inside the configured foundry Data directory")

        if not os.path.exists(src):
            raise FvttmvException("Cannot move '{0}': No such file or directory"
                                  .format(src))

        if not os.path.isfile(src) \
                and not os.path.isdir(src):
            raise FvttmvException("All source paths have to be files or a directories")

        if not self._is_moving_allowed(src):
            raise FvttmvException("Moving of '{0}' is not allowed"
                                  .format(src))

    def _is_moving_allowed(self,
                           path_to_file_or_directory: str) -> bool:

        relative_path = self.path_tools.make_path_relative_to_foundry_data(path_to_file_or_directory)

        while relative_path.endswith(os.path.sep):
            relative_path = relative_path[0:-1]

        for moving_not_allowed in self._moving_not_allowed_abs_paths:
            if PathTools.is_parent_dir(path_to_file_or_directory, moving_not_allowed):
                return False

        return True
