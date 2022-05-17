import os

from fvttmv.config import Keys, ProgramConfigImpl, ConfigFileReader
from fvttmv.exceptions import FvttmvException
from test.common import TestCase, AbsPaths, C, RelPaths


class ProgramConfigImplTest(TestCase):

    def test_constructor_exceptions_for_abs_path_to_foundry_data(self):

        print("test_constructor_exceptions_for_abs_path_to_foundry_data")

        # not absolute
        try:
            ProgramConfigImpl(C.foundrydata, [])
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        # not normalized
        try:
            ProgramConfigImpl(os.path.join(AbsPaths.Data, "..", C.Data), [])
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        # not a directory
        try:
            ProgramConfigImpl(AbsPaths.Data_txt, [])
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        try:
            ProgramConfigImpl(os.path.abspath("does_not_exist"), [])
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

    def test_constructor_exceptions_for_additional_targets_to_update(self):

        print("test_constructor_exceptions_for_additional_targets_to_update")

        # not absolute
        try:
            ProgramConfigImpl(AbsPaths.Data, [os.path.join(C.foundrydata, C.Data, RelPaths.shared_module_packs)])
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        # not normalized
        try:
            ProgramConfigImpl(AbsPaths.Data, [os.path.join(AbsPaths.shared_module, "..", C.shared_module)])
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        try:
            ProgramConfigImpl(AbsPaths.Data, [os.path.join(AbsPaths.Data, "does_not_exist")])
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

        # outside of foundry data dir
        try:
            ProgramConfigImpl(AbsPaths.Data, [os.path.join(AbsPaths.Data_txt)])
            self.fail()
        except FvttmvException as ex:
            print("Got exception: " + str(ex))

    def test_get_abs_path_to_foundrydata(self):

        print("test_get_abs_path_to_foundrydata")

        config_dict = {Keys.absolute_path_to_foundry_data_key: AbsPaths.Data}

        # noinspection PyUnresolvedReferences
        config = ConfigFileReader._ConfigFileReader__parse_dict(config_dict)

        self.assertEqual(config.get_absolute_path_to_foundry_data(),
                         AbsPaths.Data)

        self.assertEqual(config.get_additional_targets_to_update(),
                         [])

    def test_get_additional_targets_to_update(self):

        print("test_get_additional_targets_to_update")

        config_dict = {Keys.absolute_path_to_foundry_data_key: AbsPaths.Data,
                       Keys.additional_targets_to_update: [AbsPaths.shared_db]}

        # noinspection PyUnresolvedReferences
        config = ConfigFileReader._ConfigFileReader__parse_dict(config_dict)

        self.assertEqual(config.get_absolute_path_to_foundry_data(),
                         AbsPaths.Data)

        self.assertEqual(config.get_additional_targets_to_update(),
                         [AbsPaths.shared_db])
