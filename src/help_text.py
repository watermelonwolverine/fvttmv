help_text = "\
    About\n\
    =====\n\
    \n\
    Mimics the functionality of the `mv` command while also updating the references to moved files in Foundry VTT.\n\
    \n\
    IMPORTANT: Shut down Foundry VTT before moving any files.\n\
    \n\
    Usage\n\
    =====\n\
    \n\
    IMPORTANT:\n\
    ---------\n\
    Shut down Foundry VTT before moving any files.\n\
    \n\
    Use this program at your own risk. It has been tested extensively but there are no guarantees. Always keep backup of\n\
    your Foundry VTT data for cases where something goes wrong.\n\
    \n\
    Syntax\n\
    ------\n\
    \n\
    `fvttmv [--verbose-info, --verbose-debug, --version, --no-move, --check, --help] src [*srcs] [dst]`\n\
    \n\
    `src`: Source path which should be moved or checked\n\
    `*srcs`: Optional additional source paths\n\
    `dst`: Path to destination folder or file, needed when not using the --check option\n\
    \n\
    Options\n\
    -------\n\
    \n\
    `--verbose-info`: Enables verbose output to console\n\
    `--verbose-debug`: Enables very verbose output to console\n\
    `--version`: Prints version and exits\n\
    `--no-move`: Doesn't actually move any files, but updates FoundryVTT databases as if it did, useful for repairing broken\n\
    references\n\
    `--check`: Doesn't move any file, looks for references to those files. Useful when you want to delete files. Doesn't use\n\
    the `dst` argument, instead interprets all given paths as source paths\n\
    `--force` Don't ask before overriding files\n\
    `--help` Display help and exit\n\
    \n\
    Examples\n\
    --------\n\
    \n\
    Renaming/Moving a file:\n\
    \n\
    Ubuntu:\n\
    `fvttmv old/path/to/file1 new/path/to/file1`\n\
    \n\
    Windows:\n\
    `fvttmv.exe old\\path\\to\\file1 new\\path\\to\\file1`\n\
    \n\
    Moving multiple files into an existing folder:\n\
    \n\
    Ubuntu:\n\
    `fvttmv path/to/file1 path/to/file2 path/to/folder`\n\
    \n\
    Windows:\n\
    `fvttmv.exe path\to\file1 path\to\file2 path\to\folder`\n\
    \n\
    Supports wildcards on Ubuntu:\n\
    \n\
    `fvttmv some/folder/*.png path/to/other/folder`\n\
    \n\
    Looking for references to one or more files:\n\
    \n\
    Ubuntu:\n\
    `fvttmv --check some/folder/some_file.png some/folder/some_other_file.png`\n\
    \n\
    Windows:\n\
    `fvttmv.exe --check some\\folder\\some_file.png some\\folder\\some_other_file.png`\n\
    \n\
    Use single quotes when moving a file with a space:\n\
    \n\
    Ubuntu:\n\
    `fvttmv 'some folder/some file' 'some other folder/some other file'`\n\
    \n\
    Windows:\n\
    `fvttmv.exe 'some folder\\some file' 'some other folder\\some other file'`\n\
    \n\
    Known Issues and Quirks\n\
    =======================\n\
    \n\
    All systems\n\
    -----------\n\
    \n\
    Filesystems are quirky and subsequently so is this program.\n\
    \n\
    Trailing `/` and `\\` are ignored. So `fvttmv some_file some_non_existing_path/` will be treated the same\n\
    as `fvttmv some_file some_non_existing_path`. It's generally good to avoid trailing `/` and `\\` as they only cause\n\
    issues, especially `\\`.\n\
    \n\
    Windows\n\
    -------\n\
    \n\
    The program only works in powershell not in cmd.\n\
    \n\
    The Windows file system isn't case-sensitive. This means that Windows treats `C:\\SomeFolder\\SomeFile` the same\n\
    as `c:\\somefolder\\somefile`. When you want to rename a folder/file and only change the case of one or more characters\n\
    the program will tell you that the folder/file already exists. To circumvent this issue rename the folder/file twice and\n\
    use a different name in between.\n\
    \n\
    When one of the paths has `\'` at the end, the arguments will get mixed up. This is a problem with how python\n\
    handles arguments and probably can't be fixed. For example on\n\
    Windows `fvttmv.exe '\\folder name with spaces\' .\\some\\other\\path`\n\
    will fail but `fvttmv.exe '\\folder name with spaces' .\\some\\other\\path` will succeed."
