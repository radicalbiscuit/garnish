#!usr/bin/env python

from distutils.core import setup

setup(name='licme',
      version='0.1',
      description='Boilerplate licensing tool',
      author='Jennifer Hamon',
      author_email='jhamon@gmail.com',
      url='http://www.github.com/jhamon/licme',
      packages = ['licme'],
      scripts='licme/licme.py',
      package_data = {'licme' : ['header-statements/*', 'readme-statements/*',
      'licenses/*']},
      license = 'MIT License'
      )
