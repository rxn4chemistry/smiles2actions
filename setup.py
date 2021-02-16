"""
Minimal setup.py to allow for local installation in the development environment
with `pip install -e .`
"""
import io
import re
from os import path

from setuptools import setup, find_packages

# Get the version from rxn_actions/__init__.py
# Adapted from https://stackoverflow.com/a/39671214
__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
    io.open('smiles2actions/__init__.py', encoding='utf_8_sig').read()
).group(1)

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='smiles2actions',
    version=__version__,
    url='https://rxn.res.ibm.com',
    author='IBM RXN',
    author_email='noreply@zurich.ibm.com',
    description='Infer action sequences for arbitrary chemical equations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'attrs>=19.3.0',
        'jupyterlab>=2.2.1',
        'matplotlib>=3.3.2',
        'numpy>=1.19.3',
        'OpenNMT-Py==1.2.0',
        'pandas>=1.1.3',
        'pint>=0.16.1',
        'python-levenshtein>=0.12.1',
        'quantulum3>=0.7.6',
        'seaborn>=0.11.0',
        'textdistance>=4.1.5',
        'paragraph2actions @ git+https://github.com/rxn4chemistry/paragraph2actions',
    ],
)
