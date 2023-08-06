import re
from setuptools import setup

# metadata for upload to PyPI
NAME = 'xlsxtools'
DESCRIPTION = 'Utility functions for writing and manipulating Excel files'
EMAIL = 'github@burnettsonline.org'
AUTHOR = 'Josh Burnett'
REQUIRED = ['pandas', 'openpyxl']


with open('README.md') as readme:
    long_description = readme.read()


def get_version(filename='xlsxtools.py'):
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
    name="xlsxtools",
    version=get_version(),

    py_modules=["xlsxtools"],
    install_requires=REQUIRED,
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

    author=NAME,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Public Domain",
    keywords="xlsx Excel",
    url="https://github.com/joshburnett/xlsxtools",
)
