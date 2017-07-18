#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
# @Author: oesteban
# @Date:   2017-07-18 15:17:07
import os
from .. import logging, __version__
log = logging.getLogger('launcher.cli')


def get_parser():
    """ A trivial parser """
    from argparse import ArgumentParser, RawTextHelpFormatter

    parser = ArgumentParser(description='compare two pandas dataframes',
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('input_file', action='store', help='input parametric job')

    # optional arguments
    parser.add_argument('--version', action='version',
                        version='dask-launcher v{}'.format(__version__))

    # Control instruments
    g_outputs = parser.add_argument_group('Instrumental options')
    g_outputs.add_argument("-v", "--verbose", dest="verbose_count",
                           action="count", default=0,
                           help="increases log verbosity for each occurence, debug level is -vvv")
    return parser


def main():
    """Entry point"""
    from dask.distributed import Client
    from ..utils import bash as run_task
    opts = get_parser().parse_args()

    # Retrieve logging level
    log_level = int(max(2.5 - opts.verbose_count, 0) * 10)
    if opts.verbose_count > 1:
        log_level = int(max(20 - 5 * opts.verbose_count, 1))
    logging.getLogger().setLevel(log_level)

    # Read parametric file
    log.info('Running parametric file (dask-launcher-%s): %s', __version__, opts.input_file)
    with open(opts.input_file) as paramfile:
        params = paramfile.readlines()
    # Remove empty lines and comments
    params = [p.strip('\n').strip() for p in params if p.strip('\n').strip()]
    params = [p for p in params if not p.startswith('#')]

    nodes = os.getenv('SLURM_NODELIST')
    print(nodes)

    # Start dask magic
    client = Client()

    # Submit task
    log.info('Submitting %d tasks', len(params))
    tasks = [client.submit(run_task, p, log_level) for p in params]

    # Retrieve tasks
    results = [task.result() for task in tasks]
    if sum(results) > 0:
        log.warning('Some tasks failed')
    else:
        log.info('All tasks finished successfully')


if __name__ == '__main__':
    main()
