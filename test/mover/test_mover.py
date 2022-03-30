import os
import shutil

from fvttmv.move.mover import Mover
from fvttmv.run_config import RunConfig
from test.common import AbsPaths, References, C, ref, FileContents
from test.mover.common import MoverTestBase, ReplaceReferenceCall, ConfirmOverrideCall, unchanged_directory_tree


class MoverTest(MoverTestBase):

    def test_rename_file(self):
        print("test_rename_file")

        run_config = RunConfig(self.program_config)

        mover = Mover(run_config,
                      self.references_updater_mock,
                      self.override_confirm_mock)

        new_filename = "file1_after_renaming.png"

        target_location = os.path.join(AbsPaths.images,
                                       new_filename)

        mover.move([AbsPaths.file1_png],
                   target_location)

        self.directory_walker.walk_directory(AbsPaths.Data)

        expected = [AbsPaths.assets,
                    AbsPaths.images,
                    os.path.join(AbsPaths.images, new_filename),
                    AbsPaths.file2_png,
                    AbsPaths.sub_folder,
                    AbsPaths.file3_png,
                    os.path.join(AbsPaths.Data, C.Logs),
                    AbsPaths.worlds,
                    os.path.join(AbsPaths.worlds, C.not_a_world1),
                    os.path.join(AbsPaths.worlds, C.not_a_world1, C.data),
                    os.path.join(AbsPaths.worlds, C.not_a_world1, C.packs),
                    os.path.join(AbsPaths.worlds, C.not_a_world1, C.scenes),
                    os.path.join(AbsPaths.worlds, C.not_a_world2),
                    os.path.join(AbsPaths.worlds, C.not_a_world2, C.world_json),
                    os.path.join(AbsPaths.worlds, C.world1),
                    os.path.join(AbsPaths.worlds, C.world1, C.data),
                    os.path.join(AbsPaths.worlds, C.world1, C.data, C.contains_1_db),
                    os.path.join(AbsPaths.worlds, C.world1, C.packs),
                    os.path.join(AbsPaths.worlds, C.world1, C.packs, C.contains_2_db),
                    os.path.join(AbsPaths.worlds, C.world1, C.scenes),
                    os.path.join(AbsPaths.worlds, C.world1, C.world_json),
                    os.path.join(AbsPaths.worlds, C.world2),
                    os.path.join(AbsPaths.worlds, C.world2, C.data),
                    os.path.join(AbsPaths.worlds, C.world2, C.data, C.contains_1_and_2_db),
                    os.path.join(AbsPaths.worlds, C.world2, C.data, C.not_a_db_txt),
                    os.path.join(AbsPaths.worlds, C.world2, C.packs),
                    os.path.join(AbsPaths.worlds, C.world2, C.packs, C.contains_none_db),
                    os.path.join(AbsPaths.worlds, C.world2, C.scenes),
                    os.path.join(AbsPaths.worlds, C.world2, C.world_json)]

        self.assertEqual(self.walker_callback.result,
                         expected)

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

        self.directory_walker.walk_directory(AbsPaths.Data)

        expected = [AbsPaths.assets,
                    os.path.join(AbsPaths.assets, new_folder_name),
                    os.path.join(AbsPaths.assets, new_folder_name, C.file1_png),
                    os.path.join(AbsPaths.assets, new_folder_name, C.file2_png),
                    os.path.join(AbsPaths.assets, new_folder_name, C.sub_folder),
                    os.path.join(AbsPaths.assets, new_folder_name, C.sub_folder, C.file3_png),
                    os.path.join(AbsPaths.Data, C.Logs),
                    AbsPaths.worlds,
                    os.path.join(AbsPaths.worlds, C.not_a_world1),
                    os.path.join(AbsPaths.worlds, C.not_a_world1, C.data),
                    os.path.join(AbsPaths.worlds, C.not_a_world1, C.packs),
                    os.path.join(AbsPaths.worlds, C.not_a_world1, C.scenes),
                    os.path.join(AbsPaths.worlds, C.not_a_world2),
                    os.path.join(AbsPaths.worlds, C.not_a_world2, C.world_json),
                    os.path.join(AbsPaths.worlds, C.world1),
                    os.path.join(AbsPaths.worlds, C.world1, C.data),
                    os.path.join(AbsPaths.worlds, C.world1, C.data, C.contains_1_db),
                    os.path.join(AbsPaths.worlds, C.world1, C.packs),
                    os.path.join(AbsPaths.worlds, C.world1, C.packs, C.contains_2_db),
                    os.path.join(AbsPaths.worlds, C.world1, C.scenes),
                    os.path.join(AbsPaths.worlds, C.world1, C.world_json),
                    os.path.join(AbsPaths.worlds, C.world2),
                    os.path.join(AbsPaths.worlds, C.world2, C.data),
                    os.path.join(AbsPaths.worlds, C.world2, C.data, C.contains_1_and_2_db),
                    os.path.join(AbsPaths.worlds, C.world2, C.data, C.not_a_db_txt),
                    os.path.join(AbsPaths.worlds, C.world2, C.packs),
                    os.path.join(AbsPaths.worlds, C.world2, C.packs, C.contains_none_db),
                    os.path.join(AbsPaths.worlds, C.world2, C.scenes),
                    os.path.join(AbsPaths.worlds, C.world2, C.world_json)]

        self.assertEqual(self.walker_callback.result,
                         expected)

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

        expected_directory_tree = [
            AbsPaths.assets,
            os.path.join(AbsPaths.assets, C.file1_png),
            os.path.join(AbsPaths.assets, C.file3_png),
            AbsPaths.images,
            AbsPaths.file2_png,
            AbsPaths.sub_folder,
            os.path.join(AbsPaths.Data, C.Logs),
            AbsPaths.worlds,
            os.path.join(AbsPaths.worlds, C.not_a_world1),
            os.path.join(AbsPaths.worlds, C.not_a_world1, C.data),
            os.path.join(AbsPaths.worlds, C.not_a_world1, C.packs),
            os.path.join(AbsPaths.worlds, C.not_a_world1, C.scenes),
            os.path.join(AbsPaths.worlds, C.not_a_world2),
            os.path.join(AbsPaths.worlds, C.not_a_world2, C.world_json),
            os.path.join(AbsPaths.worlds, C.world1),
            os.path.join(AbsPaths.worlds, C.world1, C.data),
            os.path.join(AbsPaths.worlds, C.world1, C.data, C.contains_1_db),
            os.path.join(AbsPaths.worlds, C.world1, C.packs),
            os.path.join(AbsPaths.worlds, C.world1, C.packs, C.contains_2_db),
            os.path.join(AbsPaths.worlds, C.world1, C.scenes),
            os.path.join(AbsPaths.worlds, C.world1, C.world_json),
            os.path.join(AbsPaths.worlds, C.world2),
            os.path.join(AbsPaths.worlds, C.world2, C.data),
            os.path.join(AbsPaths.worlds, C.world2, C.data, C.contains_1_and_2_db),
            os.path.join(AbsPaths.worlds, C.world2, C.data, C.not_a_db_txt),
            os.path.join(AbsPaths.worlds, C.world2, C.packs),
            os.path.join(AbsPaths.worlds, C.world2, C.packs, C.contains_none_db),
            os.path.join(AbsPaths.worlds, C.world2, C.scenes),
            os.path.join(AbsPaths.worlds, C.world2, C.world_json)
        ]

        self.assert_directory_tree_equals(expected_directory_tree)

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

        expected_directory_tree = [
            AbsPaths.assets,
            target_location,
            os.path.join(target_location, C.file1_png),
            os.path.join(target_location, C.file2_png),
            os.path.join(target_location, C.sub_folder),
            os.path.join(target_location, C.sub_folder, C.file3_png),
            os.path.join(AbsPaths.Data, C.Logs),
            AbsPaths.worlds,
            os.path.join(AbsPaths.worlds, C.not_a_world1),
            os.path.join(AbsPaths.worlds, C.not_a_world1, C.data),
            os.path.join(AbsPaths.worlds, C.not_a_world1, C.packs),
            os.path.join(AbsPaths.worlds, C.not_a_world1, C.scenes),
            os.path.join(AbsPaths.worlds, C.not_a_world2),
            os.path.join(AbsPaths.worlds, C.not_a_world2, C.world_json),
            os.path.join(AbsPaths.worlds, C.world1),
            os.path.join(AbsPaths.worlds, C.world1, C.data),
            os.path.join(AbsPaths.worlds, C.world1, C.data, C.contains_1_db),
            os.path.join(AbsPaths.worlds, C.world1, C.packs),
            os.path.join(AbsPaths.worlds, C.world1, C.packs, C.contains_2_db),
            os.path.join(AbsPaths.worlds, C.world1, C.scenes),
            os.path.join(AbsPaths.worlds, C.world1, C.world_json),
            os.path.join(AbsPaths.worlds, C.world2),
            os.path.join(AbsPaths.worlds, C.world2, C.data),
            os.path.join(AbsPaths.worlds, C.world2, C.data, C.contains_1_and_2_db),
            os.path.join(AbsPaths.worlds, C.world2, C.data, C.not_a_db_txt),
            os.path.join(AbsPaths.worlds, C.world2, C.packs),
            os.path.join(AbsPaths.worlds, C.world2, C.packs, C.contains_none_db),
            os.path.join(AbsPaths.worlds, C.world2, C.scenes),
            os.path.join(AbsPaths.worlds, C.world2, C.world_json)]

        self.assert_directory_tree_equals(expected_directory_tree)

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

        expected_directory_tree = [
            AbsPaths.assets,
            target_location,
            os.path.join(target_location, C.images),
            os.path.join(target_location, C.images, C.file1_png),
            os.path.join(target_location, C.images, C.file2_png),
            os.path.join(target_location, C.images, C.sub_folder),
            os.path.join(target_location, C.images, C.sub_folder, C.file3_png),
            os.path.join(AbsPaths.Data, C.Logs),
            AbsPaths.worlds,
            os.path.join(AbsPaths.worlds, C.not_a_world1),
            os.path.join(AbsPaths.worlds, C.not_a_world1, C.data),
            os.path.join(AbsPaths.worlds, C.not_a_world1, C.packs),
            os.path.join(AbsPaths.worlds, C.not_a_world1, C.scenes),
            os.path.join(AbsPaths.worlds, C.not_a_world2),
            os.path.join(AbsPaths.worlds, C.not_a_world2, C.world_json),
            os.path.join(AbsPaths.worlds, C.world1),
            os.path.join(AbsPaths.worlds, C.world1, C.data),
            os.path.join(AbsPaths.worlds, C.world1, C.data, C.contains_1_db),
            os.path.join(AbsPaths.worlds, C.world1, C.packs),
            os.path.join(AbsPaths.worlds, C.world1, C.packs, C.contains_2_db),
            os.path.join(AbsPaths.worlds, C.world1, C.scenes),
            os.path.join(AbsPaths.worlds, C.world1, C.world_json),
            os.path.join(AbsPaths.worlds, C.world2),
            os.path.join(AbsPaths.worlds, C.world2, C.data),
            os.path.join(AbsPaths.worlds, C.world2, C.data, C.contains_1_and_2_db),
            os.path.join(AbsPaths.worlds, C.world2, C.data, C.not_a_db_txt),
            os.path.join(AbsPaths.worlds, C.world2, C.packs),
            os.path.join(AbsPaths.worlds, C.world2, C.packs, C.contains_none_db),
            os.path.join(AbsPaths.worlds, C.world2, C.scenes),
            os.path.join(AbsPaths.worlds, C.world2, C.world_json)]

        self.assert_directory_tree_equals(expected_directory_tree)

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

        expected_directory_tree = [
            AbsPaths.assets,
            AbsPaths.images,
            AbsPaths.file1_png,
            AbsPaths.file2_png,
            target_location,
            os.path.join(target_location, C.sub_folder),
            os.path.join(target_location, C.sub_folder, C.file3_png),
            os.path.join(target_location, sub_folder_copy),
            os.path.join(target_location, sub_folder_copy, C.file3_png),
            os.path.join(AbsPaths.Data, C.Logs),
            AbsPaths.worlds,
            os.path.join(AbsPaths.worlds, C.not_a_world1),
            os.path.join(AbsPaths.worlds, C.not_a_world1, C.data),
            os.path.join(AbsPaths.worlds, C.not_a_world1, C.packs),
            os.path.join(AbsPaths.worlds, C.not_a_world1, C.scenes),
            os.path.join(AbsPaths.worlds, C.not_a_world2),
            os.path.join(AbsPaths.worlds, C.not_a_world2, C.world_json),
            os.path.join(AbsPaths.worlds, C.world1),
            os.path.join(AbsPaths.worlds, C.world1, C.data),
            os.path.join(AbsPaths.worlds, C.world1, C.data, C.contains_1_db),
            os.path.join(AbsPaths.worlds, C.world1, C.packs),
            os.path.join(AbsPaths.worlds, C.world1, C.packs, C.contains_2_db),
            os.path.join(AbsPaths.worlds, C.world1, C.scenes),
            os.path.join(AbsPaths.worlds, C.world1, C.world_json),
            os.path.join(AbsPaths.worlds, C.world2),
            os.path.join(AbsPaths.worlds, C.world2, C.data),
            os.path.join(AbsPaths.worlds, C.world2, C.data, C.contains_1_and_2_db),
            os.path.join(AbsPaths.worlds, C.world2, C.data, C.not_a_db_txt),
            os.path.join(AbsPaths.worlds, C.world2, C.packs),
            os.path.join(AbsPaths.worlds, C.world2, C.packs, C.contains_none_db),
            os.path.join(AbsPaths.worlds, C.world2, C.scenes),
            os.path.join(AbsPaths.worlds, C.world2, C.world_json)]

        self.assert_directory_tree_equals(expected_directory_tree)

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

    def test_override_file_directly(self):
        print("test_override_file_directly")

        file1_copy = os.path.join(AbsPaths.sub_folder, C.file1_png)

        shutil.copy(AbsPaths.file2_png, file1_copy)

        self.mover.move([file1_copy],
                        AbsPaths.file1_png)

        # should be the same as before now
        self.assert_directory_tree_equals(unchanged_directory_tree)

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
        self.assert_directory_tree_equals(unchanged_directory_tree)

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
        self.assert_directory_tree_equals(unchanged_directory_tree)

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
        self.assert_directory_tree_equals(unchanged_directory_tree)

        expected_replace_reference_calls = [
            ReplaceReferenceCall(
                ref(C.assets, C.images, C.sub_folder, C.file1_png),
                References.file1_original)

        ]

        self.assert_file_contains(AbsPaths.file1_png,
                                  FileContents.file_2)
        self.assert_reference_updater_calls_equal(expected_replace_reference_calls)
        self.assert_no_override_confirms()
