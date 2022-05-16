from cli_wrapper.__constants import app_name
from cli_wrapper.__versions import pyinstaller_version, python_version
from fvttmv.config import Keys

about = "\
About\n\
=====\n\
\n\
Mimics the functionality of the `mv` command while also updating the references to moved files in Foundry VTT.\n\
\n\
IMPORTANT: Shut down Foundry VTT before moving any files."

usage_examples_windows = "\
Examples: Windows\n\
-----------------\n\
\n\
Renaming/Moving a file:\n\
\n\
`{0}.exe old\\path\\to\\file1 new\\path\\to\\file1`\n\
\n\
Moving multiple files into an existing folder:\n\
\n\
`{0}.exe path\\to\\file1 path\\to\\file2 path\\to\\folder`\n\
\n\
Looking for references to one or more files:\n\
\n\
`{0}.exe --check some\\folder\\some_file.png some\\folder\\some_other_file.png`\n\
\n\
Use single quotes when moving a file with a space:\n\
\n\
`{0}.exe 'some folder\\some file' 'some other folder\\some other file'`".format(app_name)

usage_examples_ubuntu = "\
Examples: Ubuntu\n\
----------------\n\
\n\
Renaming/Moving a file:\n\
\n\
`{0} old/path/to/file1 new/path/to/file1`\n\
\n\
Moving multiple files into an existing folder:\n\
\n\
`{0} path/to/file1 path/to/file2 path/to/folder`\n\
\n\
Supports wildcards on Ubuntu:\n\
\n\
`{0} some/folder/*.png path/to/other/folder`\n\
\n\
Looking for references to one or more files:\n\
\n\
`{0} --check some/folder/some_file.png some/folder/some_other_file.png`\n\
\n\
Use single quotes when moving a file with a space:\n\
\n\
`{0} 'some folder/some file' 'some other folder/some other file'`".format(app_name)

usage_examples_both = "\
{0}\n\
\n\
{1}".format(usage_examples_windows, usage_examples_ubuntu)

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
`{0} [--verbose-info, --verbose-debug, --version, --no-move, --check, --help] src [*srcs] [dst]`\n\
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
`--help` Display help and exit".format(app_name)

installation_windows = "\
Installation: Windows\n\
=====================\n\
\n\
Step 1: Get the exe\n\
-------------------\n\
\n\
### Option 1: Download\n\
\n\
Download one of the pre-built `{0}.exe` files from `Releases`\n\
\n\
Go to Step 2: Install program\n\
\n\
### Option 2: Build it yourself\n\
\n\
Install python3 (version >= {2}) and add it to your PATH system environment variable.\n\
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
`pip install pyInstaller=={1}`\n\
\n\
Run build file:\n\
\n\
`.\\scripts\\build_for_windows.cmd`\n\
\n\
You should now have a {0}.exe file under dist. After the build succeeded you can delete the venv you\n\
previously created.\n\
\n\
Go to Step 2: Install program\n\
\n\
Step 2: Install program\n\
-----------------------\n\
\n\
Create an empty folder where you want to install the program for example C:\\{0}\n\
\n\
Copy {0}.exe into that folder.\n\
\n\
Create a {0}.conf text file in that folder.\n\
\n\
Copy `{{\"{3}\":\"INSERT_PATH_HERE\"}}` into {0}.conf\n\
\n\
Replace `INSERT_PATH_HERE` with the path to the Data folder inside your foundrydata\n\
(Not the foundrydata folder itself!).\n\
\n\
IMPORTANT: Escape all `\\` with `\\\\` in that path.\n\
\n\
It should look something like this:\n\
\n\
`{{\"{3}\":\"C:\\\\Users\\\\user\\\\foundrydata\\\\Data\"}}`\n\
\n\
Add the installation path to your PATH system environment variable.\n\
\n\
Uninstallation: Windows\n\
=======================\n\
\n\
Delete {0}.exe and {0}.conf files from the installation directory.\n\
\n\
Remove the path to the installation directory from the PATH system environment variable.".format(app_name,
                                                                                                 pyinstaller_version,
                                                                                                 python_version,
                                                                                                 Keys.absolute_path_to_foundry_data_key)

