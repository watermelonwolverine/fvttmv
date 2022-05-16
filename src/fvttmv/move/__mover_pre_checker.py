import os
import sys
from typing import List

from fvttmv import db_file_encoding
from fvttmv.config import RunConfig
from fvttmv.exceptions import FvttmvException, FvttmvInternalException
from fvttmv.iterators.db_files_iterator import DbFilesIterator
from fvttmv.path_tools import PathTools

# some directories shouldn't be moved
_moving_not_allowed_rel_paths = \
    ["worlds",
     "systems",
     "modules"]

cannot_simultaneously_error_msg = "Cannot simultaneously move {0} and {1}"


class PreMoveChecker:
    __moving_not_allowed_abs_paths: List[str]

    # given
    __path_tools: PathTools

    def __init__(self,
                 run_config: RunConfig,
                 path_tools: PathTools):

        if sys.platform not in ["win32", "linux"]:
            raise FvttmvException("Unsupported platform")

        self.__run_config = run_config
        self.__path_tools = path_tools
        self.__moving_not_allowed_abs_paths = []

        for rel_path in _moving_not_allowed_rel_paths:
            abs_path = os.path.join(path_tools.abs_path_to_foundry_data, rel_path)
            self.__moving_not_allowed_abs_paths.append(abs_path)

    def perform_pre_checks(self,
                           src_list: List[str],
                           dst: str) -> None:
        """
        A few common checks that apply to files as well as directories
        """

        self.__check_db_files()

        if not type(src_list) == list:
            raise FvttmvInternalException("Wrong type for argument src_list: {0}".format(type(src_list)))
        if not type(dst) == str:
            raise FvttmvInternalException("Wrong type for argument dst: {0}".format(type(dst)))

        # also checks if path is ok
        if not self.__path_tools.is_in_foundry_data(dst):
            raise FvttmvException("Destination path has to be inside the configured foundry Data directory")

        # if more than one src then the dst must be a folder
        if len(src_list) > 1 \
                and not os.path.isdir(dst):
            raise FvttmvException("Cannot move multiple files or directories to '{0}': Not a directory"
                                  .format(dst))

        for src in src_list:
            self.check_src(src,
                           src_list)

    def check_src(self,
                  src: str,
                  src_list: List[str]) -> None:

        if src.endswith(os.path.sep):
            raise FvttmvInternalException()

        # also checks if path is ok
        if not self.__path_tools.is_in_foundry_data(src):
            raise FvttmvException("Source paths have to be inside the configured foundry Data directory")

        if not self.__run_config.no_move:
            # TODO test: move non-existing file

            if not os.path.exists(src):
                raise FvttmvException("Cannot move '{0}': No such file or directory"
                                      .format(src))

            if not os.path.isfile(src) \
                    and not os.path.isdir(src):
                raise FvttmvException("All source paths have to be files or a directories")

            other_src_list = src_list.copy()
            other_src_list.remove(src)
            for other_src in other_src_list:
                
                # Can't move parent and child dir simultaneously
                # TODO test: try to move parent and child or move file/dir twice
                if PathTools.is_parent_dir(other_src, src):
                    raise FvttmvException(cannot_simultaneously_error_msg.format(other_src, src))

                # Without this it fails during operation when moving two different folders which have the same name
                # for example moving creatures/players and creature_tokens/player into empty folder some_folder
                # TODO test
                _, other_name = os.path.split(other_src)
                _, name = os.path.split(src)
                if other_name == name:
                    raise FvttmvException(cannot_simultaneously_error_msg.format(other_src, src))

        if not self._is_moving_allowed(src):
            raise FvttmvException("Moving of '{0}' is not allowed"
                                  .format(src))

    def _is_moving_allowed(self,
                           path_to_file_or_directory: str) -> bool:

        relative_path = self.__path_tools.make_path_relative_to_foundry_data(path_to_file_or_directory)

        while relative_path.endswith(os.path.sep):
            relative_path = relative_path[0:-1]

        for moving_not_allowed in self.__moving_not_allowed_abs_paths:
            if PathTools.is_parent_dir(path_to_file_or_directory, moving_not_allowed):
                return False

        return True

    def __check_db_files(self):
        # fail early: check read and write access for db files and check if they are readable as utf-8
        iterator = DbFilesIterator()

        abs_paths_to_db_files = iterator.iterate_through_all(self.__run_config.get_absolute_path_to_foundry_data(),
                                                             self.__run_config.get_additional_targets_to_update())

        for abs_path_to_db_file in abs_paths_to_db_files:

            # TODO test
            if not os.access(abs_path_to_db_file, os.W_OK | os.R_OK):
                raise FvttmvException("Cannot access {0}, need read and write permissions.".format(abs_path_to_db_file))

            # check parse-ability
            # thumbs.db is an example where this would fail, which is an old thumbnail cache from Windows XP
            # TODO test
            try:
                with open(abs_path_to_db_file, "r", encoding=db_file_encoding, newline='') as fin:
                    fin.read()
            except Exception as ex:
                error_msg = "Unable to read {0} as UTF-8. It may be a system file or a corrupted db file. Reason: {1}" \
                    .format(abs_path_to_db_file,
                            ex)
                raise FvttmvException(error_msg)
