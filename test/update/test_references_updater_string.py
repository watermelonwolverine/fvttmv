import unittest

from fvttmv.exceptions import FvttmvException
from fvttmv.reference_tools import ReferenceTools
from fvttmv.update.references_updater_string import ReferencesUpdaterString
from fvttmv.update.update_context import UpdateContext
from test.common import DataStrings, References


class ReferencesUpdaterTextTest(unittest.TestCase):
    original_reference = References.file1_original
    replacement_reference = References.file1_replacement

    json_original = DataStrings.json_base_str.format(original_reference)
    html_original = DataStrings.html_base_str.format(original_reference)

    json_with_replaced_reference = DataStrings.json_base_str.format(replacement_reference)
    html_with_replaced_reference = DataStrings.html_base_str.format(replacement_reference)

    def test_replace_json_references1(self):
        print("test_replace_json_references1")

        update_context = UpdateContext(self.json_original)

        ReferencesUpdaterString._replace_json_references(update_context,
                                                         self.original_reference,
                                                         self.replacement_reference)

        self.assertTrue(update_context.data_was_updated)
        self.assertEqual(update_context.data,
                         self.json_with_replaced_reference)

    def test_replace_json_references2(self):
        print("test_replace_json_references2")
        data = DataStrings.json_base_str.format(self.original_reference + "/with/addition")

        update_context = UpdateContext(data)

        ReferencesUpdaterString._replace_json_references(update_context,
                                                         self.original_reference,
                                                         self.replacement_reference)
        self.assertFalse(update_context.data_was_updated)
        self.assertEqual(data,
                         update_context.data)

    def test_replace_json_references3(self):

        print("test_replace_json_references3")
        data = DataStrings.json_base_str.format("this/is/just/a")

        update_context = UpdateContext(data)

        ReferencesUpdaterString._replace_json_references(update_context,
                                                         self.original_reference,
                                                         self.replacement_reference)
        self.assertFalse(update_context.data_was_updated)
        self.assertEqual(data,
                         update_context.data)

    def test_replace_json_references4(self):
        print("test_replace_json_references4")

        update_context = UpdateContext(self.html_original)

        ReferencesUpdaterString._replace_json_references(update_context,
                                                         self.original_reference,
                                                         self.replacement_reference)
        self.assertFalse(update_context.data_was_updated)
        self.assertEqual(self.html_original,
                         update_context.data)

    def test_replace_html_references1(self):
        print("test_replace_html_references1")

        update_context = UpdateContext(self.html_original)

        ReferencesUpdaterString._replace_html_references(update_context,
                                                         self.original_reference,
                                                         self.replacement_reference)

        self.assertTrue(update_context.data_was_updated)
        self.assertEqual(update_context.data,
                         self.html_with_replaced_reference)

    def test_replace_html_references2(self):
        print("test_replace_html_references2")

        data = DataStrings.json_base_str.format(self.original_reference + "/with/addition")

        update_context = UpdateContext(data)

        ReferencesUpdaterString._replace_html_references(update_context,
                                                         self.original_reference,
                                                         self.replacement_reference)
        self.assertFalse(update_context.data_was_updated)
        self.assertEqual(data,
                         update_context.data)

    def test_replace_html_references3(self):
        print("test_replace_html_references3")

        data = DataStrings.json_base_str.format("this/is/just/a")

        update_context = UpdateContext(data)

        ReferencesUpdaterString._replace_html_references(update_context,
                                                         self.original_reference,
                                                         self.replacement_reference)
        self.assertFalse(update_context.data_was_updated)
        self.assertEqual(data,
                         update_context.data)

    def test_replace_html_references4(self):
        print("test_replace_html_references4")

        update_context = UpdateContext(self.json_original)

        ReferencesUpdaterString._replace_html_references(update_context,
                                                         self.original_reference,
                                                         self.replacement_reference)
        self.assertFalse(update_context.data_was_updated)
        self.assertEqual(self.json_original,
                         update_context.data)

    def test_replace_references1(self):
        print("test_replace_references1")

        data = self.json_original + self.json_original + self.html_original + self.html_original

        update_context = UpdateContext(data)

        ReferencesUpdaterString.replace_references(update_context,
                                                   self.original_reference,
                                                   self.replacement_reference)

        expected_data = self.json_with_replaced_reference + self.json_with_replaced_reference
        expected_data += self.html_with_replaced_reference + self.html_with_replaced_reference

        self.assertTrue(update_context.data_was_updated)
        self.assertEqual(expected_data,
                         update_context.data)

    def test_replace_references_exceptions1(self):

        print("test_replace_references_exceptions1")

        data = self.json_original + self.html_original

        update_context = UpdateContext(data)

        for char in ReferenceTools.illegal_chars:
            try:
                ReferencesUpdaterString.replace_references(update_context,
                                                           self.original_reference + "/" + char,
                                                           self.replacement_reference)
                self.fail()
            except FvttmvException:
                self.assertFalse(update_context.data_was_updated)
                self.assertEqual(update_context.data,
                                 data)

    def test_replace_references_exceptions2(self):

        print("test_replace_references_exceptions2")

        data = self.json_original + self.html_original

        update_context = UpdateContext(data)

        for char in ReferenceTools.illegal_chars:
            try:
                ReferencesUpdaterString.replace_references(update_context,
                                                           self.original_reference,
                                                           self.replacement_reference + "/" + char)
                self.fail()
            except FvttmvException:
                self.assertFalse(update_context.data_was_updated)
                self.assertEqual(update_context.data,
                                 data)

    def test_replace_references_exceptions3(self):

        print("test_replace_references_exceptions3")

        data = self.json_original + self.html_original

        update_context = UpdateContext(data)

        try:
            ReferencesUpdaterString.replace_references(update_context,
                                                       self.original_reference,
                                                       "/" + self.replacement_reference)
            self.fail()
        except FvttmvException:
            self.assertFalse(update_context.data_was_updated)
            self.assertEqual(update_context.data,
                             data)
