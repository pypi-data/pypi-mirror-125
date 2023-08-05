# -*- coding: utf-8 -*-

import re

from setuptools import setup

# Package meta-data.
NAME = 'ezpickle'
DESCRIPTION = 'Helper functions to simplify pickling and unpickling objects to/from files'
EMAIL = 'github@burnettsonline.org'
AUTHOR = 'Josh Burnett'


with open('README.md') as readme:
    long_description = readme.read()


def get_version(filename='ezpickle.py'):
    """ Extract version information stored as a tuple in source code """
    version = ''
    with open(filename, 'r') as fp:
        for line in fp:
            m = re.search("__version__ = '(.*)'", line)
            if m is not None:
                version = m.group(1)
                break
    return version


setup(
    name="ezpickle",
    version=get_version(),

    py_modules=["ezpickle"],
    install_requires=None,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
    ],

    # metadata for upload to PyPI
    author=NAME,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Public Domain",
    keywords="pickle unpickle",
    url="https://github.com/joshburnett/ezpickle",
)
