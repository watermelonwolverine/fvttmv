import sys

import setuptools

sys.path.append("src")

# noinspection PyPep8
from cli_wrapper.__constants import app_name, author, url, issues_url
# noinspection PyPep8
from fvttmv import __version__

long_description: str

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=app_name,
    version=__version__,
    author=author,
    author_email="29666253+watermelonwolverine@users.noreply.github.com",
    description="Moves files while also updating FoundryVTT databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
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
)
