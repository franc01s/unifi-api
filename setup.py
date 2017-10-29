#!/usr/bin/env python

from distutils.core import setup
import sys


setup(name='unifi',
      version='0.0.1',
      description='API towards Ubiquity Networks UniFi controller',
      author='Jakob Borg',
      author_email='jakob@nym.se',
      url='https://github.com/calmh/unifi-api',
      packages=['unifi'],
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: System :: Networking'],
      requires=[
          'requests'
      ]
      )
