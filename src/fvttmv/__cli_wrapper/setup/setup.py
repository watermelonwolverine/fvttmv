import sys

from fvttmv.__cli_wrapper.__constants import linux, win32
from .__ubuntu_setup import ubuntu_setup


def win_setup():
    raise NotImplementedError("Not implemented")


def setup():
    platform = sys.platform

    if platform == win32:
        win_setup()
    elif platform == linux:
        ubuntu_setup()
