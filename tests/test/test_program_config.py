import unittest

from fvttmv.config import absolute_path_to_foundry_data_key, ProgramConfig, ProgramConfigImpl
from test.common import *


class ProgramConfigImplTest(unittest.TestCase):

    def setUp(self) -> None:
        Setup.setup_working_environment()

    def test_constructor_exceptions(self):

        # not absolute
        try:
            ProgramConfigImpl({absolute_path_to_foundry_data_key: C.foundrydata})
            self.fail()
        except FvttmvException:
            pass

        # not normalized
        try:
            ProgramConfigImpl({absolute_path_to_foundry_data_key: os.path.join(AbsPaths.Data, "..", C.Data)})
            self.fail()
        except FvttmvException:
            pass

        # not a directory
        try:
            ProgramConfigImpl({absolute_path_to_foundry_data_key: os.path.abspath(C.Data)})
            self.fail()
        except FvttmvException:
            pass

        try:
            ProgramConfigImpl({absolute_path_to_foundry_data_key: os.path.abspath("does_not_exist")})
            self.fail()
        except FvttmvException:
            pass

    def test_abs_path_to_foundrydata(self):
        config_dict = {absolute_path_to_foundry_data_key: AbsPaths.Data}

        config = ProgramConfigImpl(config_dict)

        self.assertEqual(config.get_absolute_path_to_foundry_data(),
                         AbsPaths.Data)

    def test_abstract_functions(self):

        config = ProgramConfig()
        try:
            config.get_absolute_path_to_foundry_data()
            self.fail()
        except NotImplementedError:
            pass
