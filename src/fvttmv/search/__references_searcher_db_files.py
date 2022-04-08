from typing import List

from fvttmv.iterators.db_files_iterator import DbFilesIterator
from fvttmv.search.__references_searcher_file import ReferencesSearcherFile


class ReferencesSearcherDbFiles:
    """
    Searches for references in all *.db files of all worlds
    """

    @staticmethod
    def search_for_references_in_db_files(
            abs_path_to_foundry_data: str,
            reference: str) -> List[str]:
        """
        Searches all references of all *.db files of all worlds
        """
        db_files_iterator = DbFilesIterator()

        result = []

        for abs_path_to_db_file in db_files_iterator.iterate_through_all_worlds(abs_path_to_foundry_data):
            if ReferencesSearcherFile.search_for_references_in_file(abs_path_to_db_file,
                                                                    reference):
                result.append(abs_path_to_db_file)

        return result
