import unittest

from fvttmv.exceptions import FvttmvException
from fvttmv.reference_tools import ReferenceTools
from fvttmv.search.__references_searcher_string import ReferencesSearcherString


class ReferencesSearcherStringTest(unittest.TestCase):
    json_base_str = "\"img\":\"{0}\""
    html_base_str = "<img src=\\\"{0}\\\">"

    reference = "this/is/just/a/test"

    json_str = json_base_str.format(reference)
    html_str = html_base_str.format(reference)

    def test_contain_json_references(self):
        print("test_contain_json_references")

        result = ReferencesSearcherString._does_contain_json_references(self.json_str,
                                                                        self.reference)
        self.assertTrue(result)

    def test_contain_json_references2(self):
        print("test_contain_json_references2")

        result = ReferencesSearcherString._does_contain_json_references(self.json_str,
                                                                        "this/is/just/a")
        self.assertFalse(result)

    def test_contain_json_references3(self):
        print("test_contain_json_references3")

        result = ReferencesSearcherString._does_contain_json_references(self.json_str,
                                                                        "this/is/a/false/test")
        self.assertFalse(result)

    def test_contain_json_references4(self):
        print("test_contain_json_references4")

        result = ReferencesSearcherString._does_contain_json_references(self.html_str,
                                                                        self.reference)
        self.assertFalse(result)

    def test_contain_html_references1(self):
        print("test_contain_html_references1")

        result = ReferencesSearcherString._does_contain_html_references(self.html_str,
                                                                        self.reference)
        self.assertTrue(result)

    def test_contain_html_references2(self):
        print("test_contain_html_references2")

        result = ReferencesSearcherString._does_contain_html_references(self.html_str,
                                                                        "this/is/just/a")
        self.assertFalse(result)

    def test_contain_html_references3(self):
        print("test_contain_html_references3")

        result = ReferencesSearcherString._does_contain_html_references(self.html_str,
                                                                        "this/is/a/false/test")
        self.assertFalse(result)

    def test_contain_html_references4(self):
        print("test_contain_html_references4")

        result = ReferencesSearcherString._does_contain_html_references(self.json_str,
                                                                        self.reference)
        self.assertFalse(result)

    def test_contain_references1(self):
        print("test_contain_references1")

        result = ReferencesSearcherString.does_contain_references(self.html_str + self.json_str,
                                                                  self.reference)
        self.assertTrue(result)

    def test_contain_references2(self):
        print("test_contain_references2")

        result = ReferencesSearcherString.does_contain_references(self.html_str + self.json_str,
                                                                  "this/is/just/a")
        self.assertFalse(result)

    def test_contain_references3(self):
        print("test_contain_references3")

        result = ReferencesSearcherString.does_contain_references(self.html_str + self.json_str,
                                                                  "this/is/a/false/test")
        self.assertFalse(result)

    def test_does_references_exceptions(self):

        print("test_does_contain_html_references_exceptions")

        for char in ReferenceTools.illegal_chars:
            try:
                ReferencesSearcherString.does_contain_references(self.json_str,
                                                                 char)
                self.fail()
            except FvttmvException:
                pass
