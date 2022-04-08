import unittest

from fvttmv.search.__references_searcher_file import ReferencesSearcherFile
from test.common import *


class ReferencesSearcherFileTest(unittest.TestCase):

    def setUp(self) -> None:
        Setup.setup_working_environment()

    def test_search_for_references_in_file(self):
        print("test_search_for_references_in_file")

        result = ReferencesSearcherFile.search_for_references_in_file(AbsPaths.contains_1_db,
                                                                      References.file1_original)

        self.assertTrue(result)

        result = ReferencesSearcherFile.search_for_references_in_file(AbsPaths.contains_2_db,
                                                                      References.file1_original)

        self.assertFalse(result)
