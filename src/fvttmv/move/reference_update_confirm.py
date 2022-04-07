import sys

from io import TextIOWrapper


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
        self.text_io_wrapper_out.write("You didn't override {0} with {1}. "
                                       "Do you still want to replace all references? (y,n):\n".
                                       format(abs_path_to_dst_file,
                                              abs_path_to_src_file))

        input_str = self.text_io_wrapper_in.readline().strip()

        while input_str.lower() != "n" and input_str.lower() != "y":
            self.text_io_wrapper_out.write("please enter y or n:\n")
            input_str = self.text_io_wrapper_in.readline()

        return input_str.lower() == "y"
