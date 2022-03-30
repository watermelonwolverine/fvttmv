import os

from os import path
from typing import List

from fvttmv.exceptions import FvttmvException
from fvttmv.path_tools import PathTools


class WorldsFinder:
    """
    Looks for world folders in the 'worlds' folder and returns the paths to those which seem to be world folders
    and have the right version
    """

    # given
    _absolute_path_to_foundry_data: str

    def __init__(self,
                 absolute_path_to_foundry_data: str):

        if not path.isabs(absolute_path_to_foundry_data) \
                or not path.isdir(absolute_path_to_foundry_data) \
                or not PathTools.is_normalized_path(absolute_path_to_foundry_data):
            raise FvttmvException()

        self._absolute_path_to_foundry_data = absolute_path_to_foundry_data

    def get_paths_to_worlds(self) -> List[str]:
        """
        Looks for world folders in the 'worlds' folder and returns the paths to those which seem to be world folders
        and have the right version
        """

        path_to_worlds_directory = path.join(self._absolute_path_to_foundry_data,
                                             "worlds")

        worlds_directory_content = os.listdir(path_to_worlds_directory)

        result = []

        for file_or_folder_name in worlds_directory_content:

            path_to_world = os.path.join(path_to_worlds_directory,
                                         file_or_folder_name)

            if self.is_path_a_world_dir(path_to_world):
                result.append(path_to_world)

        return result

    @staticmethod
    def is_path_a_world_dir(target_path: str) -> bool:

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
