import os.path
from typing import List

from fvttmv.config import ProgramConfigChecker
from fvttmv.iterators.db_files_iterator import DbFilesIterator
from fvttmv.update.__references_updater_file import ReferencesUpdaterFile


class ReferencesUpdater:
    __abs_path_to_foundry_data: str
    __additional_targets_to_update: List[str]

    def __init__(self,
                 abs_path_to_foundry_data: str,
                 additional_targets_to_update: List[str]):
        ProgramConfigChecker.assert_path_to_foundry_data_is_ok(abs_path_to_foundry_data)
        ProgramConfigChecker.assert_additional_targets_to_update_are_ok(additional_targets_to_update)

        self.__abs_path_to_foundry_data = abs_path_to_foundry_data
        self.__additional_targets_to_update = additional_targets_to_update

    def replace_references(self,
                           old_reference: str,
                           new_reference: str):

        self.__replace_references_in_world_dbs(old_reference,
                                               new_reference)

        self.__replace_references_in_additional_targets(old_reference,
                                                        new_reference)

    def __replace_references_in_world_dbs(self,
                                          old_reference: str,
                                          new_reference: str):

        for db_file in DbFilesIterator.iterate_through_all_worlds(self.__abs_path_to_foundry_data):
            self.__replace_references_in_file(db_file,
                                              old_reference,
                                              new_reference)

    def __replace_references_in_additional_targets(self,
                                                   old_reference: str,
                                                   new_reference: str):
        for additional_target in self.__additional_targets_to_update:
            self.__replace_references_in_additional_target(additional_target,
                                                           old_reference,
                                                           new_reference)

    @staticmethod
    def __replace_references_in_additional_target(additional_target,
                                                  old_reference: str,
                                                  new_reference: str):
        if os.path.isfile(additional_target):
            ReferencesUpdater.__replace_references_in_file(additional_target,
                                                           old_reference,
                                                           new_reference)
        elif os.path.isdir(additional_target):
            ReferencesUpdater.__replace_references_in_additional_target_dir(additional_target,
                                                                            old_reference,
                                                                            new_reference)

    @staticmethod
    def __replace_references_in_additional_target_dir(additional_target_dir: str,
                                                      old_reference: str,
                                                      new_reference: str):
        for db_file in DbFilesIterator.iterate_through_dir(additional_target_dir):
            ReferencesUpdater.__replace_references_in_file(db_file,
                                                           old_reference,
                                                           new_reference)

    @staticmethod
    def __replace_references_in_file(abs_path_to_db_file: str,
                                     old_reference: str,
                                     new_reference: str):
        ReferencesUpdaterFile.replace_references_in_file(abs_path_to_db_file,
                                                         old_reference,
                                                         new_reference)
