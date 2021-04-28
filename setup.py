"""setup pyvin library"""

from setuptools import setup, find_packages

import pkg_resources  # part of setuptools
VERSION = pkg_resources.require("pyvin")[0].version

PKG = 'pyvin'


setup(
    name=PKG,
    version=VERSION,
    author="Alex Puffer",
    description="Python VIN decoder",
    url="https://github.com/arpuffer/pyvin",
    packages=find_packages(),
    provides=[PKG],
    install_requires=[
        'requests~=2.25.1',
    ],
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
