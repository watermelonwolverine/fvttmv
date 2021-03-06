import os
import shutil
import unittest
import urllib.parse

from fvttmv import utf_8

ansi = "ANSI"


def ref(*args):
    result = "/".join(args)
    result = urllib.parse.quote(result)
    return result


class C:
    """
    Constants
    """

    foundrydata = "foundrydata"

    #
    # foundrydata contents
    #
    Data = "Data"
    Logs = "Logs"

    #
    # Data contents
    #
    assets = "assets (with space)"
    worlds = "worlds"
    modules = "modules"

    #
    # assets contents
    #
    file1_png = "file1.png"
    file2_png = "file2 (with space).png"
    file3_png = "file3.png"
    images = "images"
    images2 = "images2"
    sub_folder = "sub_folder"

    #
    # worlds contents
    #
    world1 = "world1"
    world2 = "world2"
    packs = "packs"
    scenes = "scenes"
    data = "data"
    world_json = "world.json"
    not_a_world1 = "not_a_world1"
    not_a_world2 = "not_a_world2"
    contains_1_and_2_db = "contains_1_and_2.db"
    contains_1_db = "contains_1.db"
    contains_2_db = "contains_2.db"
    contains_none_db = "contains_none.db"
    should_not_be_touched_db = "should_not_be_touched.db"
    not_a_db_txt = "not_a_db.txt"

    #
    # modules contents
    #
    shared_module = "shared_module"
    shared_db = "shared.db"

    # Logs contents
    error_log = "error.log"
    Data_txt = "Data.txt"


# relative to Data folder, NOT to working dir
class RelPaths:
    #
    # Data content
    #
    assets = C.assets
    modules = C.modules
    worlds = C.worlds

    #
    # assets content
    #
    images = os.path.join(assets, C.images)

    file1_png = os.path.join(images, C.file1_png)
    file2_png = os.path.join(images, C.file2_png)

    sub_folder = os.path.join(images, C.sub_folder)
    file3_png = os.path.join(sub_folder, C.file3_png)

    #
    # worlds content
    #
    world1 = os.path.join(worlds, C.world1)
    world2 = os.path.join(worlds, C.world2)
    not_a_world1 = os.path.join(worlds, C.not_a_world1)
    not_a_world2 = os.path.join(worlds, C.not_a_world2)

    should_not_be_touched_db = os.path.join(world1, C.should_not_be_touched_db)
    contains_1_db = os.path.join(world1, C.data, C.contains_1_db)
    contains_2_db = os.path.join(world1, C.packs, C.contains_2_db)
    contains_1_and_2_db = os.path.join(world2, C.data, C.contains_1_and_2_db)
    contains_none_db = os.path.join(world2, C.packs, C.contains_none_db)

    not_a_db_txt = os.path.join(world2, C.data, C.not_a_db_txt)

    #
    # modules content
    #
    shared_module = os.path.join(modules, C.shared_module)
    shared_module_packs = os.path.join(shared_module, C.packs)
    shared_db = os.path.join(shared_module_packs, C.shared_db)


class AbsPaths:
    foundrydata = os.path.abspath(C.foundrydata)

    #
    # foundrydata contents
    #
    Data = os.path.join(foundrydata, C.Data)
    Data_txt = os.path.join(foundrydata, C.Data_txt)
    Logs = os.path.join(foundrydata, C.Logs)

    #
    # Data contents
    #
    assets = os.path.join(Data, RelPaths.assets)
    modules = os.path.join(Data, RelPaths.modules)
    worlds = os.path.join(Data, RelPaths.worlds)

    #
    # assets content
    #
    images = os.path.join(Data, RelPaths.images)

    file1_png = os.path.join(Data, RelPaths.file1_png)
    file2_png = os.path.join(Data, RelPaths.file2_png)

    sub_folder = os.path.join(Data, RelPaths.sub_folder)
    file3_png = os.path.join(Data, RelPaths.file3_png)

    #
    # worlds content
    #
    world1 = os.path.join(Data, RelPaths.world1)
    world2 = os.path.join(Data, RelPaths.world2)
    not_a_world1 = os.path.join(Data, RelPaths.not_a_world1)
    not_a_world2 = os.path.join(Data, RelPaths.not_a_world2)

    # this should be ignored, even though it is a db file
    should_not_be_touched_db = os.path.join(Data, RelPaths.should_not_be_touched_db)
    contains_1_db = os.path.join(Data, RelPaths.contains_1_db)
    contains_2_db = os.path.join(Data, RelPaths.contains_2_db)
    contains_1_and_2_db = os.path.join(Data, RelPaths.contains_1_and_2_db)
    contains_none_db = os.path.join(Data, RelPaths.contains_none_db)
    not_a_db_txt = os.path.join(Data, RelPaths.not_a_db_txt)

    #
    # module contents
    #
    shared_module = os.path.join(Data, RelPaths.shared_module)
    shared_module_packs = os.path.join(Data, RelPaths.shared_module_packs)
    shared_db = os.path.join(Data, RelPaths.shared_db)

    logs = os.path.join(os.path.abspath(C.foundrydata), C.Logs)
    error_log = os.path.join(logs, C.error_log)


class References:
    file3_original = ref(C.assets, C.images, C.sub_folder, C.file3_png)

    file1_original = ref(C.assets, C.images, C.file1_png)

    file2_original = ref(C.assets, C.images, C.file2_png)

    file1_replacement = ref(C.assets, C.images2, C.file1_png)

    file2_replacement = ref(C.assets, C.images2, C.file2_png)


