"""setup pyvin library"""

from typing import List
from setuptools import setup, find_packages
PKG = 'pyvin'
VERSION = __import__(PKG).get_version()

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name=PKG,
    version=VERSION,
    author="Alex Puffer",
    description="Python VIN decoder",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/arpuffer/pyvin",
    packages=find_packages(),
    provides=[PKG],
    install_requires= [
        requests
    ]
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
