import os
import shutil
import sys

from test.common import AbsPaths, References, C, ref, FileContents
from test.mover.common import MoverTestBase, ReplaceReferenceCall, ConfirmOverrideCall


class MoverTest(MoverTestBase):

    def test_rename_file(self):
        print("test_rename_file")

        new_filename = "file1_after_renaming.png"

        target_location = os.path.join(AbsPaths.images,
                                       new_filename)

        self.mover.move([AbsPaths.file1_png],
                        target_location)

        self.replace_path(
            AbsPaths.file1_png,
            target_location)

        self.assert_directory_tree()

        expected_update_reference_call = \
            [
                ReplaceReferenceCall(References.file1_original,
                                     ref(C.assets, C.images, new_filename))
            ]

        self.assert_reference_updater_calls_equal(expected_update_reference_call)

        self.assert_no_override_confirms()

    def test_rename_folder(self):
        print("test_rename_folder")

        new_folder_name = "images2"

        target_location = os.path.join(AbsPaths.assets,
                                       new_folder_name)

        self.mover.move([AbsPaths.images],
                        target_location)

        self.replace_path(
            AbsPaths.images,
            target_location)

        self.replace_path(
            AbsPaths.file1_png,
            os.path.join(AbsPaths.assets, new_folder_name, C.file1_png))

        self.replace_path(
            AbsPaths.file2_png,
            os.path.join(AbsPaths.assets, new_folder_name, C.file2_png), )

        self.replace_path(
            AbsPaths.sub_folder,
            os.path.join(AbsPaths.assets, new_folder_name, C.sub_folder))

        self.replace_path(
            AbsPaths.file3_png,
            os.path.join(AbsPaths.assets, new_folder_name, C.sub_folder, C.file3_png))

        self.assert_directory_tree()

        expected_replace_reference_calls = [
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

        self.assert_reference_updater_calls_equal(expected_replace_reference_calls)
        self.assert_no_override_confirms()

    def test_move_multiple_files_to_existing_directory(self):
        print("test_move_multiple_files_to_existing_directory")

        target_location = AbsPaths.assets

        self.mover.move([AbsPaths.file1_png, AbsPaths.file3_png],
                        target_location)

        self.replace_path(
            AbsPaths.file1_png,
            os.path.join(AbsPaths.assets, C.file1_png))

        self.replace_path(
            AbsPaths.file3_png,
            os.path.join(AbsPaths.assets, C.file3_png))

        self.assert_directory_tree()

        expected_replace_reference_calls = [
            ReplaceReferenceCall(
                References.file1_original,
                ref(C.assets, C.file1_png)),
            ReplaceReferenceCall(
                References.file3_original,
                ref(C.assets, C.file3_png))
        ]

        self.assert_reference_updater_calls_equal(expected_replace_reference_calls)
        self.assert_no_override_confirms()

    def test_move_directory_to_non_existing_directory(self):
        print("test_move_directory_to_non_existing_directory")

        target_location = os.path.join(AbsPaths.Data, C.images)

        self.mover.move([AbsPaths.images],
                        target_location)

        self.replace_path(
            AbsPaths.images,
            target_location)
        self.replace_path(
            AbsPaths.file1_png,
            os.path.join(target_location, C.file1_png))
        self.replace_path(
            AbsPaths.file2_png,
            os.path.join(target_location, C.file2_png))
        self.replace_path(
            AbsPaths.sub_folder,
            os.path.join(target_location, C.sub_folder))
        self.replace_path(
            AbsPaths.file3_png,
            os.path.join(target_location, C.sub_folder, C.file3_png))

        self.assert_directory_tree()

        expected_replace_reference_calls = [
            ReplaceReferenceCall(
                References.file1_original,
                ref(C.images, C.file1_png)),
            ReplaceReferenceCall(
                References.file2_original,
                ref(C.images, C.file2_png)),
            ReplaceReferenceCall(
                References.file3_original,
                ref(C.images, C.sub_folder, C.file3_png)),
            ReplaceReferenceCall(
                ref(C.assets, C.images, C.sub_folder),
                ref(C.images, C.sub_folder)),
            ReplaceReferenceCall(
                ref(C.assets, C.images, ),
                ref(C.images))
        ]

        self.assert_reference_updater_calls_equal(expected_replace_reference_calls)
        self.assert_no_override_confirms()

    def test_move_directory_to_existing_directory(self):
        print("test_move_directory_to_existing_directory")

        new_folder_name = "new_folder_name"

        target_location = os.path.join(AbsPaths.assets, new_folder_name)

        os.mkdir(target_location)

        self.mover.move([AbsPaths.images],
                        target_location)

        self.add_path(
            target_location)
        self.replace_path(
            AbsPaths.images,
            os.path.join(target_location, C.images))
        self.replace_path(
            AbsPaths.file1_png,
            os.path.join(target_location, C.images, C.file1_png))
        self.replace_path(
            AbsPaths.file2_png,
            os.path.join(target_location, C.images, C.file2_png))
        self.replace_path(
            AbsPaths.sub_folder,
            os.path.join(target_location, C.images, C.sub_folder))
        self.replace_path(
            AbsPaths.file3_png,
            os.path.join(target_location, C.images, C.sub_folder, C.file3_png))

        self.assert_directory_tree()

        expected_replace_reference_calls = [
            ReplaceReferenceCall(
                References.file1_original,
                ref(C.assets, new_folder_name, C.images, C.file1_png)),
            ReplaceReferenceCall(
                References.file2_original,
                ref(C.assets, new_folder_name, C.images, C.file2_png)),
            ReplaceReferenceCall(
                References.file3_original,
                ref(C.assets, new_folder_name, C.images, C.sub_folder, C.file3_png)),
            ReplaceReferenceCall(
                ref(C.assets, C.images, C.sub_folder),
                ref(C.assets, new_folder_name, C.images, C.sub_folder)),
            ReplaceReferenceCall(
                ref(C.assets, C.images),
                ref(C.assets, new_folder_name, C.images))
        ]

        self.assert_reference_updater_calls_equal(expected_replace_reference_calls)
        self.assert_no_override_confirms()

    def test_move_multiple_directories_to_existing_directory(self):
        print("test_move_multiple_directories_to_existing_directory")

        new_folder_name = "new_folder_name"

        target_location = os.path.join(AbsPaths.assets, new_folder_name)

        os.mkdir(target_location)

        sub_folder_copy = "sub_folder_copy"

        abs_path_to_sub_folder_copy = os.path.join(AbsPaths.images, sub_folder_copy)

        shutil.copytree(AbsPaths.sub_folder,
                        abs_path_to_sub_folder_copy)

        self.mover.move([AbsPaths.sub_folder,
                         abs_path_to_sub_folder_copy],
                        target_location)

        # add target path
        self.add_path(
            target_location)
        # copy sub_folder
        self.add_path(
            abs_path_to_sub_folder_copy)
        self.add_path(
            os.path.join(abs_path_to_sub_folder_copy, C.file3_png))
        # move sub_folder_copy
        self.replace_path(
            abs_path_to_sub_folder_copy,
            os.path.join(target_location, sub_folder_copy))
        self.replace_path(
            os.path.join(abs_path_to_sub_folder_copy, C.file3_png),
            os.path.join(target_location, sub_folder_copy, C.file3_png))
        # move sub_folder
        self.replace_path(
            AbsPaths.sub_folder,
            os.path.join(target_location, C.sub_folder))
        self.replace_path(
            AbsPaths.file3_png,
            os.path.join(target_location, C.sub_folder, C.file3_png))

        self.assert_directory_tree()

        expected_replace_reference_calls = [
            ReplaceReferenceCall(
                References.file3_original,
                ref(C.assets, new_folder_name, C.sub_folder, C.file3_png)),
            ReplaceReferenceCall(
                ref(C.assets, C.images, C.sub_folder),
                ref(C.assets, new_folder_name, C.sub_folder)),
            ReplaceReferenceCall(
                ref(C.assets, C.images, sub_folder_copy, C.file3_png),
                ref(C.assets, new_folder_name, sub_folder_copy, C.file3_png)),
            ReplaceReferenceCall(
                ref(C.assets, C.images, sub_folder_copy),
                ref(C.assets, new_folder_name, sub_folder_copy))
        ]

        self.assert_reference_updater_calls_equal(expected_replace_reference_calls)
        self.assert_no_override_confirms()

    def test_override_file_directly_no_override(self):
        print("test_override_file_directly_no_override")

        self.override_confirm_mock.default_answer = False

        file1_copy = os.path.join(AbsPaths.sub_folder, C.file1_png)

        shutil.copy(AbsPaths.file2_png, file1_copy)

        self.mover.move([file1_copy],
                        AbsPaths.file1_png)

        self.add_path(file1_copy)

        self.assert_directory_tree()

        self.assert_file_contains(AbsPaths.file1_png,
                                  FileContents.file_1)

        self.assert_no_references_updated()

        expected_overrides = [ConfirmOverrideCall(file1_copy,
                                                  AbsPaths.file1_png)]
        self.assert_overrides_confirms_equal(expected_overrides)

    def test_override_file_directly(self):
        print("test_override_file_directly")

        file1_copy = os.path.join(AbsPaths.sub_folder, C.file1_png)

        shutil.copy(AbsPaths.file2_png, file1_copy)

        self.mover.move([file1_copy],
                        AbsPaths.file1_png)

        # should be the same as before now
        self.assert_no_files_were_moved()

        expected_replace_reference_calls = [
            ReplaceReferenceCall(
                ref(C.assets, C.images, C.sub_folder, C.file1_png),
                References.file1_original)

        ]

        self.assert_file_contains(AbsPaths.file1_png,
                                  FileContents.file_2)

        self.assert_reference_updater_calls_equal(expected_replace_reference_calls)

        expected_overrides = [ConfirmOverrideCall(file1_copy,
                                                  AbsPaths.file1_png)]
        self.assert_overrides_confirms_equal(expected_overrides)

    def test_override_file_directly_force(self):
        print("test_override_file_directly_force")

        self.run_config.force = True

        file1_copy = os.path.join(AbsPaths.sub_folder, C.file1_png)

        shutil.copy(AbsPaths.file2_png, file1_copy)

        self.mover.move([file1_copy],
                        AbsPaths.file1_png)

        # should be the same as before now
        self.assert_no_files_were_moved()

        expected_replace_reference_calls = [
            ReplaceReferenceCall(
                ref(C.assets, C.images, C.sub_folder, C.file1_png),
                References.file1_original)

        ]

        self.assert_file_contains(AbsPaths.file1_png,
                                  FileContents.file_2)

        self.assert_reference_updater_calls_equal(expected_replace_reference_calls)
        self.assert_no_override_confirms()

    def test_override_file_indirectly(self):
        print("test_override_file_indirectly")

        file1_copy = os.path.join(AbsPaths.sub_folder, C.file1_png)

        shutil.copy(AbsPaths.file2_png, file1_copy)

        self.mover.move([file1_copy],
                        AbsPaths.images)

        # should be the same as before now
        self.assert_no_files_were_moved()

        expected_replace_reference_calls = [
            ReplaceReferenceCall(
                ref(C.assets, C.images, C.sub_folder, C.file1_png),
                References.file1_original)

        ]

        self.assert_file_contains(AbsPaths.file1_png,
                                  FileContents.file_2)

        self.assert_reference_updater_calls_equal(expected_replace_reference_calls)

        expected_overrides = [ConfirmOverrideCall(file1_copy,
                                                  AbsPaths.file1_png)]
        self.assert_overrides_confirms_equal(expected_overrides)

    def test_override_file_indirectly_force(self):
        print("test_override_file_indirectly_force")

        self.run_config.force = True

        file1_copy = os.path.join(AbsPaths.sub_folder, C.file1_png)

        shutil.copy(AbsPaths.file2_png, file1_copy)

        self.mover.move([file1_copy],
                        AbsPaths.images)

        # should be the same as before now
        self.assert_no_files_were_moved()

        expected_replace_reference_calls = [
            ReplaceReferenceCall(
                ref(C.assets, C.images, C.sub_folder, C.file1_png),
                References.file1_original)

        ]

        self.assert_file_contains(AbsPaths.file1_png,
                                  FileContents.file_2)
        self.assert_reference_updater_calls_equal(expected_replace_reference_calls)
        self.assert_no_override_confirms()

    def test_rename_file_with_space1(self):
        print("test_rename_file_with_space1")

        new_filename = "file1 after renaming.png"

        target_location = os.path.join(AbsPaths.images,
                                       new_filename)

        self.mover.move([AbsPaths.file1_png],
                        target_location)

        self.replace_path(AbsPaths.file1_png,
                          target_location)

        self.assert_directory_tree()

        expected_update_reference_call = \
            [
                ReplaceReferenceCall(References.file1_original,
                                     ref(C.assets, C.images, new_filename))
            ]

        self.assert_reference_updater_calls_equal(expected_update_reference_call)

        self.assert_no_override_confirms()

    def test_rename_file_with_umlaut(self):
        # hard to test this really, basically testing urllib.parse.quote
        print("test_rename_file_with_umlaut")

        new_filename = "file1_with_äöü.png"

        target_location = os.path.join(AbsPaths.images,
                                       new_filename)

        self.mover.move([AbsPaths.file1_png],
                        target_location)

        self.replace_path(AbsPaths.file1_png,
                          target_location)

        self.assert_directory_tree()

        expected_update_reference_call = \
            [
                ReplaceReferenceCall(References.file1_original,
                                     ref(C.assets, C.images, new_filename))
            ]

        self.assert_reference_updater_calls_equal(expected_update_reference_call)

        self.assert_no_override_confirms()

    def test_rename_file_with_special_symbol(self):
        # hard to test this really, basically testing urllib.parse.quote
        print("test_rename_file_with_special_symbol")

        new_filename = "file1_with_%().png"

        target_location = os.path.join(AbsPaths.images,
                                       new_filename)

        self.mover.move([AbsPaths.file1_png],
                        target_location)

        self.replace_path(AbsPaths.file1_png,
                          target_location)

        expected_update_reference_call = \
            [
                ReplaceReferenceCall(References.file1_original,
                                     ref(C.assets, C.images, new_filename))
            ]

        self.assert_reference_updater_calls_equal(expected_update_reference_call)

        self.assert_no_override_confirms()

    def test_rename_file_wrong_case(self):
        print("test_rename_file_wrong_case")

        if sys.platform != "win32":
            print("SKIPPED")
            return

        new_filename = "file1_after_renaming.png"

        target_location = os.path.join(AbsPaths.images,
                                       new_filename)

        self.mover.move([AbsPaths.file1_png.upper()],
                        target_location)

        self.replace_path(AbsPaths.file1_png,
                          target_location)

        self.assert_directory_tree()

        expected_update_reference_call = \
            [
                ReplaceReferenceCall(References.file1_original,
                                     ref(C.assets, C.images, new_filename))
            ]

        self.assert_reference_updater_calls_equal(expected_update_reference_call)

        self.assert_no_override_confirms()
