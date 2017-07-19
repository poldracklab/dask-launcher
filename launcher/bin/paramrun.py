#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
# @Author: oesteban
# @Date:   2017-07-18 15:17:07
import os
import os.path as op
from .. import logging, __version__
log = logging.getLogger('launcher.cli')

DLAUNCH_SCHEDFILE = '.dask-scheduler'
WORKER_CMD = """\
nice -n 19 sh -c "( ( nohup dask-worker --scheduler-file {sfile} > {wfile}-{node}.out \
2> {wfile}-{node}.err < /dev/null ) & )"\
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
    import paramiko
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

    # Environment
    os.chdir(os.getenv('DLAUNCH_WORKDIR', os.getcwd()))
    nodes = sp.run(['scontrol', 'show', 'hostname', os.getenv('SLURM_NODELIST')],
                   stdout=sp.PIPE).stdout.decode().strip().split('\n')
    nodes = [node for node in nodes if node]

    # log.info('Starting scheduler on "%s"', os.getenv('HOSTNAME'))
    # sched = sp.Popen(['dask-ssh', '--scheduler-file', nodes, '--log-directory', os.getcwd()])

    # Start scheduler
    sched_file = DLAUNCH_SCHEDFILE + '-%s.json' % os.getenv('SLURM_JOBID')
    log.info('Starting scheduler on "%s"', os.getenv('HOSTNAME'))
    sched = sp.Popen(['dask-scheduler', '--scheduler-file', sched_file])

    # tasks_per_node = os.getenv('SLURM_TASKS_PER_NODE')
    # print('SLURM_NODELIST=', nodes, 'SLURM_TASKS_PER_NODE=', tasks_per_node, 'HOSTNAME=', os.getenv('HOSTNAME'))
    # Start workers
    cwd = os.getcwd()
    for node in nodes:
        if node:
            log.info('Starting worker on "%s"', node)
            if node == os.getenv('HOSTNAME'):
                pass
                # sp.Popen(['dask-worker', '--scheduler-file', sched_file])
            else:
                nodecmd = WORKER_CMD(sfile=op.join(cwd, sched_file),
                                     wfile=op.join(cwd, 'worker'),
                                     node=node)
                # sp.run(['ssh', '-nf', node, nodecmd], shell=True)

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=node)
                channel = ssh.get_transport().open_session()
                channel.get_pty()
                shell = ssh.invoke_shell()
                print(nodecmd)
                shell.send(nodecmd)

    # Start dask magic
    client = Client('%s:8786' % nodes[0])

    # Submit task
    log.info('Submitting %d tasks', len(params))
    tasks = [client.submit(run_task, p, log_level) for p in params]

    # Retrieve tasks
    results = [task.result() for task in tasks]
    if sum(results) > 0:
        log.warning('Some tasks failed')
    else:
        log.info('All tasks finished successfully')

    sched.kill()
    sched.wait()


if __name__ == '__main__':
    main()
