from fvttmv.update.references_updater import ReferencesUpdater
from test.common import TestCase, AbsPaths, References, DataStrings, utf_8


class ReferencesUpdaterTest(TestCase):

    def test_replace_references(self):
        referencesUpdater = ReferencesUpdater(AbsPaths.Data,
                                              [])

        referencesUpdater.replace_references(References.file1_original,
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
