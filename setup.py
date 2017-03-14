#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from mgqueue import mgqueue

setup(
	name= mgqueue.title, # Application name:
	version= mgqueue.version, # Version number

	author= 'Masayuki Tanaka', # Author name
	author_email= 'm@like.silk.to', # Author mail	

	include_package_data=True, # Include additional files into the package
	url='https://github.com/likesilkto/mgqueue', # Details
	description='Simple task queue.', # short description
	long_description=open('README.md').read(), # long description
	install_requires=[ # Dependent packages (distributions)
		'Daemonize',
	],
	
   	packages=find_packages(),
	scripts=['scripts/mgq'],

	classifiers=[
		'Programming Language :: Python :: 3.6',
		'License :: OSI Approved :: MIT',
    ]
)

# uninstall
# % python setup.py install --record installed_files
# % cat installed_files | xargs rm -rf
# % rm installed_files

