about = "\
About\n\
=====\n\
\n\
Mimics the functionality of the `mv` command while also updating the references to moved files in Foundry VTT.\n\
\n\
IMPORTANT: Shut down Foundry VTT before moving any files."

usage = "\
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
\n\
`*srcs`: Optional additional source paths\n\
\n\
`dst`: Path to destination folder or file, needed when not using the --check option\n\
\n\
Options\n\
-------\n\
\n\
`--verbose-info`: Enables verbose output to console\n\
\n\
`--verbose-debug`: Enables very verbose output to console\n\
\n\
`--version`: Prints version and exits\n\
\n\
`--no-move`: Doesn't actually move any files, but updates FoundryVTT databases as if it did, useful for repairing broken\n\
references\n\
\n\
`--check`: Doesn't move any file, looks for references to those files. Useful when you want to delete files. Doesn't use\n\
the `dst` argument, instead interprets all given paths as source paths\n\
\n\
`--force` Don't ask before overriding files\n\
\n\
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
`fvttmv.exe path\\to\\file1 path\\to\\file2 path\\to\\folder`\n\
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
`fvttmv.exe 'some folder\\some file' 'some other folder\\some other file'`"

installation = "\
Installation: Windows\n\
=====================\n\
\n\
Step 1: Get the exe\n\
-------------------\n\
\n\
### Option 1: Download\n\
\n\
Download one of the pre-built fvttmv.exe files from `Releases`\n\
\n\
Goto Step 2: Install program\n\
\n\
### Option 2: Build it yourself\n\
\n\
Install python3 (version >= 3.9) and add it to your PATH system environment variable.\n\
\n\
You can check the version via CMD or powershell with:\n\
\n\
`python --version`\n\
\n\
Download or clone the repo.\n\
\n\
Open a CMD instance inside the project root folder and create a virtual environment.\n\
\n\
`python -m venv .\\venv`\n\
\n\
Activate the venv:\n\
\n\
`.\\venv\\Scripts\\activate`\n\
\n\
Install pyInstaller package:\n\
\n\
`pip install pyInstaller`\n\
\n\
Run build file:\n\
\n\
`.\\scripts\\build_for_windows.cmd`\n\
\n\
You should now have a fvttmv.exe file under dist. After the build succeeded you can delete the venv you previously\n\
created.\n\
\n\
Goto Step 2: Install program\n\
\n\
Step 2: Install program\n\
-----------------------\n\
\n\
Create an empty folder where you want to install the program for example C:\\fvttmv\n\
\n\
Copy fvttmv.exe into that folder.\n\
\n\
Create a fvttmv.conf text file in that folder.\n\
\n\
Copy `{\"absolute_path_to_foundry_data\":\"INSERT_PATH_HERE\"}` into fvttmv.conf\n\
\n\
Replace `INSERT_PATH_HERE` with the path to the Data folder inside your foundrydata\n\
(Not the foundrydata folder itself!).\n\
\n\
IMPORTANT: Escape all `\\` with `\\\\` in that path.\n\
\n\
It should look something like this:\n\
\n\
`{\"absolute_path_to_foundry_data\":\"C:Users\\\\user\\\\foundrydata\\\\Data\"}`\n\
\n\
Add the installation path to your PATH system environment variable.\n\
\n\
Uninstallation: Windows\n\
=======================\n\
\n\
Delete fvttmv.exe and fvttmv.conf files from the installation directory.\n\
\n\
Remove the path to the installation directory from the PATH system environment variable.\n\
\n\
Installation: Ubuntu\n\
====================\n\
\n\
Install python3 if not yet installed\n\
\n\
`sudo apt install python3`\n\
\n\
Download or clone repo.\n\
\n\
Run the install.py script inside the project folder with\n\
\n\
`sudo python3 scripts/install_on_ubuntu.py`\n\
\n\
and follow the installation instructions.\n\
\n\
Uninstallation: Ubuntu\n\
======================\n\
\n\
Delete the files /etc/fvttmv.conf and /usr/bin/fvttmv"

issues = "\
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
When one of the paths has `\\'` at the end, the arguments will get mixed up. This is a problem with how python\n\
handles arguments and probably can't be fixed. For example on\n\
Windows `fvttmv.exe '\\folder name with spaces\\' .\\some\\other\\path`\n\
will fail but `fvttmv.exe '\\folder name with spaces' .\\some\\other\\path` will succeed."

help_text = "\
%s\n\
\n\
%s\n\
\n\
%s" % (about, usage, issues)

read_me = "\
%s\n\
\n\
%s\n\
\n\
%s\n\
\n\
%s" % (about, installation, usage, issues)
