import os

from fvttmv.exceptions import FvttmvException


class DirectoryWalkerCallback:

    def step_into_directory(self, abs_path_to_directory: str) -> None:
        raise NotImplementedError("Not implemented")

    def step_out_of_directory(self, abs_path_to_directory: str) -> None:
        raise NotImplementedError("Not implemented")

    def process_file(self, abs_path_to_file: str) -> None:
        raise NotImplementedError("Not implemented")


class DirectoryWalker:
    _callback: DirectoryWalkerCallback

    def __init__(self,
                 callback: DirectoryWalkerCallback):
        self._callback = callback

    def walk_directory(self,
                       abs_path_to_directory: str) -> None:

        if not os.path.exists(abs_path_to_directory) \
                or not os.path.isdir(abs_path_to_directory) \
                or not os.path.isabs(abs_path_to_directory):
            raise FvttmvException()

        directory_content = os.listdir(abs_path_to_directory)

        for element in directory_content:

            abs_path_to_element = os.path.join(abs_path_to_directory,
                                               element)

            if os.path.isdir(abs_path_to_element):
                self._callback.step_into_directory(abs_path_to_element)
                self.walk_directory(abs_path_to_element)
                self._callback.step_out_of_directory(abs_path_to_element)
            elif os.path.isfile(abs_path_to_element):
                self._callback.process_file(abs_path_to_element)
