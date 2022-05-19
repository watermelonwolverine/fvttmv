import sys

from cli_wrapper.__ubuntu_setup import ubuntu_setup
from cli_wrapper.main import linux, win32


def ask_yes_or_no_question(question: str):
    while True:
        answer = input("{0} (yes, no): ".format(question))
        if answer in ["yes", "y"]:
            return True
        if answer in ["no", "n"]:
            return False
        print("Please enter 'yes' or 'no'.")


def win_setup():
    raise NotImplementedError("Not implemented")


def setup():
    platform = sys.platform

    if platform == win32:
        win_setup()
    elif platform == linux:
        ubuntu_setup()
