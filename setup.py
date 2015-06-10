#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'rdflib==4.2.0',
    'rdflib-sqlalchemy==0.2.dev0',
    'SQLAlchemy==1.0.4',
    'requests==2.5.1',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='articles',
    version='0.0.1',
    description="",
    long_description=readme + '\n\n' + history,
    author="Douglas La Rocca",
    author_email='douglarocca@gmail.com',
    url='https://github.com/douglas-larocca/articles',
    packages=[
        'articles',
    ],
    package_dir={'articles':
                 'articles'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='articles',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
