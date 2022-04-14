import unittest

from fvttmv.exceptions import FvttmvException
from fvttmv.iterators.db_files_iterator import DbFilesIterator
from test.common import *


class DbFilesIteratorTest(unittest.TestCase):

    def setUp(self) -> None:
        Setup.setup_working_environment()

    def test_iterate_through_world_dir(self) -> None:

        print("test_iterate_through_world_dir")

        expected = [AbsPaths.contains_1_db,
                    AbsPaths.contains_2_db]

        result = []

        for db_file in DbFilesIterator.iterate_through_world_dir(AbsPaths.world1):
            result.append(db_file)

        self.assertEqual(expected, result)

    def test_iterate_through_world_dir_exception1(self):

        print("test_iterate_through_world_dir_exception1")

        try:
            for _ in DbFilesIterator.iterate_through_all_worlds("./foundrydata_copy"):
                self.fail()
        except FvttmvException:
            pass

    def test_iterate_through_world_dir_exception2(self):

        print("test_iterate_through_world_dir_exception2")

        try:
            for _ in DbFilesIterator.iterate_through_all_worlds(AbsPaths.contains_1_db):
                self.fail()
        except FvttmvException:
            pass

    def test_iterate_though_world_dir_exception3(self):

        print("test_iterate_though_world_dir_exception3")
        path_that_does_not_exist = os.path.join(AbsPaths.Data,
                                                "does_not_exist")

        try:
            for _ in DbFilesIterator.iterate_through_world_dir(path_that_does_not_exist):
                self.fail()
        except FvttmvException:
            pass

    def test_iterate_through_all_worlds(self) -> None:

        print("test_iterate_through_all_worlds")

        expected = [AbsPaths.contains_1_db,
                    AbsPaths.contains_2_db,
                    AbsPaths.contains_1_and_2_db,
                    AbsPaths.contains_none_db]

        result = []

        for db_file in DbFilesIterator.iterate_through_all_worlds(AbsPaths.Data):
            result.append(db_file)

        self.assertEqual(expected, result)
