import os
from typing import List

from fvttmv.config import RunConfig, ProgramConfigChecker
from fvttmv.exceptions import FvttmvInternalException
from fvttmv.move.__directory_mover import DirectoryMover
from fvttmv.move.__file_mover import FileMover
from fvttmv.move.__mover_pre_checker import PreMoveChecker
from fvttmv.move.override_confirm import OverrideConfirm
from fvttmv.move.reference_update_confirm import ReferenceUpdateConfirm
from fvttmv.path_tools import PathTools
from fvttmv.update.references_updater import ReferencesUpdater


class Mover:
    """
    Moves files and directories and updates references
    """

    def __init__(self,
                 run_config: RunConfig,
                 references_updater: ReferencesUpdater,
                 override_confirm: OverrideConfirm = OverrideConfirm(),
                 reference_update_confirm: ReferenceUpdateConfirm = ReferenceUpdateConfirm()):

        self.__run_config = run_config

        self.__path_tools = PathTools(run_config.get_absolute_path_to_foundry_data())

        self.__file_mover = FileMover(run_config,
                                      self.__path_tools,
                                      references_updater,
                                      override_confirm,
                                      reference_update_confirm)

        self.__directory_mover = DirectoryMover(run_config,
                                                self.__path_tools,
                                                references_updater,
                                                self.move)

        self.__pre_move_checker = PreMoveChecker(run_config,
                                                 self.__path_tools)

        ProgramConfigChecker.assert_config_is_ok(run_config)

    def __correct_cases(self,
                        src_list: List[str]):

        result = []

        for src in src_list:

            if os.path.exists(src):
                result.append(PathTools.get_correctly_cased_path(src))
            else:
                if self.__run_config.no_move:
                    # TODO improve: Could correct the parts of the path that exist
                    result.append(src)
                else:
                    raise FvttmvInternalException("Path does not exist: {0}".format(src))

        return result

    def __move_single(self,
                      src: str,
                      dst: str,
                      depth: int):

        if os.path.isfile(src):
            self.__file_mover.move_file(src,
                                        dst,
                                        depth)
        elif os.path.isdir(src):
            self.__directory_mover.move_directory(src,
                                                  dst,
                                                  depth)
        else:
            if os.path.exists(src):
                raise FvttmvInternalException("Can only move files or folders.")
            else:
                if self.__run_config.no_move and depth == 0:
                    # Treat non-existing paths as files
                    self.__file_mover.move_file(src,
                                                dst,
                                                depth)
                else:
                    raise FvttmvInternalException("Path does not exist: {0}".format(src))

    def move(self,
             src_list: List[str],
             dst: str,
             depth: int = 0) -> None:

        self.__pre_move_checker.perform_pre_checks(src_list,
                                                   dst)

        # Windows is not case sensitive -> correct cases of path to avoid problems
        case_corrected_src_list = self.__correct_cases(src_list)

        for src in case_corrected_src_list:
            self.__move_single(src,
                               dst,
                               depth)
