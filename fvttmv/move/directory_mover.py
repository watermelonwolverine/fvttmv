import logging
import os
from typing import Callable, List

from fvttmv.exceptions import FvttmvException
from fvttmv.path_tools import PathTools
from fvttmv.run_config import RunConfig
from fvttmv.update.references_updater import ReferencesUpdater

cannot_move_msg = "Cannot move {0} to {1}: Operation not permitted"


class DirectoryMover:
    config: RunConfig
    path_tools: PathTools
    move_func: Callable[[List[str], str, int], None]
    references_updater: ReferencesUpdater

    def __init__(self,
                 config: RunConfig,
                 path_tools: PathTools,
                 references_updater: ReferencesUpdater,
                 move_func: Callable[[List[str], str, int], None]):

        self.config = config
        self.path_tools = path_tools
        self.move_func = move_func
        self.references_updater = references_updater

    def move_directory(self,
                       abs_path_to_src_dir: str,
                       abs_path_to_dst_dir: str,
                       depth: int) -> None:

        self._perform_pre_checks(abs_path_to_src_dir,
                                 abs_path_to_dst_dir)

        if os.path.isdir(abs_path_to_dst_dir) and depth == 0:
            self._move_directory_into_directory(
                abs_path_to_src_dir,
                abs_path_to_dst_dir,
                depth)
        elif not os.path.exists(abs_path_to_dst_dir) or depth > 0 or self.config.no_move:
            self._move_directory_directly_to_position(
                abs_path_to_src_dir,
                abs_path_to_dst_dir,
                depth)
        else:
            raise FvttmvException(cannot_move_msg.format(abs_path_to_src_dir, abs_path_to_dst_dir))

    def _move_directory_into_directory(self,
                                       abs_path_to_src_dir: str,
                                       abs_path_to_dst_dir: str,
                                       depth: int):

        directory_name = os.path.split(abs_path_to_src_dir)[1]
        new_abs_path_to_dst_dir = os.path.join(abs_path_to_dst_dir, directory_name)

        self._move_directory_directly_to_position(abs_path_to_src_dir,
                                                  new_abs_path_to_dst_dir,
                                                  depth)

    def _move_directory_directly_to_position(self,
                                             abs_path_to_src_dir: str,
                                             abs_path_to_dst_dir: str,
                                             depth: int):

        if not self.config.no_move:

            if os.path.exists(abs_path_to_dst_dir):
                raise FvttmvException(cannot_move_msg.format(abs_path_to_src_dir,
                                                             abs_path_to_dst_dir))

            os.mkdir(abs_path_to_dst_dir)

            logging.debug("Created empty dir %s", abs_path_to_dst_dir)

        self._move_contents_of_directory_to_directory(abs_path_to_src_dir,
                                                      abs_path_to_dst_dir,
                                                      depth)

        self._update_dbs_after_moving(abs_path_to_src_dir,
                                      abs_path_to_dst_dir)

        if len(os.listdir(abs_path_to_src_dir)) == 0:
            os.rmdir(abs_path_to_src_dir)
            logging.debug("Deleted empty dir %s", abs_path_to_src_dir)

    def _perform_pre_checks(self,
                            abs_path_to_src_dir: str,
                            abs_path_to_dst_dir: str):

        PathTools.assert_path_format_is_ok(abs_path_to_src_dir)
        PathTools.assert_path_format_is_ok(abs_path_to_dst_dir)

        if not self.config.no_move:
            self._assert_parent_dir_exists(abs_path_to_dst_dir)

        if abs_path_to_src_dir == abs_path_to_dst_dir:
            raise FvttmvException("Cannot move {0} onto itself'"
                                  .format(abs_path_to_src_dir))

        if PathTools.is_parent_dir(abs_path_to_src_dir,
                                   abs_path_to_dst_dir):
            raise FvttmvException("Cannot move {0} to a subdirectory of itself, '{1}'"
                                  .format(abs_path_to_src_dir, abs_path_to_dst_dir))

    def _update_dbs_after_moving(self,
                                 abs_path_to_src_dir: str,
                                 abs_path_to_dst_dir: str) -> None:

        old_reference = self.path_tools.create_reference_from_absolute_path(abs_path_to_src_dir)

        new_reference = self.path_tools.create_reference_from_absolute_path(abs_path_to_dst_dir)

        self.references_updater.replace_references(
            old_reference,
            new_reference)

    @staticmethod
    def _assert_parent_dir_exists(abs_path_to_dir):
        (abs_path_to_parent_dir, _) = os.path.split(abs_path_to_dir)

        if not os.path.exists(abs_path_to_parent_dir) \
                or not os.path.isdir(abs_path_to_parent_dir):
            raise FvttmvException("Cannot move into '{0}': No such directory".format(abs_path_to_parent_dir))

    def _move_contents_of_directory_to_directory(self,
                                                 abs_path_to_src_dir: str,
                                                 abs_path_to_dst_dir: str,
                                                 depth: int) -> None:
        PathTools.assert_path_format_is_ok(abs_path_to_src_dir)
        PathTools.assert_path_format_is_ok(abs_path_to_dst_dir)

        src_contents = os.listdir(abs_path_to_src_dir)

        for file_or_directory_name in src_contents:
            abs_path_to_sub_src = os.path.join(abs_path_to_src_dir,
                                               file_or_directory_name)

            abs_path_to_sub_dst = os.path.join(abs_path_to_dst_dir,
                                               file_or_directory_name)

            self.move_func([abs_path_to_sub_src],
                           abs_path_to_sub_dst,
                           depth + 1)