installation_ubuntu = "\
Installation: Ubuntu 16.04 -20.04\n\
=================================\n\
\n\
Optional: Install Python\n\
------------------------\n\
\n\
An up-to-date Ubuntu 20.04 should have python >= 3.8. Check it with:\n\
\n\
`python3 --version`\n\
\n\
From here on `pythonX` will be used as placeholder for the python you should use. Depending on your system you need to\n\
replace `X` with `3`, `3.8`, `3.9` or `3.10` .\n\
\n\
Install python version>=3.8 if not yet installed.\n\
\n\
`sudo apt install pythonX`\n\
\n\
Step 1: Get the executable\n\
--------------------------\n\
\n\
### Option 1: Download\n\
\n\
Download one of the pre-built `{0}` files from `Releases`\n\
\n\
Go to Step 2: Install the files\n\
\n\
### Option 2: Build it yourself\n\
\n\
Install python if haven't already.\n\
\n\
Download or clone repo.\n\
\n\
Create venv inside the repo:\n\
\n\
`sudo apt install pythonX-venv`\n\
\n\
`pythonX -m venv ./venv`\n\
\n\
Activate venv:\n\
\n\
`source venv/bin/activate`\n\
\n\
Install pyInstaller:\n\
\n\
`pythonX -m pip install pyInstaller=={1}`\n\
\n\
Now run the build script:\n\
\n\
`./scrips/build_for_ubuntu.sh`\n\
\n\
Step 2: Install the files\n\
-------------------------\n\
\n\
### Option 1: Automatic installation\n\
\n\
Install python if you haven't already.\n\
\n\
Clone the repo if you haven't already.\n\
\n\
Go into the project folder.\n\
\n\
Build the project if you haven't already. If you downloaded a pre-built executable. Create a folder named `dist` and move the file there. \n\
\n\
Inside the project folder run:\n\
\n\
`sudo pythonX scripts/install_on_ubuntu.sh`\n\
\n\
### Option 2: Manual installation\n\
\n\
Copy the `{0}` file either from `dist` from where you downloaded it to `usr/bin/{0}`\n\
\n\
Make the file executable:\n\
\n\
`sudo chmod ugo=rx usr/bin/{0}`\n\
\n\
Create a `{0}.conf` file at `/etc/`\n\
\n\
Copy `{{\"{3}\":\"INSERT_PATH_HERE\"}}` into `{0}.conf`\n\
\n\
Replace `INSERT_PATH_HERE` with the path to the Data folder inside your foundrydata\n\
(Not the foundrydata folder itself!).\n\
\n\
It should look something like this:\n\
\n\
`{{\"{3}\":\"/home/user/foundrydata/Data\"}}`\n\
\n\
Uninstallation: Ubuntu\n\
======================\n\
\n\
Delete the files /etc/{0}.conf and /usr/bin/{0}".format(app_name,
                                                        pyinstaller_version,
                                                        python_version,
                                                        Keys.absolute_path_to_foundry_data_key)

installation_both = "\
{0}\n\
\n\
{1}".format(installation_windows, installation_ubuntu)

issues = "\
Known Issues and Quirks\n\
=======================\n\
\n\
All systems\n\
-----------\n\
\n\
Filesystems are quirky and subsequently so is this program.\n\
\n\
Trailing `/` and `\\` are ignored. So `{0} some_file some_non_existing_path/` will be treated the same\n\
as `{0} some_file some_non_existing_path`. It's generally good to avoid trailing `/` and `\\` as they only cause\n\
issues, especially `\\`.\n\
\n\
If the programs encounters a .db file it can not read as UTF-8 it will fail.\n\
An example for such a file would be `thumbs.db` which is a thumbnail cache in Windows XP.\n\
Right now the only thing that can be done is to remove the file if it's not needed or temporarily rename it.\n\
If this problem is encountered often, I'll may implement a blacklist feature, so let me know if this happens to you.\n\
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
Windows `{0}.exe '\\folder name with spaces\\' .\\some\\other\\path`\n\
will fail but `{0}.exe '\\folder name with spaces' .\\some\\other\\path` will succeed.".format(app_name)

additional_configuration = "\
Additional Configuration\n\
========================\n\
\n\
You may have db files outside of worlds you would like to update.\n\
For example you may have one or more modules that you use to share things between worlds.\n\
In this case you need to tell the program where to look for those db files so it can update them.\n\
For this purpose add the following to your {0}.conf:\n\
\n\
```\n\
\"{1}\":LIST_OF_ADDITIONAL_TARGETS\n\
```\n\
\n\
`LIST_OF_ADDITIONAL_TARGETS` has be a list of existing absolute paths to either files or folders.\n\
They also have to be inside the {2} directory.\n\
\n\
Important: Folders are not traversed recursively.\n\
\n\
With this configuration your {0}.conf file might look something like this:\n\
\n\
```\n\
{{\n\
    \"{2}\":\"/home/user/foundrydata/Data\",\n\
    \"{1}\":[\n\
             \"/home/user/foundrydata/Data/modules/share-module/packs\",\n\
             \"/home/user/foundrydata/Data/modules/other-share-module/packs/some-db.db\"\n\
            ]\n\
}}\n\
```\n\
".format(app_name,
         Keys.additional_targets_to_update,
         Keys.absolute_path_to_foundry_data_key)

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
%s\n\
\n\
%s\n\
\n\
%s" % (about, installation_both, usage, usage_examples_both, additional_configuration, issues)

read_me_for_ubuntu = "\
%s\n\
\n\
%s\n\
\n\
%s\n\
\n\
%s\n\
\n\
%s\n\
\n\
%s" % (about, installation_ubuntu, usage, usage_examples_ubuntu, additional_configuration, issues)

read_me_for_windows = "\
%s\n\
\n\
%s\n\
\n\
%s\n\
\n\
%s\n\
\n\
%s\n\
\n\
%s" % (about, installation_windows, usage, usage_examples_windows, additional_configuration, issues)
