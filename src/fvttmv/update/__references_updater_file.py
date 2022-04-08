import logging

from fvttmv.update.__references_updater_string import ReferencesUpdaterString
from fvttmv.update.__update_context import UpdateContext


class ReferencesUpdaterFile:

    @staticmethod
    def replace_references_in_file(path_to_db_file: str,
                                   old_reference: str,
                                   new_reference: str) -> None:
        logging.info("Replacing references to %s with %s in %s",
                     old_reference,
                     new_reference,
                     path_to_db_file)

        data: str

        with open(path_to_db_file, "rt", encoding="utf-8", newline='') as fin:
            data = fin.read()

        update_context = UpdateContext(data)

        ReferencesUpdaterString.replace_references(update_context,
                                                   old_reference,
                                                   new_reference)

        if not update_context.data_was_updated:
            logging.info("No references found in %s.", path_to_db_file)
            return

        with open(path_to_db_file, "wt", encoding="utf-8", newline='') as fout:
            fout.write(update_context.data)
            fout.flush()
            logging.info("Updated %s", path_to_db_file)
