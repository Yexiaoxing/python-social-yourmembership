#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

try:
    import setuptools
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

from setuptools import setup, find_packages



# Requirements
REQUIRES = [
    "Django>=1.8",
    "Django<1.10",
    "python-social-auth>=0.2.3",
]


setup(
    name="python-social-yourmembership",
    version="0.0.2",
    description="A plugin of YourMembership SSO, with python-social-auth",
    author='Xiaoxing Ye',
    author_email='ye@xiaoxing.us',
    url="https://gitlab.com/mailman/hyperkitty",
    license="GPLv3",
    classifiers=[
        "Framework :: Django",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 2",
        ],
    keywords='email',
    #packages=find_packages(exclude=["*.test", "test", "*.test.*"]),
    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIRES,
    )