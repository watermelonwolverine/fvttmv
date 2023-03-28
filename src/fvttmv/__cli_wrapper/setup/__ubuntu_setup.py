import json
import os
import sys
from typing import List

from fvttmv.config import Keys
from .__common import ask_yes_or_no_question
from ..__constants import win32, linux
from ...exceptions import FvttmvException, FvttmvInternalException

cancelled_setup = "Cancelled setup."


def __get_foundry_data_example() -> str:
    platform = sys.platform

    if platform == win32:
        return "C:\\Users\\User\\AppData\\Local\\FoundryVTT\\Data"
    if platform == linux:
        return "/home/user/.local/share/FoundryVTT"

    raise FvttmvInternalException(f"Unsupported Platform {platform}")


def __check_folder_name(abs_path_to_foundry_data: str) -> None:
    if not os.path.split(abs_path_to_foundry_data)[1] == "Data":
        query = "The entered path does lead to a 'Data' directory. Make sure you entered the right one. " \
                "Do you want to continue?"

        should_continue = ask_yes_or_no_question(query)

        if not should_continue:
            raise FvttmvException(cancelled_setup)


def __check_existence(abs_path_to_foundry_data: str) -> None:
    if not os.path.exists(abs_path_to_foundry_data):
        should_continue = ask_yes_or_no_question(f"'{abs_path_to_foundry_data}' does not exist. "
                                                 "Do you want to continue?")

        if not should_continue:
            raise FvttmvException(cancelled_setup)


def __query_path_to_foundry_data() -> str:
    query = "Enter path to the 'Data' folder of your foundry data" \
            f" (for example {__get_foundry_data_example()})"

    path_to_foundry_data = input(query)

    abs_path_to_foundry_data = os.path.abspath(path_to_foundry_data)

    __check_folder_name(abs_path_to_foundry_data)

    __check_existence(abs_path_to_foundry_data)

    return abs_path_to_foundry_data


def __ask_for_additional_target_to_update(abs_path_to_foundry_data: str) -> str:
    raise NotImplementedError()


def __query_additional_targets(abs_path_to_foundry_data: str) -> List[str]:
    query = "You can add additional targets to update. The main reason to do this is to update references in " \
            "shared compendiums. Do you want to add additional targets?"

    wants_to_add = ask_yes_or_no_question(query)

    if not wants_to_add:
        return []

    result = []

    while True:
        additional_target = __ask_for_additional_target_to_update(abs_path_to_foundry_data)

        result.append(additional_target)

        wants_to_add_more = ask_yes_or_no_question("Do you want to add another additional target?")

        if not wants_to_add_more:
            break

    return result


def ubuntu_setup():

    abs_path_to_foundry_data = __query_path_to_foundry_data()

    additional_targets_to_update = __query_additional_targets(abs_path_to_foundry_data)

    while True:
        wants_to_add_additional_target = input("Do you want to add an additional target to update (for example "
                                               "/home/user/foundrydata/Data/modules/shared-module/packs)?")
        if wants_to_add_additional_target:
            path_to_additional_target = input("Enter the path to the target: ")

            abs_path_to_additional_target = os.path.abspath(os.path.normpath(path_to_additional_target))

            if not path_tools.is_in_foundry_data(abs_path_to_additional_target):
                print("Error: The given path is not inside the 'Data' directory. The path was not added.")
                continue

            additional_targets_to_update.append(abs_path_to_additional_target)

        else:
            break

    config_dict = \
        {
            Keys.absolute_path_to_foundry_data_key: path_to_foundry_data,
            Keys.additional_targets_to_update: additional_targets_to_update
        }

    try:

        with open(path_to_config_file_linux, "w+", encoding="utf-8") as config_fout:
            json.dump(config_dict, config_fout)
            print("Created config file {0}".format(path_to_config_file_linux))
    except BaseException as error:
        print(error)
        print("Unable to write config file to {0}. Cancelling installation...".format(path_to_config_file_linux))
        exit()

    print("Setup completed")
