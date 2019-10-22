#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'mutalisk'

from setuptools import setup

require_packages = ['setuptools', 'requests', 'ecdsa']

setup(name='cosmostx',
      version='0.1.0',
      description='cosmos python sdk',
      author='',
      author_email='',
      url='https://github.com/mutalisk999/cosmos-tx',
      platforms='any',
      packages=['cosmostx'],
      install_requires=require_packages,
      zip_safe=False,)