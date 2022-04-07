import unittest

from fvttmv.exceptions import FvttmvException
from test.common import *

from fvttmv.iterators.db_files_iterator import DbFilesIterator


class DbFilesIteratorTest(unittest.TestCase):

    def setUp(self) -> None:
        Setup.setup_working_environment()

    def test_iterate_through_directory(self) -> None:

        print("test_iterate_through_directory")

        expected = [AbsPaths.contains_1_db,
                    AbsPaths.contains_2_db]

        result = []

        for db_file in DbFilesIterator.iterate_through_directory(AbsPaths.world1):
            result.append(db_file)

        self.assertEqual(expected, result)

    def test_iterate_through_directory_exceptions(self):

        print("test_iterate_through_directory_exceptions")

        try:
            for _ in DbFilesIterator.iterate_through_directory("./foundrydata_copy"):
                self.fail()
        except FvttmvException:
            pass

        try:
            for _ in DbFilesIterator.iterate_through_directory(AbsPaths.contains_1_db):
                self.fail()
        except FvttmvException:
            pass

        path_that_does_not_exist = os.path.join(AbsPaths.Data,
                                                "does_not_exist")

        try:
            for _ in DbFilesIterator.iterate_through_directory(path_that_does_not_exist):
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
