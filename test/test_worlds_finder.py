import unittest

from fvttmv.exceptions import FvttmvException
from fvttmv.wolds_finder import WorldsFinder
from test.common import *


class WorldsFinderTest(unittest.TestCase):
    worlds_finder: WorldsFinder

    def setUp(self) -> None:
        Setup.setup_working_environment()
        self.worlds_finder = WorldsFinder(AbsPaths.Data)

    def test_constructor_exceptions(self):

        print("test_constructor_exceptions")

        relative_path = os.path.join(C.foundrydata, C.Data)

        try:
            WorldsFinder(relative_path)
            self.fail()
        except FvttmvException:
            pass

        path_that_is_not_a_directory = os.path.abspath("Data")

        try:
            WorldsFinder(path_that_is_not_a_directory)
            self.fail()
        except FvttmvException:
            pass

        path_that_does_not_exist = os.path.join(AbsPaths.Data,
                                                "does_not_exist",
                                                C.Data)
        try:
            WorldsFinder(path_that_does_not_exist)
            self.fail()
        except FvttmvException:
            pass

        path_not_normalized = os.path.join(AbsPaths.Data, "..", C.Data)

        try:
            WorldsFinder(path_not_normalized)
            self.fail()
        except FvttmvException:
            pass

    def test_is_path_a_world_dir(self):

        print("test_is_path_a_world_dir")

        result = self.worlds_finder.is_path_a_world_dir(AbsPaths.world1)

        self.assertTrue(result)

        result = self.worlds_finder.is_path_a_world_dir(AbsPaths.not_a_world1)

        self.assertFalse(result)

    def test_get_paths_to_worlds(self):
        print("test_get_paths_to_worlds")

        result = self.worlds_finder.get_paths_to_worlds()
        expected = [AbsPaths.world1, AbsPaths.world2]

        self.assertEqual(result, expected)
