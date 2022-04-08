About
=====

Mimics the functionality of the `mv` command while also updating the references to moved files in Foundry VTT.

IMPORTANT: Shut down Foundry VTT before moving any files.

Installation: Windows
=====================

Step 1: Get the exe
-------------------

### Option 1: Download

Download one of the pre-built fvttmv.exe files from `Releases`

Goto Step 2: Install program

### Option 2: Build it yourself

Install python3 (version >= 3.9) and add it to your PATH system environment variable.

You can check the version via CMD or powershell with:

`python --version`

Download or clone the repo.

Open a CMD instance inside the project root folder and create a virtual environment.

`python -m venv .\venv`

Activate the venv:

`.\venv\Scripts\activate`

Install pyInstaller package:

`pip install pyInstaller`

Run build file:

`.\build_for_windows.cmd`

You should now have a fvttmv.exe file under dist. After the build succeeded you can delete the venv you previously
created.

Goto Step 2: Install program

Step 2: Install program
-----------------------

Create an empty folder where you want to install the program for example C:\fvttmv

Copy fvttmv.exe into that folder.

Create a fvttmv.conf text file in that folder.

Copy `{"absolute_path_to_foundry_data":"INSERT_PATH_HERE"}` into fvttmv.conf

Replace `INSERT_PATH_HERE` with the path to the Data folder inside your foundrydata
(Not the foundrydata folder itself!).

IMPORTANT: Escape all \\ with \\\\ in that path.

It should look something like this:

`{"absolute_path_to_foundry_data":"C:Users\\user\\foundrydata\\Data"}`

Add the installation path to your PATH system environment variable.

Uninstallation: Windows
=======================

Delete fvttmv.exe and fvttmv.conf files from the installation directory.

Remove the path to the installation directory from the PATH system environment variable.

Installation: Ubuntu
====================

Install python3 if not yet installed

`sudo apt install python3`

Download or clone repo.

Run the install.py script inside the project folder with

`sudo python3 install_on_ubuntu.py`

and follow the installation instructions.

Uninstallation: Ubuntu
======================

Delete the files /etc/fvttmv.conf and /usr/bin/fvttmv

Usage
=====

IMPORTANT:
---------
Shut down Foundry VTT before moving any files.

Use this program at your own risk. It has been tested extensively but there are no guarantees. Always keep backup of
your Foundry VTT data for cases where something goes wrong.

Syntax
------

`fvttmv [--verbose-info, --verbose-debug, --version, --no-move, --check, --help] src [*srcs] [dst]`

`src`: Source path which should be moved or checked\
`*srcs`: Optional additional source paths\
`dst`: Path to destination folder or file, needed when not using the --check option

Options
-------

`--verbose-info`: Enables verbose output to console\
`--verbose-debug`: Enables very verbose output to console\
`--version`: Prints version and exits\
`--no-move`: Doesn't actually move any files, but updates FoundryVTT databases as if it did, useful for repairing broken
references\
`--check`: Doesn't move any file, looks for references to those files. Useful when you want to delete files. Doesn't use
the `dst` argument, instead interprets all given paths as source paths\
`--force` Don't ask before overriding files\
`--help` Display help and exit

Examples
--------

Renaming/Moving a file:

Ubuntu:  
`fvttmv old/path/to/file1 new/path/to/file1`

Windows:  
`fvttmv.exe old\path\to\file1 new\path\to\file1`

Moving multiple files into an existing folder:

Ubuntu:
`fvttmv path/to/file1 path/to/file2 path/to/folder`

Windows:
`fvttmv.exe path\to\file1 path\to\file2 path\to\folder`

Supports wildcards on Ubuntu:

`fvttmv some/folder/*.png path/to/other/folder`

Looking for references to one or more files:

Ubuntu:
`fvttmv --check some/folder/some_file.png some/folder/some_other_file.png`

Windows:
`fvttmv.exe --check some\folder\some_file.png some\folder\some_other_file.png`

Use single quotes when moving a file with a space:

Ubuntu:
`fvttmv 'some folder/some file' 'some other folder/some other file'`

Windows:
`fvttmv.exe 'some folder\some file' 'some other folder\some other file'`

Known Issues and Quirks
=======================

All systems
-----------

Filesystems are quirky and subsequently so is this program.

Trailing `/` and `\` are ignored. So `fvttmv some_file some_non_existing_path/` will be treated the same
as `fvttmv some_file some_non_existing_path`. It's generally good to avoid trailing `/` and `\` as they only cause
issues, especially `\`.

Windows
-------

The program only works in powershell not in cmd.

The Windows file system isn't case-sensitive. This means that Windows treats `C:\SomeFolder\SomeFile` the same
as `c:\somefolder\somefile`. When you want to rename a folder/file and only change the case of one or more characters
the program will tell you that the folder/file already exists. To circumvent this issue rename the folder/file twice and
use a different name in between.

When one of the paths has `\'` at the end, the arguments will get mixed up. This is a problem with how python
handles arguments and probably can't be fixed. For example on
Windows `fvttmv.exe '\folder name with spaces\' .\some\other\path`
will fail but `fvttmv.exe '\folder name with spaces' .\some\other\path` will succeed.

