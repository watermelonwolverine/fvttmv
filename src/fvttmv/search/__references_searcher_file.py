from fvttmv import db_file_encoding
from fvttmv.search.__references_searcher_string import ReferencesSearcherString


class ReferencesSearcherFile:
    """
    Looks for references in a single file
    """

    @staticmethod
    def search_for_references_in_file(path_to_db_file: str,
                                      reference: str) -> bool:
        data: str

        with open(path_to_db_file, "rt", encoding=db_file_encoding, newline='') as fin:
            data = fin.read()

        return ReferencesSearcherString.does_contain_references(data,
                                                                reference)
