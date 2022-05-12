from fvttmv.search.__references_searcher_db_files import ReferencesSearcherDbFiles
from test.common import TestCase, AbsPaths, References


class ReferencesSearcherDbFilesTest(TestCase):

    def test_search_for_references_in_db_files1(self):
        print("test_search_for_references_in_db_files1")

        expected = []

        result = ReferencesSearcherDbFiles.search_for_references_in_db_files(AbsPaths.Data,
                                                                             "does/not/exist")

        self.assertEqual(result, expected)

    def test_search_for_references_in_db_files2(self):
        print("test_search_for_references_in_db_files2")

        expected = [AbsPaths.contains_1_db,
                    AbsPaths.contains_1_and_2_db]

        result = ReferencesSearcherDbFiles.search_for_references_in_db_files(AbsPaths.Data,
                                                                             References.file1_original)

        self.assertEqual(expected, result)
