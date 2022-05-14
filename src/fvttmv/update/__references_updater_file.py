import logging

from fvttmv import db_file_encoding
from fvttmv.exceptions import FvttmvException
from fvttmv.update.__references_updater_string import ReferencesUpdaterString
from fvttmv.update.__update_context import UpdateContext


class ReferencesUpdaterFile:

    @staticmethod
    def replace_references_in_file(path_to_db_file: str,
                                   old_reference: str,
                                   new_reference: str) -> None:
        logging.debug("Replacing references to %s with %s in %s",
                      old_reference,
                      new_reference,
                      path_to_db_file)

        data: str

        try:
            with open(path_to_db_file, "rt", encoding=db_file_encoding, newline='') as fin:
                data = fin.read()
        except Exception as ex:
            raise FvttmvException(
                "Exception: {0}. Unable to read file {1} as UTF-8. Is this file a correct db file?".format(
                    ex,
                    path_to_db_file))

        update_context = UpdateContext(data)

        ReferencesUpdaterString.replace_references(update_context,
                                                   old_reference,
                                                   new_reference)

        if not update_context.data_was_updated:
            logging.debug("No references found in %s.", path_to_db_file)
            return

        try:
            with open(path_to_db_file, "wt", encoding=db_file_encoding, newline='') as fout:
                fout.write(update_context.data)
                fout.flush()
                logging.info("Updated %s", path_to_db_file)
        except Exception as ex:
            raise FvttmvException(
                "Exception: {0}. Unable to write to file {1}. Do you have the write permissions?".format(
                    ex,
                    path_to_db_file))
