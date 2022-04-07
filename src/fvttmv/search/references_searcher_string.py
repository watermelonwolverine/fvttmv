from fvttmv.exceptions import FvttmvException
from fvttmv.reference_tools import ReferenceTools


class ReferencesSearcherString:
    """
    Contains functions for searching for json and html references.
    Very similar to ReferencesReplacer in functionality
    """

    @staticmethod
    def does_contain_references(data: str,
                                reference: str) -> bool:

        if ReferenceTools.does_contain_illegal_char(reference):
            raise FvttmvException()

        found_reference = ReferencesSearcherString._does_contain_json_references(data,
                                                                                 reference)
        if not found_reference:
            found_reference = ReferencesSearcherString._does_contain_html_references(data,
                                                                                     reference)
        return found_reference

    @staticmethod
    def _does_contain_html_references(data: str,
                                      reference: str) -> bool:

        text_to_find = "src=\\\"{0}\\\"".format(reference)

        return data.find(text_to_find) != -1

    @staticmethod
    def _does_contain_json_references(data: str,
                                      reference: str) -> bool:

        text_to_find = "\":\"{0}\"".format(reference)

        return data.find(text_to_find) != -1
