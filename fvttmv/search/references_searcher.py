import os
import sys
from io import TextIOWrapper
from typing import List

from fvttmv.exceptions import FvttmvException
from fvttmv.iterators.directory_walker import DirectoryWalker, DirectoryWalkerCallback
from fvttmv.path_tools import PathTools
from fvttmv.search.references_searcher_db_files import ReferencesSearcherDbFiles


class DirectoryWalkerCallbackImpl(DirectoryWalkerCallback):
    _path_tools: PathTools
    _text_io_wrapper: TextIOWrapper

    def __init__(self,
                 path_tools: PathTools,
                 text_io_wrapper: TextIOWrapper):
        self._path_tools = path_tools
        self._text_io_wrapper = text_io_wrapper

    def step_into_directory(self,
                            abs_path_to_directory: str) -> None:
        pass

    def step_out_of_directory(self, abs_path_to_directory: str) -> None:
        pass

    def process_file(self,
                     abs_path_to_file: str) -> None:
        relative_path_to_file = self._path_tools.make_path_relative_to_foundry_data(abs_path_to_file)

        relative_path_to_file_unix_style = relative_path_to_file.replace("\\", "/")

        abs_paths_to_db_files = ReferencesSearcherDbFiles.search_for_references_in_db_files(
            self._path_tools.abs_path_to_foundry_data,
            relative_path_to_file_unix_style)

        for abs_path_to_db_file in abs_paths_to_db_files:
            relative_path_to_db_file = self._path_tools.make_path_relative_to_foundry_data(abs_path_to_db_file)
            self._text_io_wrapper.write(
                "Found reference to {0} in {1}\n".format(relative_path_to_file_unix_style,
                                                         relative_path_to_db_file))


class ReferencesSearcher:
    """
    Searches for references
    """

    _path_tools: PathTools
    _text_io_wrapper: TextIOWrapper

    def __init__(self,
                 path_tools: PathTools,
                 text_io_wrapper: TextIOWrapper = sys.stdout):

        self._path_tools = path_tools
        self._text_io_wrapper = text_io_wrapper

    def search(self,
               search_list: List[str]) -> None:

        self._perform_pre_checks(search_list)

        walker_callback = DirectoryWalkerCallbackImpl(self._path_tools,
                                                      self._text_io_wrapper)

        directory_walker = DirectoryWalker(walker_callback)

        for absolute_path_to_file_or_directory in search_list:

            if os.path.isdir(absolute_path_to_file_or_directory):
                directory_walker.walk_directory(absolute_path_to_file_or_directory)
            else:
                walker_callback.process_file(absolute_path_to_file_or_directory)

    def _perform_pre_checks(self,
                            search_list: List[str]) -> None:

        for path in search_list:

            # requiring paths to be absolute - makes thing easier to implement
            if not os.path.isabs(path) \
                    or not self._path_tools.is_in_foundry_data(path) \
                    or not PathTools.is_normalized_path(path):
                raise FvttmvException()
