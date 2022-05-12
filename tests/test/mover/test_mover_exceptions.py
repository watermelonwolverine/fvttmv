import os
import sys

from fvttmv.exceptions import FvttmvException
from test.common import AbsPaths, C
from test.mover.common import MoverTestCaseBase


class MoverTestCaseExceptions(MoverTestCaseBase):

    def test_move_outside_Data_dir(self):
        print("test_move_outside_Data_dir")

        try:
            self.mover.move([AbsPaths.error_log],
                            os.path.join(AbsPaths.logs, "new_filename.log"))
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        self.assert_nothing_changed()

    def test_move_file_to_non_existing_dir(self):
        print("test_move_file_to_non_existing_dir")

        try:
            self.mover.move([AbsPaths.file1_png],
                            os.path.join(AbsPaths.images, "does_not_exist" + os.path.sep))
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        self.assert_nothing_changed()

    def test_move_multiple_file_onto_file(self):
        print("test_move_multiple_file_onto_file")

        try:
            self.mover.move([AbsPaths.file1_png, AbsPaths.file2_png],
                            AbsPaths.file3_png)
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        self.assert_nothing_changed()

    def test_move_non_normalized_src(self):

        print("test_move_non_normalized_path")

        try:
            self.mover.move([os.path.join(AbsPaths.images, "..", C.images, C.file1_png)],
                            AbsPaths.images.join("file3.png"))
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        self.assert_nothing_changed()

    def test_move_non_normalized_dst(self):

        print("test_move_non_normalized_dst")

        try:
            self.mover.move([AbsPaths.file1_png],
                            os.path.join(AbsPaths.images, "..", C.images, "new_filename.png"))
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        self.assert_nothing_changed()

    def test_move_Data_dir(self):
        print("test_move_Data_dir")

        try:
            self.mover.move([AbsPaths.Data],
                            os.path.join(os.path.abspath(C.foundrydata), "Data2"))
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        self.assert_nothing_changed()

    def test_move_relative_path(self):

        print("test_move_relative_path")

        try:
            self.mover.move([AbsPaths.file1_png],
                            os.path.join(C.foundrydata, C.Data, C.file1_png))
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        self.assert_nothing_changed()

    def test_move_non_existing_file(self):

        print("test_move_non_existing_file")

        try:
            self.mover.move([os.path.join(AbsPaths.Data, C.file1_png)],
                            AbsPaths.file1_png)
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        self.assert_nothing_changed()

    def test_move_src_directory_into_child_directory(self):

        print("test_move_src_directory_into_child_directory")

        try:
            self.mover.move([AbsPaths.assets],
                            AbsPaths.images)
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        self.assert_nothing_changed()

    def test_move_file_onto_itself_directly(self):

        print("test_move_file_onto_itself_directly")

        try:
            self.mover.move([AbsPaths.file3_png],
                            AbsPaths.file3_png)
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        self.assert_nothing_changed()

    def test_move_file_onto_itself_indirectly(self):

        print("test_move_file_onto_itself_indirectly")

        try:
            self.mover.move([AbsPaths.file3_png],
                            AbsPaths.sub_folder)
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        self.assert_nothing_changed()

    def test_move_directory_onto_itself_directly(self):

        print("test_move_directory_onto_itself_directly")

        try:
            self.mover.move([AbsPaths.sub_folder],
                            AbsPaths.sub_folder)
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        self.assert_nothing_changed()

    def test_move_directory_onto_itself_indirectly(self):

        print("test_move_directory_onto_itself_directly")

        try:
            self.mover.move([AbsPaths.sub_folder],
                            AbsPaths.images)
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        self.assert_nothing_changed()

    def test_move_file_to_non_existing_dir_no_move(self):
        print("test_move_file_to_non_existing_dir_no_move")

        target_path = os.path.join(AbsPaths.images, "does_not_exist")

        target_path += os.path.sep

        try:
            self.mover.move([AbsPaths.file1_png], target_path)
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

    def test_rename_file_with_quotation_marks1(self):
        print("test_rename_file_with_quotation_marks1")

        target_path = "\"" + AbsPaths.assets + "\""

        try:
            self.mover.move([AbsPaths.file1_png], target_path)
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

    def test_rename_file_with_quotation_marks2(self):
        print("test_rename_file_with_quotation_marks2")

        target_path = "\"" + AbsPaths.assets

        try:
            self.mover.move([AbsPaths.file1_png], target_path)
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

    def test_rename_file_with_quotation_marks3(self):
        print("test_rename_file_with_quotation_marks3")

        target_path = AbsPaths.assets + "\""

        try:
            self.mover.move([AbsPaths.file1_png], target_path)
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

    def test_rename_folder_case_sensitive_windows(self):

        if sys.platform != "win32":
            print("SKIPPED test_rename_folder_case_sensitive_windows")
            return

        print("test_rename_folder_case_sensitive_windows")

        source_path = os.path.join(AbsPaths.images, "some_folder")

        target_path = os.path.join(AbsPaths.images, "Some_Folder")

        os.mkdir(source_path)

        try:
            self.mover.move([source_path], target_path)
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))
            pass
