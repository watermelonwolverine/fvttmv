import unittest

from fvttmv.update.references_updater_file import ReferencesUpdaterFile
from test.common import Setup, References, AbsPaths, DataStrings


class ReferencesUpdaterFileTest(unittest.TestCase):

    def setUp(self) -> None:
        Setup.setup_working_environment()

    def test_replace_references_in_file1(self):
        print("test_replace_references_in_file1")

        ReferencesUpdaterFile.replace_references_in_file(AbsPaths.contains_2_db,
                                                         References.file1_original,
                                                         References.file1_replacement)
        data: str

        with open(AbsPaths.contains_2_db, "r", encoding="utf-8", newline='') as fin:
            data = fin.read()

        self.assertEqual(DataStrings.contains_2_original,
                         data)

    def test_replace_references_in_file2(self):
        print("test_replace_references_in_file2")

        ReferencesUpdaterFile.replace_references_in_file(AbsPaths.contains_1_db,
                                                         References.file1_original,
                                                         References.file1_replacement)
        data: str

        with open(AbsPaths.contains_1_db, "r", encoding="utf-8", newline='') as fin:
            data = fin.read()

        self.assertEqual(DataStrings.contains_1_changed,
                         data)
