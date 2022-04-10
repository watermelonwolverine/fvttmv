import glob
import os.path
import sys

from fvttmv.exceptions import FvttmvException, FvttmvInternalException
from fvttmv.reference_tools import ReferenceTools


class PathTools:
    abs_path_to_foundry_data: str

    def __init__(self,
                 absolute_path_to_foundry_data: str):

        PathTools.assert_path_format_is_ok(absolute_path_to_foundry_data)

        if not os.path.isdir(absolute_path_to_foundry_data):
            raise FvttmvException("Configured Foundry VTT Data folder does not exist.")

        self.abs_path_to_foundry_data = absolute_path_to_foundry_data

    def create_reference_from_absolute_path(self,
                                            absolute_path: str) -> str:

        rel_path = self.make_path_relative_to_foundry_data(absolute_path)

        result = ReferenceTools.create_reference_from_relative_path(rel_path)

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

        if PathTools.paths_are_the_same(absolute_path, self.abs_path_to_foundry_data):
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

        return PathTools.paths_are_the_same(common_path, absolute_parent_path)

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

    @staticmethod
    def filesystem_is_case_sensitive():
        if sys.platform == "win32":
            return True
        if sys.platform == "linux":
            return False
        else:
            raise FvttmvInternalException("Unsupported Platform")

    @staticmethod
    def maybe_lower_case_path(path: str):
        if PathTools.filesystem_is_case_sensitive():
            return path.lower()
        else:
            return path

    @staticmethod
    def paths_are_the_same(path1: str,
                           path2: str):
        return PathTools.maybe_lower_case_path(path1) == PathTools.maybe_lower_case_path(path2)

    @staticmethod
    def get_correctly_cased_path(abs_path):

        if not os.path.exists(abs_path):
            raise FvttmvException("Cannot correctly case path that does not exist: %s" % abs_path)

        PathTools.assert_path_format_is_ok(abs_path)

        if sys.platform == "linux":
            return abs_path
        if sys.platform == "win32":
            return PathTools.__get_correctly_case_windows_path(abs_path)

    @staticmethod
    def __get_correctly_case_windows_path(abs_path: str):

        splits = abs_path.split('\\')

        # disk letter
        wildcard_expression = [splits[0].upper()]
        for name in splits[1:]:
            wildcard_expression.append(PathTools.__prepare_name_for_glob(name))

        res = glob.glob('\\'.join(wildcard_expression))
        if len(res) != 1:
            raise FvttmvInternalException("Unable to correctly case windows path: %s" % abs_path)

        return res[0]

    @staticmethod
    def __prepare_name_for_glob(name: str):

        escaped_name = glob.escape(name)

        upper = escaped_name.upper()
        lower = escaped_name.lower()

        index_of_difference: int = -1

        for i in range(0, len(upper)):
            if upper[i] != lower[i]:
                index_of_difference = i
                break

        if index_of_difference == -1:
            # nothing to do
            return escaped_name

        # noinspection PyPep8
        result = lower[0:index_of_difference] + \
                 "[" + lower[index_of_difference] + "]" \
                 + lower[index_of_difference + 1:]

        return result
