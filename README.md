About
=====

Mimics the functionality of the `mv` command while also updating the references to moved files in Foundry VTT.

IMPORTANT: Shut down Foundry VTT before moving any files.

Installation: Windows
=====================

Step 1: Get the exe
-------------------

### Option 1: Download

Download one of the pre-built `fvttmv.exe` files from `Releases`

Go to Step 2: Install program

### Option 2: Build it yourself

Install python3 (version >= 3.8) and add it to your PATH system environment variable.

You can check the version via CMD or powershell with:

`python --version`

Download or clone the repo.

Open a CMD instance inside the project root folder and create a virtual environment.

`python -m venv .\venv`

Activate the venv:

`.\venv\Scripts\activate`

Install pyInstaller package:

`pip install pyInstaller==4.10`

Run build file:

`.\scripts\build_for_windows.cmd`

You should now have a fvttmv.exe file under dist. After the build succeeded you can delete the venv you
previously created.

Go to Step 2: Install program

Step 2: Install program
-----------------------

Create an empty folder where you want to install the program for example C:\fvttmv

Copy fvttmv.exe into that folder.

Create a fvttmv.conf text file in that folder.

Copy `{"absolute_path_to_foundry_data":"INSERT_PATH_HERE"}` into fvttmv.conf

Replace `INSERT_PATH_HERE` with the path to the Data folder inside your foundrydata
(Not the foundrydata folder itself!).

IMPORTANT: Escape all `\` with `\\` in that path.

It should look something like this:

`{"absolute_path_to_foundry_data":"C:\\Users\\user\\foundrydata\\Data"}`

Add the installation path to your PATH system environment variable.

Uninstallation: Windows
=======================

Delete fvttmv.exe and fvttmv.conf files from the installation directory.

Remove the path to the installation directory from the PATH system environment variable.

Installation: Ubuntu 16.04 -20.04
=================================

Optional: Install Python
------------------------

An up-to-date Ubuntu 20.04 should have python >= 3.8. Check it with:

`python3 --version`

From here on `pythonX` will be used as placeholder for the python you should use. Depending on your system you need to
replace `X` with `3`, `3.8`, `3.9` or `3.10` .

Install python version>=3.8 if not yet installed.

`sudo apt install pythonX`

Step 1: Get the executable
--------------------------

### Option 1: Download

Download one of the pre-built `fvttmv` files from `Releases`

Go to Step 2: Install the files

### Option 2: Build it yourself

Install python if haven't already.

Download or clone repo.

Create venv inside the repo:

`sudo apt install pythonX-venv`

`pythonX -m venv ./venv`

Activate venv:

`source venv/bin/activate`

Install pyInstaller:

`pythonX -m pip install pyInstaller==4.10`

Now run the build script:

`./scrips/build_for_ubuntu.sh`

Step 2: Install the files
-------------------------

### Option 1: Automatic installation

Install python if you haven't already.

Clone the repo if you haven't already.

Go into the project folder.

Build the project if you haven't already. If you downloaded a pre-built executable. Create a folder named `dist` and move the file there. 

Inside the project folder run:

`sudo pythonX scripts/install_on_ubuntu.sh`

### Option 2: Manual installation

Copy the `fvttmv` file either from `dist` from where you downloaded it to `usr/bin/fvttmv`

Make the file executable:

`sudo chmod ugo=rx usr/bin/fvttmv`

Create a `fvttmv.conf` file at `/etc/`

Copy `{"absolute_path_to_foundry_data":"INSERT_PATH_HERE"}` into `fvttmv.conf`

Replace `INSERT_PATH_HERE` with the path to the Data folder inside your foundrydata
(Not the foundrydata folder itself!).

It should look something like this:

`{"absolute_path_to_foundry_data":"/home/user/foundrydata/Data"}`

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

`src`: Source path which should be moved or checked

`*srcs`: Optional additional source paths

`dst`: Path to destination folder or file, needed when not using the --check option

Options
-------

`--verbose-info`: Enables verbose output to console

`--verbose-debug`: Enables very verbose output to console

`--version`: Prints version and exits

`--no-move`: Doesn't actually move any files, but updates FoundryVTT databases as if it did, useful for repairing broken
references

`--check`: Doesn't move any file, looks for references to those files. Useful when you want to delete files. Doesn't use
the `dst` argument, instead interprets all given paths as source paths

`--force` Don't ask before overriding files

`--help` Display help and exit

Examples: Windows
-----------------

Renaming/Moving a file:

`fvttmv.exe old\path\to\file1 new\path\to\file1`

Moving multiple files into an existing folder:

`fvttmv.exe path\to\file1 path\to\file2 path\to\folder`

Looking for references to one or more files:

`fvttmv.exe --check some\folder\some_file.png some\folder\some_other_file.png`

Use single quotes when moving a file with a space:

`fvttmv.exe 'some folder\some file' 'some other folder\some other file'`

Examples: Ubuntu
----------------

Renaming/Moving a file:

`fvttmv old/path/to/file1 new/path/to/file1`

Moving multiple files into an existing folder:

`fvttmv path/to/file1 path/to/file2 path/to/folder`

Supports wildcards on Ubuntu:

`fvttmv some/folder/*.png path/to/other/folder`

Looking for references to one or more files:

`fvttmv --check some/folder/some_file.png some/folder/some_other_file.png`

Use single quotes when moving a file with a space:

`fvttmv 'some folder/some file' 'some other folder/some other file'`

Additional Configuration
========================

You may have db files outside of worlds you would like to update.
For example you may have one or more modules that you use to share things between worlds.
In this case you need to tell the program where to look for those db files so it can update them.
For this purpose add the following to your fvttmv.conf:

```
"additional_targets_to_update":LIST_OF_ADDITIONAL_TARGETS
```

`LIST_OF_ADDITIONAL_TARGETS` has be a list of existing absolute paths to either files or folders.
They also have to be inside the absolute_path_to_foundry_data directory.

Important: Folders are not traversed recursively.

With this configuration your fvttmv.conf file might look something like this:

```
{
    "absolute_path_to_foundry_data":"/home/user/foundrydata/Data",
    "additional_targets_to_update":[
             "/home/user/foundrydata/Data/modules/share-module/packs",
             "/home/user/foundrydata/Data/modules/other-share-module/packs/some-db.db"
            ]
}
```


Known Issues and Quirks
=======================

All systems
-----------

Filesystems are quirky and subsequently so is this program.

Trailing `/` and `\` are ignored. So `fvttmv some_file some_non_existing_path/` will be treated the same
as `fvttmv some_file some_non_existing_path`. It's generally good to avoid trailing `/` and `\` as they only cause
issues, especially `\`.

If the programs encounters a .db file it can not read as UTF-8 it will fail.
An example for such a file would be `thumbs.db` which is a thumbnail cache in Windows XP.
Right now the only thing that can be done is to remove the file if it's not needed or temporarily rename it.
If this problem is encountered often, I'll may implement a blacklist feature, so let me know if this happens to you.

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