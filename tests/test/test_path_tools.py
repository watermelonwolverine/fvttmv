import os.path
import unittest

from fvttmv.exceptions import FvttmvException
from fvttmv.path_tools import PathTools
from test.common import *


class PathToolsTest(unittest.TestCase):
    path_tools: PathTools

    def setUp(self):
        Setup.setup_working_environment()
        self.path_tools = PathTools(AbsPaths.Data)

    def test_constructor_exceptions(self):

        print("test_constructor_exceptions")

        relative_path = os.path.join(C.foundrydata, C.data)

        try:
            PathTools(relative_path)
            self.fail()
        except FvttmvException:
            pass

        path_that_is_not_a_directory = os.path.abspath(C.Data)

        try:
            PathTools(path_that_is_not_a_directory)
            self.fail()
        except FvttmvException:
            pass

        path_that_does_not_exist = os.path.join(AbsPaths.Data,
                                                "does_not_exist",
                                                C.Data)
        try:
            PathTools(path_that_does_not_exist)
            self.fail()
        except FvttmvException:
            pass

        path_not_normalized = os.path.join(AbsPaths.Data, "..", C.Data)

        try:
            PathTools(path_not_normalized)
            self.fail()
        except FvttmvException:
            pass

    def test_is_normalized_path1(self):

        print("test_is_normalized_path1")

        path_not_normalized = os.path.join(AbsPaths.Data, "..", C.Data, C.worlds)

        result = PathTools.is_normalized_path(path_not_normalized)

        self.assertFalse(result)

    def test_is_normalized_path2(self):
        print("test_is_normalized_path2")

        path_normalized = AbsPaths.worlds

        result = PathTools.is_normalized_path(path_normalized)

        self.assertTrue(result)

    def test_is_normalized_path3(self):
        print("test_is_normalized_path3")

        path_normalized = AbsPaths.worlds

        path_normalized += os.path.sep

        result = PathTools.is_normalized_path(path_normalized)

        self.assertTrue(result)

    def test_make_path_relative_to_foundry_data(self):

        print("test_make_path_relative_to_foundry_data")

        path_within_foundry_data = AbsPaths.world1

        expected = RelPaths.world1

        result = self.path_tools.make_path_relative_to_foundry_data(path_within_foundry_data)

        self.assertEqual(result, expected)

    def test_make_path_relative_to_foundry_data_exceptions(self):

        print("test_make_path_relative_to_foundry_data_exceptions")

        path_not_normalized = os.path.join(AbsPaths.Data, "..", C.Data, C.worlds)

        try:
            self.path_tools.make_path_relative_to_foundry_data(path_not_normalized)
            self.fail()
        except FvttmvException:
            pass

        path_outside_of_foundry_data = os.path.normpath(os.path.join(AbsPaths.Data, "..", C.Logs))

        try:
            self.path_tools.make_path_relative_to_foundry_data(path_outside_of_foundry_data)
            self.fail()
        except FvttmvException:
            pass

        relative_path = os.path.join(C.foundrydata, C.data, C.assets)

        try:
            self.path_tools.make_path_relative_to_foundry_data(relative_path)
            self.fail()
        except FvttmvException:
            pass

    def test_ends_with_separator1(self):

        print("test_ends_with_separator")

        result = PathTools.ends_with_separator(AbsPaths.Data + "\\")

        self.assertEqual(result, True)

    def test_ends_with_separator2(self):

        print("test_ends_with_separator")

        result = PathTools.ends_with_separator(AbsPaths.Data + "/")

        self.assertEqual(result, True)

    def test_contains_illegal_character(self):
        print("test_contains_illegal_character")

        for char in ["*", "\"", ":", "|"]:
            result = PathTools.contains_illegal_characters(AbsPaths.Data + char)

            self.assertEqual(result, True)

    def test_get_correctly_case_path1(self):
        print("test_get_correctly_case_path1")

        dir_path = os.path.join(AbsPaths.Data, "folder_name[")

        os.mkdir(dir_path)

        result = PathTools.get_correctly_cased_path(dir_path.upper())

        self.assertEqual(dir_path, result)

    def test_get_correctly_case_path2(self):
        print("test_get_correctly_case_path2")

        dir_path = os.path.join(AbsPaths.Data, "folder_name]")

        os.mkdir(dir_path)

        result = PathTools.get_correctly_cased_path(dir_path.upper())

        self.assertEqual(dir_path, result)

    def test_get_correctly_case_path3(self):
        print("test_get_correctly_case_path3")

        dir_path = os.path.join(AbsPaths.Data, "folder_name[blabla]")

        os.mkdir(dir_path)

        result = PathTools.get_correctly_cased_path(dir_path.upper())

        self.assertEqual(dir_path, result)

    def test_get_correctly_case_path4(self):
        print("test_get_correctly_case_path4")

        dir_path = os.path.join(AbsPaths.Data, "[folder_name")

        os.mkdir(dir_path)

        result = PathTools.get_correctly_cased_path(dir_path.upper())

        self.assertEqual(dir_path, result)

    def test_get_correctly_case_path5(self):
        print("test_get_correctly_case_path5")

        dir_path = os.path.join(AbsPaths.Data, "]folder_name")

        os.mkdir(dir_path)

        result = PathTools.get_correctly_cased_path(dir_path.upper())

        self.assertEqual(dir_path, result)

    def test_get_correctly_case_path6(self):
        print("test_get_correctly_case_path6")

        dir_path = os.path.join(AbsPaths.Data, "][folder_name]")

        os.mkdir(dir_path)

        result = PathTools.get_correctly_cased_path(dir_path.upper())

        self.assertEqual(dir_path, result)