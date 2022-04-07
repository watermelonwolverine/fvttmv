from fvttmv.program_config import ProgramConfig


class RunConfig(ProgramConfig):
    # If this is set to true no files will be moved, only the references will be updated
    no_move: bool = False

    # If this is set to true all files given as args are handled as src files and all the program does is look for
    # references and print some information
    check_only: bool = False

    # Do not prompt before overriding
    force: bool = False

    _program_config: ProgramConfig

    def __init__(self,
                 program_config: ProgramConfig):
        self._program_config = program_config

    def get_absolute_path_to_foundry_data(self) -> str:
        return self._program_config.get_absolute_path_to_foundry_data()

    def __str__(self):
        return "RunConfig: ProgramConfig:{0}, no_move={1}, check_only={2}".format(
            str(self._program_config),
            self.no_move,
            self.check_only)
