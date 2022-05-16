import sys
from io import TextIOWrapper

from fvttmv.exceptions import FvttmvException


class OverrideConfirm:
    text_io_wrapper_out: TextIOWrapper
    text_io_wrapper_in: TextIOWrapper

    def __init__(self,
                 text_io_wrapper_out: TextIOWrapper = sys.stdout,
                 text_io_wrapper_in: TextIOWrapper = sys.stdin):
        self.text_io_wrapper_out = text_io_wrapper_out
        self.text_io_wrapper_in = text_io_wrapper_in

    def confirm_override(self,
                         abs_path_to_src_file,
                         abs_path_to_dst_file) -> bool:
        self.text_io_wrapper_out.write("You are trying to move\n"
                                       "{0}\n"
                                       "to\n"
                                       "{1}\n"
                                       "which already exists. Do you want to override the file at the target location? (y,n):\n".
                                       format(abs_path_to_src_file,
                                              abs_path_to_dst_file))

        try:
            input_str = self.text_io_wrapper_in.readline().strip()
        except KeyboardInterrupt:
            raise FvttmvException("KeyboardInterrupt")

        while input_str.lower() != "n" and input_str.lower() != "y":
            self.text_io_wrapper_out.write("please enter y or n:\n")
            input_str = self.text_io_wrapper_in.readline()

        return input_str.lower() == "y"
