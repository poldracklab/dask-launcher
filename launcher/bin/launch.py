#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from .. import logging, __version__
log = logging.getLogger('launcher.cli')

def get_parser():
    """ A trivial parser """
    from argparse import ArgumentParser, RawTextHelpFormatter

    parser = ArgumentParser(description='compare two pandas dataframes',
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('tasks_file', action='store', help='input parametric job')

    # optional arguments
    g_job = parser.add_argument_group('Job details')
    g_job.add_argument('-j', '--jobname', default='dlaunch', help='Job name')
    g_job.add_argument('-A', '--allocation', default='Analysis_Lonestar',
                       help='Project allocation')
    g_job.add_argument('--email', help='email address for notifications')


    g_resources = parser.add_argument_group('Configuration of requested resources')
    g_resources.add_argument('-N', '--nodes', action='store', dest='num_nodes', type=int,
                             default=1, help='number of nodes to request')
    g_resources.add_argument('-n', '--ntasks-per-node', action='store', type=int, default=1,
                             help='number of tasks per node')
    g_resources.add_argument('-p', '--partition', action='store', default='normal',
                             help='partition/queue for this job')
    g_resources.add_argument('-r', '--runtime', action='store', default='01:00:00',
                             help='requested wallclock time')

    parser.add_argument('--version', action='version',
                        version='dask-launcher v{}'.format(__version__))

    # Control instruments
    g_outputs = parser.add_argument_group('Instrumental options')
    g_outputs.add_argument("-v", "--verbose", dest="verbose_count",
                           action="count", default=0,
                           help="increases log verbosity for each occurence, debug level is -vvv")
    return parser
