#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from mgqueue import mgqueue

setup(
	name= mgqueue.title, # Application name:
	version= mgqueue.version, # Version number

	author= 'Masayuki Tanaka', # Author name
	author_email= 'm@like.silk.to', # Author mail	

	url='https://github.com/likesilkto/mgqueue', # Details
	description='Simple task queue.', # short description
	long_description='https://likesilkto.github.io/mgqueue', # long description
	install_requires=[ # Dependent packages (distributions)
		'daemonize',
	],
	
	include_package_data=False, # Include additional files into the package
	packages=find_packages(),
	scripts=['scripts/mgq'],

	test_suite = 'tests',

	classifiers=[
		'Programming Language :: Python :: 3.6',
		'License :: OSI Approved :: MIT',
    ]
)

# uninstall
# % python setup.py install --record installed_files
# % cat installed_files | xargs rm -rf
# % rm installed_files

