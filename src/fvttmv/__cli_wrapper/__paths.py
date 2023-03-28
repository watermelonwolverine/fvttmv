import os

from fvttmv.__cli_wrapper.__constants import app_name, author

config_file_name = f"{app_name}.toml"

config_dir_ubuntu_user = os.path.join(os.path.expanduser("~"),
                                      "config",
                                      author,
                                      app_name)

config_dir_ubuntu_global = os.path.join("/",
                                        "etc",
                                        "xdg",
                                        author,
                                        app_name)

config_dir_windows_user = os.path.join(os.path.expandvars("%LOCALAPPDATA%"),
                                       author,
                                       app_name)

config_dir_windows_global = os.path.join(os.path.expandvars("%PROGRAMDATA%"),
                                         author,
                                         app_name)
