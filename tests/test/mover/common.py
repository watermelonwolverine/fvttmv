import json
import unittest
from typing import List

from fvttmv.config import RunConfig, ProgramConfig, ProgramConfigImpl
from fvttmv.iterators.directory_walker import DirectoryWalkerCallback, DirectoryWalker
from fvttmv.move.mover import Mover
from fvttmv.move.override_confirm import OverrideConfirm
from fvttmv.move.reference_update_confirm import ReferenceUpdateConfirm
from fvttmv.update.references_updater import ReferencesUpdater
from test.common import AbsPaths, Setup


class DirectoryWalkerCallbackImpl(DirectoryWalkerCallback):
    result: List

    def __init__(self):
        self.result = []

    def step_into_directory(self, abs_path_to_directory: str) -> None:
        self.result.append(abs_path_to_directory)

    def step_out_of_directory(self, abs_path_to_directory: str) -> None:
        pass

    def process_file(self, abs_path_to_file: str) -> None:
        self.result.append(abs_path_to_file)


class ReplaceReferenceCall:
    old_reference: str
    new_reference: str

    def __init__(self,
                 old_reference: str,
                 new_reference: str) -> None:
        self.old_reference = old_reference
        self.new_reference = new_reference

    def __eq__(self, other):
        if not issubclass(type(other), type(self)):
            return False

        otherCall: ReplaceReferenceCall = other

        return \
            self.old_reference == otherCall.old_reference \
            and self.new_reference == otherCall.new_reference

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.__str__()


class ReferencesUpdaterMock(ReferencesUpdater):
    calls: List[ReplaceReferenceCall]

    # noinspection PyMissingConstructor
    def __init__(self):
        self.calls = []

    def replace_references(self,
                           old_reference: str,
                           new_reference: str):
        call = ReplaceReferenceCall(old_reference,
                                    new_reference)

        self.calls.append(call)


class ConfirmOverrideCall:
    abs_path_to_src_file: str
    abs_path_to_dst_file: str

    def __init__(self,
                 abs_path_to_src_file: str,
                 abs_path_to_dst_file: str) -> None:
        self.abs_path_to_src_file = abs_path_to_src_file
        self.abs_path_to_dst_file = abs_path_to_dst_file

    def __eq__(self, other):
        if not issubclass(type(other), type(self)):
            return False

        otherCall: ConfirmOverrideCall = other

        return \
            self.abs_path_to_src_file == otherCall.abs_path_to_src_file \
            and self.abs_path_to_dst_file == otherCall.abs_path_to_dst_file

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.__str__()


class OverrideConfirmMock(OverrideConfirm):
    calls: List[ConfirmOverrideCall]

    default_answer = True

    # noinspection PyMissingConstructor
    def __init__(self):
        self.calls = []

    def confirm_override(self,
                         abs_path_to_src_file,
                         abs_path_to_dst_file) -> bool:
        call = ConfirmOverrideCall(abs_path_to_src_file,
                                   abs_path_to_dst_file)

        self.calls.append(call)

        return self.default_answer


class ReferenceUpdateConfirmMock(ReferenceUpdateConfirm):
    calls: List[ConfirmOverrideCall]

    default_answer = True

    # noinspection PyMissingConstructor
    def __init__(self):
        self.calls = []

    def confirm_reference_update(self,
                                 abs_path_to_src_file,
                                 abs_path_to_dst_file) -> bool:
        call = ConfirmOverrideCall(abs_path_to_src_file,
                                   abs_path_to_dst_file)

        self.calls.append(call)

        return self.default_answer


class MoverTestBase(unittest.TestCase):
    # config
    program_config: ProgramConfig
    run_config: RunConfig
    # mocks
    reference_updater_mock: ReferencesUpdaterMock
    override_confirm_mock: OverrideConfirmMock
    reference_reference_confirm_mock: ReferenceUpdateConfirmMock
    # workers
    __walker_callback: DirectoryWalkerCallbackImpl
    __directory_walker: DirectoryWalker
    # context
    __unchanged_directory_tree: List[str]
    expected_directory_tree: List[str]

    mover: Mover

    def setUp(self) -> None:
        Setup.setup_working_environment()

        self.__instantiate_configs()
        self.__instantiate_mocks()
        self.__instantiate_workers()
        self.__remember_unchanged_dir_tree()

        self.mover = Mover(self.run_config,
                           self.references_updater_mock,
                           self.override_confirm_mock,
                           self.reference_reference_confirm_mock)

    def __instantiate_configs(self):
        self.program_config = ProgramConfigImpl(AbsPaths.Data, [])
        self.run_config = RunConfig(self.program_config)

    def __instantiate_mocks(self):
        self.references_updater_mock = ReferencesUpdaterMock()
        self.override_confirm_mock = OverrideConfirmMock()
        self.reference_reference_confirm_mock = ReferenceUpdateConfirmMock()

    def __instantiate_workers(self):
        self.__walker_callback = DirectoryWalkerCallbackImpl()
        self.__directory_walker = DirectoryWalker(self.__walker_callback)

    def __remember_unchanged_dir_tree(self):
        self.__directory_walker.walk_directory(AbsPaths.Data)
        self.__unchanged_directory_tree = self.__walker_callback.result[:]
        self.__walker_callback.result.clear()
        self.expected_directory_tree = self.__unchanged_directory_tree.copy()

    def assert_no_override_confirms(self):
        self.assert_overrides_confirms_equal([])

    def assert_overrides_confirms_equal(self,
                                        override_confirms: List[ConfirmOverrideCall]):
        self.assertEqual(override_confirms,
                         self.override_confirm_mock.calls)

    def assert_no_files_were_moved(self):
        self.expected_directory_tree = self.__unchanged_directory_tree
        self.assert_directory_tree()

    def assert_no_references_updated(self):
        self.assert_reference_updater_calls_equal(self.references_updater_mock.calls)

    def assert_nothing_changed(self):
        self.assert_no_files_were_moved()
        self.assert_no_references_updated()
        self.assert_no_override_confirms()

    def assert_reference_updater_calls_equal(self,
                                             expected_reference_updater_calls: List[ReplaceReferenceCall]):
        self.assertEqual(expected_reference_updater_calls,
                         self.references_updater_mock.calls)

    def assert_directory_tree(self):
        self.__directory_walker.walk_directory(AbsPaths.Data)

        self.assertEqual(self.expected_directory_tree,
                         self.__walker_callback.result)

    def assert_file_contains(self,
                             path_to_file: str,
                             expected_text_content: str):
        with open(path_to_file, "r", encoding='UTF-8', newline='') as fin:
            text_content_of_file = fin.read()
            self.assertEqual(expected_text_content, text_content_of_file)

    def replace_path(self,
                     element_to_replace: str,
                     new_element: str):
        index = self.expected_directory_tree.index(element_to_replace)
        self.expected_directory_tree[index] = new_element
        self.expected_directory_tree.sort(key=str.lower)

    def add_path(self,
                 element_to_add: str):
        self.expected_directory_tree.append(element_to_add)
        self.expected_directory_tree.sort(key=str.lower)
