import unittest
from typing import List

from fvttmv.exceptions import FvttmvException
from fvttmv.iterators.directory_walker import DirectoryWalker, DirectoryWalkerCallback
from test.common import *


class DirectoryWalkerCallbackImpl(DirectoryWalkerCallback):
    result: List[str] = []

    def process_file(self, abs_path_to_file: str) -> None:
        self.result.append(abs_path_to_file)

    def step_into_directory(self, abs_path_to_directory: str) -> None:
        self.result.append("in: " + abs_path_to_directory)

    def step_out_of_directory(self, abs_path_to_directory: str) -> None:
        self.result.append("out: " + abs_path_to_directory)


class DirectoryWalkerTest(unittest.TestCase):
    directory_walker_callback_impl: DirectoryWalkerCallbackImpl
    directory_walker: DirectoryWalker

    def setUp(self) -> None:
        Setup.setup_working_environment()
        self.directory_walker_callback_impl = DirectoryWalkerCallbackImpl()
        self.directory_walker = DirectoryWalker(self.directory_walker_callback_impl)

    def test_walk_directory(self):

        print("test_walk_directory")

        abs_path_to_assets_dir = AbsPaths.assets

        self.directory_walker.walk_directory(abs_path_to_assets_dir)

        expected = ["in: " + AbsPaths.images,
                    AbsPaths.file1_png,
                    AbsPaths.file2_png,
                    "in: " + AbsPaths.sub_folder,
                    AbsPaths.file3_png,
                    "out: " + AbsPaths.sub_folder,
                    "out: " + AbsPaths.images]

        result = self.directory_walker_callback_impl.result

        self.assertEqual(result, expected)

    def test_walk_directory_exceptions(self):

        print("test_walk_directory_exceptions")

        try:
            self.directory_walker.walk_directory(C.foundrydata)
            self.fail()
        except FvttmvException:
            pass

        path_that_is_not_a_directory = AbsPaths.contains_1_db

        try:
            self.directory_walker.walk_directory(path_that_is_not_a_directory)
            self.fail()
        except FvttmvException:
            pass

        path_that_does_not_exist = os.path.join(AbsPaths.Data, "does_not_exist")

        try:
            self.directory_walker.walk_directory(path_that_does_not_exist)
            self.fail()
        except FvttmvException:
            pass
