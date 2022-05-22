win32 = "win32"
linux = "linux"
app_name = "fvttmv"
config_file_name = f"{app_name}.conf"

config_dir_ubuntu = "~/.local/etc"
config_dir_windows = f"%LOCALAPPDATA%\\{app_name}"

path_to_config_file_linux = f"{config_dir_ubuntu}/{config_file_name}"
path_to_config_file_windows = f"{config_dir_windows}\\{config_file_name}"

author = "watermelonwolverine"
url = "https://github.com/%s/%s" % (author, app_name)
issues_url = "%s/issues" % url
