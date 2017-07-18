#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
# @Author: oesteban
# @Date:   2017-07-18 14:53:43

"""
dask-launcher: A reinterpretation of the TACC launcher in Python, based off dask
"""

from datetime import date
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__author__ = 'Oscar Esteban'
__email__ = 'code@oscaresteban.es'
__maintainer__ = 'Oscar Esteban'
__copyright__ = ('Copyright %d, Center for Reproducible Neuroscience, '
                 'Stanford University') % date.today().year
__credits__ = 'Oscar Esteban'
__license__ = 'MIT License'
__status__ = 'Prototype'
__description__ = 'A reinterpretation of the TACC launcher in Python, based off dask'
__longdesc__ = ("Dask-launcher is a utility for performing simple, data parallel, "
                "high throughput computing (HTC) workflows on clusters, massively parallel "
                "processor (MPP) systems, workgroups of computers, and personal machines.")

__url__ = 'http://dask-launcher.readthedocs.org/'
__download__ = ('https://github.com/poldracklab/dask-launcher/archive/'
                '{}.tar.gz'.format(__version__))

PACKAGE_NAME = 'launcher'
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: System :: Distributed Computing',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
]

SETUP_REQUIRES = []

REQUIRES = [
    'dask',
    'distributed',
    'jinja2',
    'versioneer',
]

LINKS_REQUIRES = []

TESTS_REQUIRES = []

EXTRA_REQUIRES = {
    'doc': ['sphinx>=1.5,<1.6', 'sphinx_rtd_theme>=0.2.4', 'sphinx-argparse'],
    'tests': TESTS_REQUIRES,
}

# Enable a handle to install all extra dependencies at once
EXTRA_REQUIRES['all'] = [val for _, val in list(EXTRA_REQUIRES.items())]
