# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

"""
:authors: vurdolag
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2021 vurdolag
"""


version = '1.0.0'

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='types_checker',
    version=version,

    author='vurdolag',
    author_email='vlad_fotal@mail.ru',

    description=(
        "This is a simple type checker for python functions."
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/vurdolag/py-func-type-checker',
    download_url=f'https://github.com/vurdolag/py-func-type-checker/archive/v{version}.zip',

    license='Apache License, Version 2.0, see LICENSE file',

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    packages=find_packages(),
    keywords=[
        'function', 'runtime', 'types', 'checker', 'strong types'
    ],
)