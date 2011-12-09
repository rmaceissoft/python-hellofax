import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "python-hellofax",
    version = "0.1",
    description = "A Python library for accessing the Hello Fax API.",
    long_description = read('README.rst'),
    url = 'https://github.com/rmaceissoft/python-hellofax',
    author = 'Reiner Marquez',
    author_email = 'rmaceissoft@gmail.com',
    packages = find_packages(exclude=['tests', 'example', 'docs']),
    classifiers = [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = ['requests'],
)