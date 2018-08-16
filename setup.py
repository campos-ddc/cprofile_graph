#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

requirements = [
    'click>=6.0',
    'gprof2dot>=2016.10.13',
    'pygraphviz',
]

test_requirements = []

setup(
    name='cprofile_graph',
    version='2.0.4',
    description="cprofile_graph is used to generate visual graphs for Python profiling.",
    author="Diogo de Campos",
    author_email='campos.ddc@gmail.com',
    url='https://github.com/campos-ddc/cprofile_graph',
    packages=[
        'cprofile_graph',
    ],
    package_dir={'cprofile_graph': 'cprofile_graph'},
    entry_points={
        'console_scripts': ['cprofile_graph=cprofile_graph.cli:main']
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='cprofile_graph',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    test_suite='tests',
    tests_require=test_requirements)
