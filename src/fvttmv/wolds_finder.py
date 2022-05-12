import os
from os import path
from typing import List

from fvttmv.config import ProgramConfigChecker


class WorldsFinder:
    """
    Looks for world folders in the 'worlds' folder and returns the paths to those which seem to be world folders
    and have the right version
    """

    # given
    __abs_path_to_foundry_data: str

    def __init__(self,
                 abs_path_to_foundry_data: str):

        ProgramConfigChecker.assert_path_to_foundry_data_is_ok(abs_path_to_foundry_data)

        self.__abs_path_to_foundry_data = abs_path_to_foundry_data

    def get_paths_to_worlds(self) -> List[str]:
        """
        Looks for world folders in the 'worlds' folder and returns the paths to those which seem to be world folders
        and have the right version
        """

        path_to_worlds_directory = path.join(self.__abs_path_to_foundry_data,
                                             "worlds")

        # os.listdir is not always sorted the same way. For testing purposes and reproduction purposes it should be though
        worlds_directory_content = sorted(os.listdir(path_to_worlds_directory))

        result = []

        for file_or_folder_name in worlds_directory_content:

            path_to_world = os.path.join(path_to_worlds_directory,
                                         file_or_folder_name)

            if self._is_path_a_world_dir(path_to_world):
                result.append(path_to_world)

        return result

    @staticmethod
    def _is_path_a_world_dir(target_path: str) -> bool:

        # has to be a directory
        if not path.isdir(target_path):
            return False

        # has to have world.json file
        if not path.exists(
                path.join(target_path,
                          "world.json")):
            return False

        path_to_data_dir = path.join(target_path,
                                     "data")

        # has to have a data sub directory
        if not path.isdir(path_to_data_dir):
            return False

        return True
