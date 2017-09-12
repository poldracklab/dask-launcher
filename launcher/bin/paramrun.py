#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
import os
import os.path as op
import re
from .. import logging, __version__
log = logging.getLogger('launcher.cli')

DLAUNCH_SCHEDFILE = '.dask-scheduler'
WORKER_CMD = """\
dask-worker --scheduler-file {sfile} --nprocs {nprocs} --no-bokeh \
&> {wfile}-{node}.out\
""".format


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
    import subprocess as sp
    from dask.distributed import Client
    from ..utils import bash as run_task
    opts = get_parser().parse_args()

    # Retrieve logging level
    log_level = int(max(2.5 - opts.verbose_count, 0) * 10)
    if opts.verbose_count > 1:
        log_level = int(max(20 - 5 * opts.verbose_count, 1))
    logging.getLogger().setLevel(log_level)

    # Environment: Setup work directory and variables
    job_id = os.getenv('SLURM_JOBID')
    workdir = os.getenv('DLAUNCH_WORKDIR', os.getcwd())
    os.chdir(workdir)
    rmi_dir = op.abspath('.dlauncher-rmi-%s' % job_id)
    os.makedirs(rmi_dir, exist_ok=True)
    sched_file = op.join(rmi_dir, DLAUNCH_SCHEDFILE + '.json')
    nodes = sp.run(['scontrol', 'show', 'hostname', os.getenv('SLURM_NODELIST')],
                   stdout=sp.PIPE).stdout.decode().strip().split('\n')
    nodes = [node for node in nodes if node]

    # Read parametric file
    log.info('Running parametric file (dask-launcher-%s): %s', __version__, opts.input_file)
    with open(opts.input_file) as paramfile:
        params = paramfile.readlines()
    # Remove empty lines and comments
    params = [p.strip('\n').strip() for p in params if p.strip('\n').strip()]
    params = [p for p in params if not p.startswith('#')]

    # Start scheduler
    sched_node = os.getenv('HOSTNAME')
    log.info('Starting scheduler on "%s"', sched_node)
    sched = sp.Popen('dask-scheduler --scheduler-file {sfile} &> {logfile}'.format(
        sfile=sched_file, logfile=op.join(rmi_dir, 'scheduler-%s.out' % sched_node)), shell=True)

    # Start workers
    tasks_per_node = []
    for ntasks in os.getenv('SLURM_TASKS_PER_NODE').split(','):
        try:
            tasks_per_node += [int(ntasks)]
        except ValueError:
            values = re.match('(\d+)\(x(\d+)\)', ntasks).groups()
            tasks_per_node += [int(values[0])] * int(values[1])

    for node, ntasks in zip(nodes, tasks_per_node):
        if node and ntasks > 0:
            nodecmd = WORKER_CMD(sfile=sched_file,
                                 wfile=op.join(rmi_dir, 'worker'),
                                 node=node,
                                 nprocs=ntasks)
            log.info('Starting worker on "%s":\n%s', node, nodecmd)

            if node == os.getenv('HOSTNAME'):
                sp.Popen(nodecmd, shell=True)
            else:
                nodecmd = 'ssh -t %s \'cd %s; sh -c "( ( nohup %s ) & )"\'' % (
                    workdir, node, nodecmd)
                sp.run(nodecmd, shell=True)

    # Start dask magic
    client = Client(scheduler_file=sched_file)

    # Submit task
    log.info('Submitting %d tasks', len(params))
    tasks = client.map(run_task, [(p, i, job_id) for i, p in enumerate(params)])

    # Retrieve exit codes:
    success = client.gather(tasks)
    if sum(success) == 0:
        log.info('All tasks finished successfully')
    else:
        log.warning('Some tasks failed')

    sched.kill()
    sched.wait()


if __name__ == '__main__':
    main()