class DataStrings:
    json_base_str = "{{\"object1\":{{\"img\":\"{0}\"}}}}"
    html_base_str = "<img src=\\\"{0}\\\">"

    base_data_str = json_base_str + "\n" + html_base_str

    contains_1_original = base_data_str.format(References.file1_original)

    contains_2_original = base_data_str.format(References.file2_original)

    contains_1_and_2_original = contains_1_original + "\n" + contains_2_original

    not_a_db = contains_1_and_2_original

    contains_1_changed = base_data_str.format(References.file1_replacement)

    contains_2_changed = base_data_str.format(References.file2_replacement)

    contains_1_and_2_changed = contains_1_changed + "\n" + contains_2_original

    shared_db = contains_1_and_2_original

    shared_db_changed = contains_1_and_2_changed

    contains_none = base_data_str.format("bla/bla/bla")

    should_not_be_touched_db = contains_1_and_2_original


class FileContents:
    file_1 = "blablabla"
    file_2 = "this is the contents of file 2"
    file_3 = "blabla\nblablabla"
    Data_txt = "OOF"


class Setup:

    @staticmethod
    def setup_working_environment():
        if os.path.exists(C.foundrydata):
            shutil.rmtree(C.foundrydata)

        Setup._setup_folder_structure()

        Setup._create_files()

    @staticmethod
    def _setup_folder_structure():
        os.makedirs(AbsPaths.Logs)
        os.makedirs(AbsPaths.shared_module_packs)
        os.makedirs(AbsPaths.sub_folder)

        #
        # worlds
        #
        os.makedirs(os.path.join(AbsPaths.not_a_world1, C.data))
        os.makedirs(os.path.join(AbsPaths.not_a_world1, C.packs))
        os.makedirs(os.path.join(AbsPaths.not_a_world1, C.scenes))
        os.makedirs(os.path.join(AbsPaths.not_a_world2))
        os.makedirs(os.path.join(AbsPaths.world1, C.data))
        os.makedirs(os.path.join(AbsPaths.world1, C.packs))
        os.makedirs(os.path.join(AbsPaths.world1, C.scenes))
        os.makedirs(os.path.join(AbsPaths.world2, C.data))
        os.makedirs(os.path.join(AbsPaths.world2, C.packs))
        os.makedirs(os.path.join(AbsPaths.world2, C.scenes))

    @staticmethod
    def _create_files():
        Setup._create_db_files()
        Setup._create_png_files()
        Setup._create_world_json_files()

        with open(AbsPaths.Data_txt, "wt", encoding=utf_8, newline='') as fout:
            fout.write(FileContents.Data_txt)

    @staticmethod
    def _create_db_files():
        with open(AbsPaths.contains_2_db, "wt", encoding=utf_8, newline='') as fout:
            fout.write(DataStrings.contains_2_original)

        with open(AbsPaths.contains_1_db, "wt", encoding=utf_8, newline='') as fout:
            fout.write(DataStrings.contains_1_original)

        with open(AbsPaths.contains_1_and_2_db, "wt", encoding=utf_8, newline='') as fout:
            fout.write(DataStrings.contains_1_and_2_original)

        with open(AbsPaths.contains_none_db, "wt", encoding=utf_8, newline='') as fout:
            fout.write(DataStrings.contains_none)

        with open(AbsPaths.not_a_db_txt, "wt", encoding=utf_8, newline='') as fout:
            fout.write(DataStrings.not_a_db)

        with open(AbsPaths.should_not_be_touched_db, "wt", encoding=utf_8, newline='') as fout:
            fout.write(DataStrings.should_not_be_touched_db)

        with open(AbsPaths.shared_db, "wt", encoding=utf_8, newline='') as fout:
            fout.write(DataStrings.shared_db)

    @staticmethod
    def _create_png_files():
        with open(AbsPaths.file1_png, "wt", encoding=utf_8, newline='') as fout:
            fout.write(FileContents.file_1)

        with open(AbsPaths.file2_png, "wt", encoding=utf_8, newline='') as fout:
            fout.write(FileContents.file_2)

        with open(AbsPaths.file3_png, "wt", encoding=utf_8, newline='') as fout:
            fout.write(FileContents.file_3)

    @staticmethod
    def _create_world_json_files():
        path_to_world1_json = os.path.join(AbsPaths.world1, C.world_json)

        with open(path_to_world1_json, "wt", encoding=utf_8, newline='') as fout:
            fout.write("")

        path_to_world_2_json = os.path.join(AbsPaths.world2, C.world_json)
        with open(path_to_world_2_json, "wt", encoding=utf_8, newline='') as fout:
            fout.write("")

        path_to_not_a_world2_json = os.path.join(AbsPaths.worlds, C.not_a_world2, C.world_json)
        with open(path_to_not_a_world2_json, "wt", encoding=utf_8, newline='') as fout:
            fout.write("")


# For testing in a real environment
class TestCase(unittest.TestCase):

    def setUp(self) -> None:
        Setup.setup_working_environment()

# For testing in a virtual environment
# class TestCase(fake_filesystem_unittest.TestCase):
#
#     def setUp(self) -> None:
#         self.setUpPyfakefs()
#         Setup.setup_working_environment()
