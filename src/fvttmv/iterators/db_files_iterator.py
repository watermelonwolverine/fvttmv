import os
from typing import List

from fvttmv.path_tools import PathTools
from fvttmv.wolds_finder import WorldsFinder

dirs_in_worlds_to_look_for_db_file = ["data", "packs"]


class DbFilesIterator:
    """
    Tools for iterating over db files.
    """

    def iterate_through_all(self,
                            abs_path_to_foundry_data: str,
                            abs_paths_to_additional_targets: List[str]):

        # Check before iterating -> Don't fail in the middle
        for abs_path in abs_paths_to_additional_targets + [abs_path_to_foundry_data]:
            PathTools.assert_path_format_is_ok(abs_path)

        for abs_path_to_target in abs_paths_to_additional_targets:
            PathTools.assert_path_is_file_or_dir(abs_path_to_target)

        PathTools.assert_path_is_dir(abs_path_to_foundry_data)

        for abs_path_to_db in self.__iterate_through_all_worlds(abs_path_to_foundry_data):
            yield abs_path_to_db

        for abs_path_to_db in self.__iterate_trough_additional_targets(abs_paths_to_additional_targets):
            yield abs_path_to_db

    def __iterate_through_all_worlds(self,
                                     abs_path_to_foundry_data: str):

        PathTools.assert_path_format_is_ok(abs_path_to_foundry_data)
        PathTools.assert_path_is_dir(abs_path_to_foundry_data)

        worlds_finder = WorldsFinder(abs_path_to_foundry_data)

        world_dirs = worlds_finder.get_paths_to_worlds()

        for path_to_world_dir in world_dirs:
            for db_file in self.__iterate_through_world_dir(path_to_world_dir):
                yield db_file

    def __iterate_trough_additional_targets(self,
                                            abs_paths_to_additional_targets: List[str]):

        for abs_path_to_additional_target in abs_paths_to_additional_targets:

            if os.path.isfile(abs_path_to_additional_target):
                yield abs_path_to_additional_target
                continue

            for abs_path_to_db in self.__iterate_through_dir(abs_path_to_additional_target):
                yield abs_path_to_db

    def __iterate_through_dir(self,
                              abs_path_to_dir: str):

        PathTools.assert_path_format_is_ok(abs_path_to_dir)
        PathTools.assert_path_is_dir(abs_path_to_dir)

        # os.listdir is not always sorted the same way. For testing purposes and reproduction purposes it should be though
        for element in sorted(os.listdir(abs_path_to_dir)):
            abs_path_to_element = os.path.join(abs_path_to_dir, element)

            if not os.path.isfile(abs_path_to_element):
                continue

            if element.endswith(".db"):
                yield abs_path_to_element

    def __iterate_through_world_dir(self,
                                    abs_path_to_world_dir: str):

        for directory in dirs_in_worlds_to_look_for_db_file:
            abs_path_to_dir = os.path.join(abs_path_to_world_dir, directory)
            for db_file in self.__iterate_through_dir(abs_path_to_dir):
                yield db_file
