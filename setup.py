#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) Maya Fishbach (2018)
#
# This file is part of the gwcosmology python package.
#
# gwcosmology is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gwcosmology is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gwcosmology.  If not, see <http://www.gnu.org/licenses/>.

"""Setup the gwcosmology package
"""

from __future__ import print_function

import sys
if sys.version < '2.6':
    raise ImportError("Python versions older than 2.6 are not supported.")

import glob
import os.path

from setuptools import (setup, find_packages)

# set basic metadata
PACKAGENAME = 'gwcosmology'
DISTNAME = 'gwcosmology'
AUTHOR = 'Maya Fishbach'
AUTHOR_EMAIL = 'maya.fishbach@ligo.org'
LICENSE = 'GPLv3'

cmdclass = {}

# -- versioning ---------------------------------------------------------------

import versioneer
__version__ = versioneer.get_version()
cmdclass.update(versioneer.get_cmdclass())

# -- documentation ------------------------------------------------------------

# import sphinx commands
try:
    from sphinx.setup_command import BuildDoc
except ImportError:
    pass
else:
    cmdclass['build_sphinx'] = BuildDoc

# -- dependencies -------------------------------------------------------------

setup_requires = [
    'setuptools',
    'pytest-runner',
]

install_requires = [
    'numpy >= 1.7.1',
    'scipy >= 0.12.1',
    'matplotlib >= 1.2.0, != 2.1.0, != 2.1.1',
    'astropy >= 1.1.1, < 3.0.0 ; python_version < \'3\'',
    'astropy >= 1.1.1 ; python_version >= \'3\'',
    'seaborn >= 0.9.0'
]

tests_require = [
    'pytest'
]

extras_require = {
    'doc': [
        'ipython',
        'sphinx',
        'numpydoc',
        'sphinx_rtd_theme',
        'sphinxcontrib_programoutput',
    ],
}

# enum34 required for python < 3.4
try:
    import enum  # pylint: disable=unused-import
except ImportError:
    install_requires.append('enum34')

# -- run setup ----------------------------------------------------------------

packagenames = find_packages()

setup(name=DISTNAME,
      provides=[PACKAGENAME],
      version=__version__,
      description=None,
      long_description=None,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      packages=packagenames,
      include_package_data=True,
      cmdclass=cmdclass,
      setup_requires=setup_requires,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require=extras_require,
      test_suite='gwcosmology.tests',
      use_2to3=True,
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Topic :: Scientific/Engineering :: Physics',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Operating System :: MacOS',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      ],
)
