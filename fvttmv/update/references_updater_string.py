import logging

from fvttmv.exceptions import FvttmvException
from fvttmv.reference_tools import ReferenceTools
from fvttmv.update.update_context import UpdateContext


class ReferencesUpdaterString:
    """
    Contains functions for replacing json and html references in strings
    """

    @staticmethod
    def replace_references(update_context: UpdateContext,
                           old_reference: str,
                           new_reference: str) -> None:
        if ReferenceTools.does_contain_illegal_char(old_reference) or \
                ReferenceTools.does_contain_illegal_char(new_reference) \
                or new_reference.startswith("/"):
            raise FvttmvException()

        ReferencesUpdaterString._replace_html_references(update_context,
                                                         old_reference,
                                                         new_reference)

        ReferencesUpdaterString._replace_json_references(update_context,
                                                         old_reference,
                                                         new_reference)

    @staticmethod
    def _replace_html_references(update_context: UpdateContext,
                                 old_reference: str,
                                 new_reference: str) -> None:
        data = update_context.data

        base_text = "src=\\\"{0}\\\""

        text_to_replace = base_text.format(old_reference)

        new_text = base_text.format(new_reference)

        if data.find(text_to_replace) == -1:
            return

        updated_data = data.replace(text_to_replace,
                                    new_text)

        update_context.override_data(updated_data)

        logging.debug("Found and replaced html reference to %s with %s",
                      old_reference,
                      new_reference)

    @staticmethod
    def _replace_json_references(update_context: UpdateContext,
                                 old_reference: str,
                                 new_reference: str) -> None:
        base_text = "\":\"{0}\""

        text_to_replace = base_text.format(old_reference)

        new_text = base_text.format(new_reference)

        data = update_context.data

        if data.find(text_to_replace) == -1:
            return

        updated_data = data.replace(text_to_replace,
                                    new_text)

        update_context.override_data(updated_data)

        logging.debug("Found and replaced json reference to %s with %s",
                      old_reference,
                      new_reference)
