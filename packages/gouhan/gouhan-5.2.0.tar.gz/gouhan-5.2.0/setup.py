from typing import IO
import setuptools


with open('README.md','r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'gouhan',
    version = '5.2.0',
    author = 'zhu',
    author_email = '15010232321@163.com',
    description = 'This is a test',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://upload.pypi.org/legacy',
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3'
    ],
)