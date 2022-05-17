import sys

import setuptools

sys.path.append("src")

# noinspection PyPep8
from cli_wrapper.__constants import app_name, author, url, issues_url
# noinspection PyPep8
from fvttmv import __version__

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
    packages=setuptools.find_packages(where="src", exclude=['cli_wrapper']),
    python_requires=">=3.8",
)
