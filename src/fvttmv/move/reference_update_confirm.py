import sys
from io import TextIOWrapper

from fvttmv.exceptions import FvttmvException


class ReferenceUpdateConfirm:
    text_io_wrapper_out: TextIOWrapper
    text_io_wrapper_in: TextIOWrapper

    def __init__(self,
                 text_io_wrapper_out: TextIOWrapper = sys.stdout,
                 text_io_wrapper_in: TextIOWrapper = sys.stdin):
        self.text_io_wrapper_out = text_io_wrapper_out
        self.text_io_wrapper_in = text_io_wrapper_in

    def confirm_reference_update(self,
                                 abs_path_to_src_file,
                                 abs_path_to_dst_file) -> bool:
        self.text_io_wrapper_out.write("You didn't override\n"
                                       "{0}\n"
                                       "with\n"
                                       "{1}\n"
                                       "Do you still want to replace all references? (y,n):\n".
                                       format(abs_path_to_dst_file,
                                              abs_path_to_src_file))

        try:
            input_str = self.text_io_wrapper_in.readline().strip()
        except KeyboardInterrupt:
            raise FvttmvException("KeyboardInterrupt")

        while input_str.lower() != "n" and input_str.lower() != "y":
            self.text_io_wrapper_out.write("please enter y or n:\n")
            input_str = self.text_io_wrapper_in.readline()

        return input_str.lower() == "y"
