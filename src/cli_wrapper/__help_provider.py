import os
import sys

from cli_wrapper.__help_texts import read_me_for_ubuntu, read_me_for_windows
from fvttmv.exceptions import FvttmvException


def __generate_readme_md_file():
    path_to_readme = os.path.abspath("README.md")

    if os.path.exists(path_to_readme):
        print("Cannot generate README at {0}. File already exists.\n".format(path_to_readme))
        return

    platform = sys.platform

    readme_text: str
    if platform == "linux":
        readme_text = read_me_for_ubuntu
    elif platform == "win32":
        readme_text = read_me_for_windows
    else:
        raise FvttmvException("Unsupported system: {0}".format(platform))

    with open(path_to_readme, "wt+", encoding="UTF-8") as fh:
        fh.write(readme_text)

    print("Generated README at {0}\n".format(path_to_readme))


def __maybe_generate_readme_md_file():
    yes = "yes"
    no = "no"

    user_input = input("Do you want me to generate a new README.md? Enter {0} or {1} (default: {1}):\n"
                       .format(yes, no))

    if user_input not in [yes, no, ""]:
        print("Unknown option: {0}, assuming {1}".format(user_input, no))

    if user_input == yes:
        __generate_readme_md_file()
        input("Press ENTER to continue.")


def tell_user_how_to_use_the_program():
    print("You started this program without giving it any arguments.\n")
    print("This is a command line tool. It has to be used from a command line interface.\n")
    print("If you are on Windows execute this program from powershell.\n"
          "If you are on Ubuntu execute this program from bash.\n")
    print("If you haven't already read the README.md file.\n")

    __maybe_generate_readme_md_file()
