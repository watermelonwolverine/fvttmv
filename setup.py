import setuptools

import fvttmv

long_description: str

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fvttmv",
    version=fvttmv.__version__,
    author="watermelonwolverine",
    author_email="29666253+watermelonwolverine@users.noreply.github.com",
    description="Moves files while also updating FoundryVTT databases",
    url="https://github.com/watermelonwolverine/fvttmv",
    project_urls=
    {
        "Bug Tracker": "https://github.com/watermelonwolverine/fvttmv/issues"
    },
    classifiers=
    [
        "Programming Language:: Python:: 3",
        "License:: OSI Approved:: MIT License",
        "Operating System:: OS Independent"
    ],
    package_dir={"", "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">= 3.9"
)
