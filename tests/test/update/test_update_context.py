import unittest

from fvttmv.update.update_context import UpdateContext
from test.common import *


class UpdateContextTest(unittest.TestCase):

    def test_init(self):
        print("test_init")

        data = DataStrings.contains_1_and_2_original

        update_context = UpdateContext(data)

        self.assertFalse(update_context.data_was_updated)
        self.assertEqual(update_context.data,
                         data)

    def test_set_data(self):
        print("test_set_data")

        data = DataStrings.contains_1_and_2_original
        new_data = DataStrings.contains_1_and_2_changed

        update_context = UpdateContext(data)

        update_context.override_data(new_data)

        self.assertTrue(update_context.data_was_updated)
        self.assertEqual(update_context.data,
                         new_data)
