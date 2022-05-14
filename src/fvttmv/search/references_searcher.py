import os
import sys
from io import TextIOWrapper
from typing import List

from fvttmv.exceptions import FvttmvException
from fvttmv.iterators.directory_walker import DirectoryWalker, DirectoryWalkerCallback
from fvttmv.path_tools import PathTools
from fvttmv.search.__references_searcher_db_files import ReferencesSearcherDbFiles


class DirectoryWalkerCallbackImpl(DirectoryWalkerCallback):

    def __init__(self,
                 abs_path_to_foundry_data: str,
                 abs_paths_to_additional_targets: List[str],
                 text_io_wrapper: TextIOWrapper):
        # context
        self.__abs_path_to_foundry_data = abs_path_to_foundry_data
        self.__abs_paths_to_additional_targets = abs_paths_to_additional_targets
        self.__text_io_wrapper = text_io_wrapper

        # workers
        self.__path_tools = PathTools(abs_path_to_foundry_data)

    def step_into_directory(self,
                            abs_path_to_directory: str) -> None:
        pass

    def step_out_of_directory(self,
                              abs_path_to_directory: str) -> None:
        pass

    def process_file(self,
                     abs_path_to_file: str) -> None:
        relative_path_to_file_unix_style = self.__path_tools.create_reference_from_absolute_path(abs_path_to_file)

        abs_paths_to_db_files = ReferencesSearcherDbFiles.search_for_references_in_db_files(
            self.__abs_path_to_foundry_data,
            self.__abs_paths_to_additional_targets,
            relative_path_to_file_unix_style)

        for abs_path_to_db_file in abs_paths_to_db_files:
            relative_path_to_db_file = self.__path_tools.make_path_relative_to_foundry_data(abs_path_to_db_file)
            self.__text_io_wrapper.write(
                "Found reference to {0} in {1}\n".format(relative_path_to_file_unix_style,
                                                         relative_path_to_db_file))


class ReferencesSearcher:
    """
    Searches for references
    """

    def __init__(self,
                 abs_path_to_foundry_data: str,
                 abs_paths_to_additional_targets: List[str],
                 text_io_wrapper: TextIOWrapper = sys.stdout):
        # context
        self.__abs_path_to_foundry_data = abs_path_to_foundry_data
        self.__abs_paths_to_additional_targets = abs_paths_to_additional_targets
        self.__text_io_wrapper = text_io_wrapper

        # workers
        self.__path_tools = PathTools(abs_path_to_foundry_data)

    def search(self,
               search_list: List[str]) -> None:

        self.__perform_pre_checks(search_list)

        walker_callback = DirectoryWalkerCallbackImpl(self.__abs_path_to_foundry_data,
                                                      self.__abs_paths_to_additional_targets,
                                                      self.__text_io_wrapper)

        directory_walker = DirectoryWalker(walker_callback)

        for absolute_path_to_file_or_directory in search_list:

            if os.path.isdir(absolute_path_to_file_or_directory):
                directory_walker.walk_directory(absolute_path_to_file_or_directory)
            else:
                walker_callback.process_file(absolute_path_to_file_or_directory)

    def __perform_pre_checks(self,
                             search_list: List[str]) -> None:

        for path in search_list:

            # requiring paths to be absolute - makes thing easier to implement
            if not os.path.isabs(path) \
                    or not self.__path_tools.is_in_foundry_data(path) \
                    or not PathTools.is_normalized_path(path):
                raise FvttmvException()
