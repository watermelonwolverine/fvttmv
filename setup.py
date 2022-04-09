import os

import setuptools


def get_version() -> str:
    path_to_version = os.path.join("src", "fvttmv", "_version.py")

    version_py_text: str

    with open(path_to_version, "rt", encoding="utf-8") as fh:
        version_py_text = fh.read()

    splits = version_py_text.split("\"")

    if len(splits) != 3:
        raise Exception()
    else:
        return splits[1]


version = get_version()

long_description: str

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fvttmv",
    version=version,
    author="watermelonwolverine",
    author_email="29666253+watermelonwolverine@users.noreply.github.com",
    description="Moves files while also updating FoundryVTT databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/watermelonwolverine/fvttmv",
    project_urls={
        "Bug Tracker": "https://github.com/watermelonwolverine/fvttmv/issues",
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
