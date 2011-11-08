#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# pyrdc's setup.py

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "pyrdc",
    packages = ["pyrdc"],
    version = "0.0.1",
    description = "Utils python library",
    author = "Rafael Durán Castañeda",
    author_email = "rafadurancastaneda@gmail.com",
    url = "https://github.com/rafaduran/pyrdc",
    download_url = "https://github.com/rafaduran/pyrdc/tarball/0.0.1",
    keywords = ["decorator", "patterns","utils"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
      long_description = read("README.md"))