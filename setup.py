#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
from setuptools import setup, find_packages

ROOT_DIR = pathlib.Path(__file__).parent
README = (ROOT_DIR / "README.md").read_text()

# Package meta-data.
NAME = 'fastic'
DESCRIPTION = 'Flask static site generator with perks'
URL = 'https://github.com/mdxprograms/fastic'
EMAIL = 'mdxprograms@gmail.com'
AUTHOR = 'Josh Waller'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = '1.0.0'

# required packages
REQUIRED = [
    "astroid", "click", "dukpy", "htmlmin", "isort", "itsdangerous",
    "lazy-object-proxy", "libsass", "mccabe", "ply", "python-dotenv", "six",
    "slimit", "tornado", "typed-ast", "wrapt", "Flask", "Flask-FlatPages",
    "Frozen-Flask", "Jinja2", "Markdown", "MarkupSafe", "PyYAML", "Werkzeug"
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    install_requires=REQUIRED,
)
