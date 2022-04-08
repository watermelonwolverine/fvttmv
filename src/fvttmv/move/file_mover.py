import logging
import os
import shutil

from fvttmv.exceptions import FvttmvException
from fvttmv.move.override_confirm import OverrideConfirm
from fvttmv.move.reference_update_confirm import ReferenceUpdateConfirm
from fvttmv.path_tools import PathTools
from fvttmv.config import RunConfig
from fvttmv.update.references_updater import ReferencesUpdater


class FileMover:
    config: RunConfig
    path_tools: PathTools
    references_updater: ReferencesUpdater
    override_confirm: OverrideConfirm
    references_update_confirm: ReferenceUpdateConfirm

    def __init__(self,
                 config: RunConfig,
                 path_tools: PathTools,
                 references_updater: ReferencesUpdater,
                 override_confirm: OverrideConfirm,
                 reference_update_confirm: ReferenceUpdateConfirm):

        self.config = config
        self.path_tools = path_tools
        self.references_updater = references_updater
        self.override_confirm = override_confirm
        self.references_update_confirm = reference_update_confirm

    def move_file(self,
                  abs_path_to_src_file: str,
                  abs_path_to_dst: str,
                  depth: int) -> None:

        PathTools.assert_path_format_is_ok(abs_path_to_src_file)
        PathTools.assert_path_format_is_ok(abs_path_to_dst)

        if os.path.isdir(abs_path_to_dst) and depth == 0:
            self._move_file_to_directory(abs_path_to_src_file,
                                         abs_path_to_dst)
        else:
            self._move_file_to_new_file(abs_path_to_src_file,
                                        abs_path_to_dst)

    def _move_file_to_directory(self,
                                abs_path_to_src_file: str,
                                abs_path_to_dst_dir: str) -> None:

        (_, file_name) = os.path.split(abs_path_to_src_file)

        new_dst = os.path.join(abs_path_to_dst_dir,
                               file_name)

        self._move_file_to_new_file(abs_path_to_src_file,
                                    new_dst)

    def _move_file_to_new_file(self,
                               abs_path_to_src_file: str,
                               abs_path_to_dst_file: str) -> None:

        self._pre_check_requirements(abs_path_to_src_file,
                                     abs_path_to_dst_file)

        file_was_moved = self._maybe_move_file(abs_path_to_src_file,
                                               abs_path_to_dst_file)

        update_references = file_was_moved

        if not update_references:
            update_references = self.references_update_confirm.confirm_reference_update(abs_path_to_src_file,
                                                                                        abs_path_to_dst_file)

        if update_references:
            self._update_dbs_after_moving(abs_path_to_src_file,
                                          abs_path_to_dst_file)

    def _pre_check_requirements(self,
                                abs_path_to_src_file: str,
                                abs_path_to_dst_file: str) -> None:

        if self.config.no_move:
            return

        # don't move file onto itself
        if PathTools.paths_are_the_same(abs_path_to_dst_file, abs_path_to_src_file):
            raise FvttmvException("Cannot move {0} onto itself".format(abs_path_to_src_file))

        # can't override a folder with a file
        if os.path.exists(abs_path_to_dst_file) \
                and os.path.isdir(abs_path_to_dst_file):
            raise FvttmvException(
                "{0} already exists and is a directory. Cannot continue.".format(abs_path_to_dst_file))

        (dst_dir, _) = os.path.split(abs_path_to_dst_file)

        # cannot move file into non existing directory
        if not os.path.exists(dst_dir):
            raise FvttmvException("Destination directory '{0}' does not exist"
                                  .format(abs_path_to_dst_file))

    def _maybe_move_file(self,
                         abs_path_to_src_file: str,
                         abs_path_to_dst_file: str) -> bool:
        if self.config.no_move:
            return True

        move = True

        if not self.config.force \
                and os.path.exists(abs_path_to_dst_file):
            move = self.override_confirm.confirm_override(abs_path_to_src_file,
                                                          abs_path_to_dst_file)

        if move:
            shutil.move(abs_path_to_src_file,
                        abs_path_to_dst_file)
            logging.debug("Moved %s to %s",
                          abs_path_to_src_file,
                          abs_path_to_dst_file)
            return True
        else:
            logging.debug("Did not override %s with %s",
                          abs_path_to_dst_file,
                          abs_path_to_src_file)
            return False

    def _update_dbs_after_moving(self,
                                 abs_path_to_src_file: str,
                                 abs_path_to_dst_file: str) -> None:

        old_reference = self.path_tools.create_reference_from_absolute_path(abs_path_to_src_file)

        new_reference = self.path_tools.create_reference_from_absolute_path(abs_path_to_dst_file)

        self.references_updater.replace_references(
            old_reference,
            new_reference)
