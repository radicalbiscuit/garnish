#!usr/bin/env python

from distutils.core import setup

setup(name='kale',
      version='0.1.0',
      description='Command-line boilerplate licensing tool',
      author='Jennifer Hamon',
      author_email='jhamon@gmail.com',
      url='http://www.github.com/jhamon/kale',
      packages = ['kale'],
      scripts='kale/kale.py',
      package_data = {'kale' : ['header-statements/*', 'readme-statements/*',
      'licenses/*']},
      license = 'MIT License'
      )
