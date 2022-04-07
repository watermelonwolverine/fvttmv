import os

from fvttmv.exceptions import FvttmvException
from test.common import AbsPaths, References, C, ref
from test.mover.common import MoverTestBase, ReplaceReferenceCall


class MoverTestNoMove(MoverTestBase):

    def setUp(self) -> None:
        super(MoverTestNoMove, self).setUp()
        self.run_config.no_move = True

    def test_rename_file_no_move(self):
        print("test_rename_file_no_move")

        new_filename = "file1_after_renaming.png"

        target_location = os.path.join(AbsPaths.images,
                                       new_filename)

        self.mover.move([AbsPaths.file1_png],
                        target_location)

        expected_reference_updater_calls = [
            ReplaceReferenceCall(References.file1_original,
                                 ref(C.assets, C.images, new_filename))
        ]

        self.assertEqual(self.references_updater_mock.calls,
                         expected_reference_updater_calls)

        self.assert_no_files_were_moved()
        self.assert_no_override_confirms()

    def test_rename_folder_no_move(self):
        print("test_rename_folder_no_move")

        new_folder_name = "images2"

        target_location = os.path.join(AbsPaths.assets,
                                       new_folder_name)

        self.mover.move([AbsPaths.images],
                        target_location)

        expected_reference_updater_calls = [
            ReplaceReferenceCall(
                References.file1_original,
                ref(C.assets, new_folder_name, C.file1_png)),
            ReplaceReferenceCall(
                References.file2_original,
                ref(C.assets, new_folder_name, C.file2_png)),
            ReplaceReferenceCall(
                ref(C.assets, C.images, C.sub_folder, C.file3_png),
                ref(C.assets, new_folder_name, C.sub_folder, C.file3_png)),
            ReplaceReferenceCall(
                ref(C.assets, C.images, C.sub_folder),
                ref(C.assets, new_folder_name, C.sub_folder)),
            ReplaceReferenceCall(
                ref(C.assets, C.images),
                ref(C.assets, new_folder_name))
        ]

        self.assert_reference_updater_calls_equal(expected_reference_updater_calls)

        self.assert_no_files_were_moved()
        self.assert_no_override_confirms()

    def test_move_multiple_files_no_move(self):
        print("test_move_multiple_files_no_move")

        target_location = AbsPaths.assets

        self.mover.move([AbsPaths.file1_png, AbsPaths.file3_png],
                        target_location)

        expected_reference_updater_calls = [
            ReplaceReferenceCall(References.file1_original,
                                 ref(C.assets, C.file1_png)),
            ReplaceReferenceCall(References.file3_original,
                                 ref(C.assets, C.file3_png))
        ]

        self.assertEqual(expected_reference_updater_calls,
                         self.references_updater_mock.calls)

        self.assert_no_files_were_moved()
        self.assert_no_override_confirms()

    def test_move_outside_Data_dir_no_move(self):
        print("test_move_outside_Data_dir_no_move")

        try:
            self.mover.move([AbsPaths.error_log],
                            os.path.join(AbsPaths.logs, "new_filename.log"))
            self.fail()
        except FvttmvException:
            pass

        self.assert_nothing_changed()

    def test_move_file_to_non_existing_dir_no_move2(self):

        print("test_move_file_to_non_existing_dir_no_move2")

        self.mover.move([AbsPaths.file1_png],
                        os.path.join(AbsPaths.images, "does_not_exist", C.file1_png))

        print(self.references_updater_mock.calls)

        self.assert_no_files_were_moved()
        self.assert_no_override_confirms()
