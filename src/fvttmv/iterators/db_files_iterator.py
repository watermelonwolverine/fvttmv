import os

from fvttmv.exceptions import FvttmvInternalException
from fvttmv.path_tools import PathTools
from fvttmv.wolds_finder import WorldsFinder

dirs_to_look_for_db_file = ["data", "packs"]

# thumbs.db = old windows xp thumbnail cache.
db_files_to_ignore = ["thumbs.db"]


class DbFilesIterator:
    """
    Iterates over all the foundry VTT *.db files in a given world directory
    """

    @staticmethod
    def iterate_through_world_dir(abs_path_to_world_dir: str):

        PathTools.assert_path_format_is_ok(abs_path_to_world_dir)

        if not os.path.isdir(abs_path_to_world_dir):
            raise FvttmvInternalException("{0} is not a directory.".format(abs_path_to_world_dir))

        for directory in dirs_to_look_for_db_file:
            path_to_dir = os.path.join(abs_path_to_world_dir, directory)
            for element in os.listdir(path_to_dir):
                path_to_element = os.path.join(path_to_dir, element)

                if not os.path.isfile(path_to_element):
                    continue

                if element in db_files_to_ignore:
                    continue

                if element.endswith(".db"):
                    yield path_to_element

    @staticmethod
    def iterate_through_all_worlds(abs_path_to_foundry_data: str):

        PathTools.assert_path_format_is_ok(abs_path_to_foundry_data)

        worlds_finder = WorldsFinder(abs_path_to_foundry_data)

        world_dirs = worlds_finder.get_paths_to_worlds()

        for path_to_world_dir in world_dirs:
            for db_file in DbFilesIterator.iterate_through_world_dir(path_to_world_dir):
                yield db_file
