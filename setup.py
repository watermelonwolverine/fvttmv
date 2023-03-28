import os
import sys
from glob import glob

import setuptools

if sys.platform == "win32":
    # for some reason on Windows this is needed
    path_to_project_dir = os.path.split(os.path.realpath(__file__))[0]
    sys.path.append(path_to_project_dir)

from src.fvttmv import __version__
from src.fvttmv.__cli_wrapper.__constants import app_name, author, url, issues_url

setuptools.setup(
    name=app_name,
    version=__version__,
    author=author,
    author_email="29666253+watermelonwolverine@users.noreply.github.com",
    description="Moves files while also updating FoundryVTT databases",
    url=url,
    project_urls={
        "Bug Tracker": issues_url,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob('src/*.py')],
    entry_points={
        'console_scripts': [f'{app_name} = fvttmv.__cli_wrapper.cli:main'],
    },
    requires=["appdirs", "toml"]
)
