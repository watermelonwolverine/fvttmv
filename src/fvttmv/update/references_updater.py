from fvttmv.__checks import check_path_to_foundry_data
from fvttmv.exceptions import FvttmvException
from fvttmv.iterators.db_files_iterator import DbFilesIterator
from fvttmv.update.__references_updater_file import ReferencesUpdaterFile


class ReferencesUpdater:
    __abs_path_to_foundry_data: str

    def __init__(self,
                 abs_path_to_foundry_data: str):

        if not check_path_to_foundry_data(abs_path_to_foundry_data):
            raise FvttmvException("abs_path_to_foundry_data is not ok")

        self.__abs_path_to_foundry_data = abs_path_to_foundry_data

    def replace_references(self,
                           old_reference: str,
                           new_reference: str):

        self._do_replace_references(self.__abs_path_to_foundry_data,
                                    old_reference,
                                    new_reference)

    @staticmethod
    def _do_replace_references(abs_path_to_foundry_data: str,
                               old_reference: str,
                               new_reference: str):
        db_files_iterator = DbFilesIterator()

        for db_file in db_files_iterator.iterate_through_all_worlds(
                abs_path_to_foundry_data):
            ReferencesUpdaterFile.replace_references_in_file(db_file,
                                                             old_reference,
                                                             new_reference)
