import json
import os

from cli_wrapper.__constants import path_to_config_file_linux
from cli_wrapper.__setup import ask_yes_or_no_question
from fvttmv.config import Keys
from fvttmv.path_tools import PathTools


def ubuntu_setup():
    path_to_foundry_data = input("Enter path to the 'Data' folder of your foundry data (for example "
                                 "/home/user/foundrydata/Data): ")

    if not path_to_foundry_data.endswith("Data"):

        should_continue = ask_yes_or_no_question(
            "The entered path does end with Data. Make sure you entered the right one. "
            "Do you want to continue?")

        if not should_continue:
            print("Cancelling installation...")
            exit()

    abs_path_to_foundry_data = os.path.abspath(os.path.normpath(path_to_foundry_data))

    if not os.path.exists(path_to_foundry_data):

        should_continue = ask_yes_or_no_question("The entered path does not exist. "
                                                 "Do you want to continue?")

        if not should_continue:
            print("Cancelling installation...")
            exit()

    path_tools = PathTools(abs_path_to_foundry_data)

    additional_targets_to_update = []

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
