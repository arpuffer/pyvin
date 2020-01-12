"""setup pyvin library"""

from typing import List
from setuptools import setup, find_packages
PKG = 'pyvin'
VERSION = __import__(PKG).get_version()

def requirements_file_to_list(filename: str = "requirements.txt") -> List:
    """Create list of requirements from requirements.txt file

    Args:
        filename (str, optional): . Defaults to "requirements.txt".

    Returns:
        List
    """
    with open(filename, 'r') as infile:
        return [x.rstrip() for x in list(infile) if x and not x.startswith('#')]

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name=PKG,
    version="0.0.1",
    author="Alex Puffer",
    description="Python VIN decoder",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/arpuffer/pyvin",
    packages=find_packages(),
    provides=[PKG],
    install_requires=requirements_file_to_list(),
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
