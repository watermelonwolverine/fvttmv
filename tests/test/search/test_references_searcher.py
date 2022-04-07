import unittest
from io import TextIOWrapper

from fvttmv.exceptions import FvttmvException
from fvttmv.path_tools import PathTools
from fvttmv.search.references_searcher import ReferencesSearcher
from test.common import *


class TextIOWrapperMock(TextIOWrapper):
    outputs = []

    # noinspection PyMissingConstructor
    def __init__(self):
        pass

    def write(self, string: str):
        self.outputs.append(string)


class ReferencesSearcherTest(unittest.TestCase):
    _path_tools: PathTools

    def setUp(self) -> None:
        Setup.setup_working_environment()
        self._path_tools = PathTools(AbsPaths.Data)

    def test_search_exceptions(self):
        print("test_search_exceptions")

        text_io_wrapper = TextIOWrapperMock()

        references_searcher = ReferencesSearcher(self._path_tools,
                                                 text_io_wrapper)

        relative_path = os.path.join("assets", "images", "test1.png")

        try:
            references_searcher.search([relative_path])
            self.fail()
        except FvttmvException:
            pass

        non_normalized_path = os.path.join(AbsPaths.Data, C.assets, C.images, "..", C.images, C.file1_png)

        try:
            references_searcher.search([non_normalized_path])
            self.fail()
        except FvttmvException:
            pass

    def test_search(self):
        print("test_search")

        text_io_wrapper = TextIOWrapperMock()

        references_searcher = ReferencesSearcher(self._path_tools,
                                                 text_io_wrapper)

        references_searcher.search([AbsPaths.images])

        expected = ['Found reference to {0} in {1}\n'.format(References.file1_original, RelPaths.contains_1_db),
                    'Found reference to {0} in {1}\n'.format(References.file1_original, RelPaths.contains_1_and_2_db),
                    'Found reference to {0} in {1}\n'.format(References.file2_original, RelPaths.contains_2_db),
                    'Found reference to {0} in {1}\n'.format(References.file2_original, RelPaths.contains_1_and_2_db)]

        result = text_io_wrapper.outputs

        print(result)

        self.assertEqual(expected, result)
