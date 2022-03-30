import os

from os import path
from typing import List

from fvttmv.exceptions import FvttmvException
from fvttmv.wolds_finder import WorldsFinder


class DbFilesIterator:
    """
    Iterates over all the *.db files in a given directory
    """

    @staticmethod
    def iterate_through_directory(path_to_directory: str):

        if not path.isdir(path_to_directory) \
                or not path.isabs(path_to_directory):
            raise FvttmvException("{0} is not absolute or not a directory".format(path_to_directory))

        directory_contents = os.listdir(path_to_directory)

        for element in directory_contents:

            path_to_element = path.join(path_to_directory, element)

            if path.isdir(path_to_element):

                for db_file in DbFilesIterator.iterate_through_directory(path_to_element):
                    yield db_file

            elif element.endswith(".db"):
                yield path_to_element

    @staticmethod
    def iterate_through_all_directories(paths_to_directory: List[str]):

        for path_to_directory in paths_to_directory:
            for db_file in DbFilesIterator.iterate_through_directory(path_to_directory):
                yield db_file

    @staticmethod
    def iterate_through_all_worlds(absolute_path_to_foundrydata: str):

        worlds_finder = WorldsFinder(absolute_path_to_foundrydata)

        worlds = worlds_finder.get_paths_to_worlds()

        for db_file in DbFilesIterator.iterate_through_all_directories(worlds):
            yield db_file
