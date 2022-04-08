import os
from typing import List

from fvttmv.config import RunConfig, ProgramConfigChecker
from fvttmv.move.directory_mover import DirectoryMover
from fvttmv.move.file_mover import FileMover
from fvttmv.move.mover_pre_checker import PreMoveChecker
from fvttmv.move.override_confirm import OverrideConfirm
from fvttmv.move.reference_update_confirm import ReferenceUpdateConfirm
from fvttmv.path_tools import PathTools
from fvttmv.update.references_updater import ReferencesUpdater


class Mover:
    """
    Moves files and directories and updates references
    """

    # worker
    directory_mover: DirectoryMover
    file_mover: FileMover
    path_tools: PathTools
    override_confirm: OverrideConfirm
    reference_update_confirm: ReferenceUpdateConfirm
    pre_move_checker: PreMoveChecker

    def __init__(self,
                 run_config: RunConfig,
                 references_updater: ReferencesUpdater,
                 override_confirm: OverrideConfirm = OverrideConfirm(),
                 reference_update_confirm: ReferenceUpdateConfirm = ReferenceUpdateConfirm()):

        self.path_tools = PathTools(run_config.get_absolute_path_to_foundry_data())

        self.file_mover = FileMover(run_config,
                                    self.path_tools,
                                    references_updater,
                                    override_confirm,
                                    reference_update_confirm)

        self.directory_mover = DirectoryMover(run_config,
                                              self.path_tools,
                                              references_updater,
                                              self.move)

        self.pre_move_checker = PreMoveChecker(self.path_tools)

        ProgramConfigChecker.check_config(run_config)

    def move(self,
             src_list: List[str],
             dst: str,
             depth: int = 0) -> None:

        self.pre_move_checker.perform_pre_checks(src_list,
                                                 dst)

        for src in src_list:
            self._move_single(src,
                              dst,
                              depth)

    def _move_single(self,
                     src: str,
                     dst: str,
                     depth: int):

        if os.path.isfile(src):
            self.file_mover.move_file(src,
                                      dst,
                                      depth)
        else:
            self.directory_mover.move_directory(src,
                                                dst,
                                                depth)
