#!usr/bin/env python

import os
from setuptools import setup

from garnish.__init__ import __version__ as VERSION

setup(name='garnish',
      license='MIT License',
      version=VERSION,
      description='Command-line tool for adding boilerplate licensing to your open-source projects. GPL, MIT, and BSD licenses supported.',
      long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
      author='Jennifer Hamon',
      author_email='jhamon@gmail.com',
      maintainer='Jennifer Hamon',
      install_requires=['setuptools'],
      url='http://www.github.com/jhamon/garnish',
      packages = ['garnish'],
      package_data = {'garnish' : ['data/*']},
      classifiers = ['Intended Audience :: Developers',
                    'License :: OSI Approved :: MIT License',
                    'Operating System :: OS Independent',
                    'Topic :: Software Development :: Documentation'],
      keywords = 'opensource gpl mit bsd licenses licensing',
      entry_points = {'console_scripts': ['garnish=garnish.cli:main']}
      )
