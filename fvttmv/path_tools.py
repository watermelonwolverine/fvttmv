import os.path

from fvttmv.exceptions import FvttmvException, FvttmvInternalException


class PathTools:
    abs_path_to_foundry_data: str

    def __init__(self,
                 absolute_path_to_foundry_data: str):

        PathTools.assert_path_format_is_ok(absolute_path_to_foundry_data)

        if not os.path.isdir(absolute_path_to_foundry_data):
            raise FvttmvException("Configured Foundry VTT Data folder does not exist.")

        self.abs_path_to_foundry_data = absolute_path_to_foundry_data

    def make_path_relative_to_foundry_data_unix_style(self,
                                                      absolute_path: str) -> str:

        rel_path = self.make_path_relative_to_foundry_data(absolute_path)

        result = rel_path.replace("\\", "/")

        return result

    def make_path_relative_to_foundry_data(self,
                                           absolute_path: str) -> str:

        PathTools.assert_path_format_is_ok(absolute_path)

        if not self.is_in_foundry_data(absolute_path):
            raise FvttmvException()

        result = os.path.normpath(absolute_path)

        return os.path.relpath(result,
                               self.abs_path_to_foundry_data)

    def is_in_foundry_data(self,
                           absolute_path: str) -> bool:

        self.assert_path_format_is_ok(absolute_path)

        if absolute_path == self.abs_path_to_foundry_data:
            return False

        return self.is_parent_dir(self.abs_path_to_foundry_data,
                                  absolute_path)

    @staticmethod
    def is_parent_dir(absolute_parent_path,
                      absolute_path):
        PathTools.assert_path_format_is_ok(absolute_path)
        PathTools.assert_path_format_is_ok(absolute_parent_path)

        common_path = os.path.commonpath([absolute_parent_path,
                                          absolute_path])

        return common_path == absolute_parent_path

    @staticmethod
    def is_normalized_path(path: str) -> bool:

        if path.endswith(os.path.sep):
            path = path[:-len(os.path.sep)]

        norm_path = os.path.normpath(path)
        return path == norm_path

    @staticmethod
    def ends_with_separator(path: str):
        if path.endswith(os.path.sep) or path.endswith("/") or path.endswith("\\"):
            return True

    @staticmethod
    def contains_illegal_characters(path: str):

        try:
            os.stat(path)
        except FileNotFoundError:
            return False
        except OSError:
            return True

        return False

    @staticmethod
    def assert_path_format_is_ok(path: str):
        if not os.path.isabs(path) \
                or not PathTools.is_normalized_path(path) \
                or PathTools.ends_with_separator(path) \
                or PathTools.contains_illegal_characters(path):
            raise FvttmvInternalException("{0} is not ok".format(path))
