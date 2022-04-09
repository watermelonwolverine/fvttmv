import unittest

from fvttmv.config import Keys, ProgramConfig, ProgramConfigImpl, ConfigFileReader
from fvttmv.exceptions import FvttmvException
from test.common import *


class ProgramConfigImplTest(unittest.TestCase):

    def setUp(self) -> None:
        Setup.setup_working_environment()

    def test_constructor_exceptions(self):

        # not absolute
        try:
            ProgramConfigImpl(C.foundrydata)
            self.fail()
        except FvttmvException:
            pass

        # not normalized
        try:
            ProgramConfigImpl(os.path.join(AbsPaths.Data, "..", C.Data))
            self.fail()
        except FvttmvException:
            pass

        # not a directory
        try:
            ProgramConfigImpl(os.path.abspath(C.Data))
            self.fail()
        except FvttmvException:
            pass

        try:
            ProgramConfigImpl(os.path.abspath("does_not_exist"))
            self.fail()
        except FvttmvException:
            pass

    def test_abs_path_to_foundrydata(self):
        config_dict = {Keys.absolute_path_to_foundry_data_key: AbsPaths.Data}

        config = ConfigFileReader.parse_dict(config_dict)

        self.assertEqual(config.get_absolute_path_to_foundry_data(),
                         AbsPaths.Data)

    def test_abstract_functions(self):

        config = ProgramConfig()
        try:
            config.get_absolute_path_to_foundry_data()
            self.fail()
        except NotImplementedError:
            pass
