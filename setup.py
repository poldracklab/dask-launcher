#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
# @Author: oesteban
# @Date:   2017-07-18 15:04:27
""" dask-launcher setup script """


def main():
    """ Install entry-point """
    import os
    from setuptools import setup, find_packages
    from launcher.__about__ import (
        __version__,
        __author__,
        __email__,
        __maintainer__,
        __copyright__,
        __credits__,
        __license__,
        __status__,
        __description__,
        __longdesc__,
        __url__,
        __download__,
        PACKAGE_NAME,
        CLASSIFIERS,
        REQUIRES,
        SETUP_REQUIRES,
        LINKS_REQUIRES,
        TESTS_REQUIRES,
        EXTRA_REQUIRES,
    )
    pkg_data = {
        'launcher': [
            'tpl/*.jnj2',
        ]
    }

    version = None
    cmdclass = {}
    root_dir = os.path.dirname(os.path.realpath(__file__))
    if os.path.isfile(os.path.join(root_dir, 'launcher', 'VERSION')):
        with open(os.path.join(root_dir, 'launcher', 'VERSION')) as vfile:
            version = vfile.readline().strip()
        pkg_data['launcher'].insert(0, 'VERSION')

    if version is None:
        import versioneer
        version = versioneer.get_version()
        cmdclass = versioneer.get_cmdclass()

    setup(
        name=PACKAGE_NAME,
        version=version,
        description=__description__,
        long_description=__longdesc__,
        author=__author__,
        author_email=__email__,
        license=__license__,
        maintainer_email=__email__,
        classifiers=CLASSIFIERS,
        # Dependencies handling
        setup_requires=SETUP_REQUIRES,
        install_requires=REQUIRES,
        dependency_links=LINKS_REQUIRES,
        tests_require=TESTS_REQUIRES,
        extras_require=EXTRA_REQUIRES,
        url=__url__,
        download_url=__download__,
        entry_points={'console_scripts': [
            # 'mriqc=mriqc.bin.mriqc_run:main',
        ]},
        packages=find_packages(exclude=['*.tests']),
        package_data=pkg_data,
        zip_safe=False,
        cmdclass=cmdclass,
    )


if __name__ == '__main__':
    main()
