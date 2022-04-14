import unittest

from fvttmv.update.references_updater import ReferencesUpdater
from test.common import *


class ReferencesUpdaterTest(unittest.TestCase):

    def setUp(self) -> None:
        Setup.setup_working_environment()

    def test_replace_references(self):
        ReferencesUpdater._do_replace_references(AbsPaths.Data,
                                                 References.file1_original,
                                                 References.file1_replacement)

        with open(AbsPaths.contains_1_db, "r", encoding="utf-8", newline='') as fin:
            data = fin.read()
            self.assertEqual(data,
                             DataStrings.contains_1_changed)

        with open(AbsPaths.contains_2_db, "r", encoding="utf-8", newline='') as fin:
            data = fin.read()
            self.assertEqual(data,
                             DataStrings.contains_2_original)

        with open(AbsPaths.contains_1_and_2_db, "r", encoding="utf-8", newline='') as fin:
            data = fin.read()
            self.assertEqual(data,
                             DataStrings.contains_1_and_2_changed)

        with open(AbsPaths.contains_none_db, "r", encoding="utf-8", newline='') as fin:
            data = fin.read()
            self.assertEqual(data,
                             DataStrings.contains_none)

        with open(AbsPaths.not_a_db_txt, "r", encoding="utf-8", newline='') as fin:
            data = fin.read()
            self.assertEqual(data,
                             DataStrings.not_a_db)

        with open(AbsPaths.should_not_be_touched_db, "r", encoding=utf_8, newline='') as fin:
            data = fin.read()
            self.assertEqual(data,
                             DataStrings.should_not_be_touched_db)

        with open(AbsPaths.thumbs_db, "r", encoding=utf_8, newline='') as fin:
            data = fin.read()
            self.assertEqual(data,
                             DataStrings.thumbs_db)
