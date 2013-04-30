#!usr/bin/env python

from setuptools import setup

from kale.__init__ import __version__ as VERSION

setup(name='kale',
      license='MIT License',
      version=VERSION,
      description='Command-line tool for adding boilerplate licensing to your open-source projects. GPL, MIT, and BSD licenses supported.',
      long_description=open('README.md', 'r').read(),
      author='Jennifer Hamon',
      author_email='jhamon@gmail.com',
      maintainer='Jennifer Hamon',
      install_requires=['setuptools'],
      url='http://www.github.com/jhamon/kale',
      packages = ['kale'],
      package_data = {'kale' : ['header-statements/*', 'readme-statements/*',
      'licenses/*']},
      keywords = 'opensource gpl mit bsd licenses licensing',
      entry_points = {'console_scripts': ['kale=kale.cli:main']}
      )
