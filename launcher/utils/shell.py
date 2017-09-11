#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
# @Author: oesteban
# @Date:   2017-07-18 15:37:33
"""
Running bash commands
"""


def bash(args):
    """
    A task runner for bash
    """
    import os
    from datetime import datetime
    import subprocess

    cmd, task_id, job_id = args

    log_path = os.path.join(
        os.path.abspath('.dlauncher-rmi-%s' % job_id), 'task-%05d')
    out_file = open((log_path + '.out') % task_id, 'w')
    err_file = open((log_path + '.err') % task_id, 'w')

    out_file.write("""\
[{date}] Starting task {job_id}-{task_id}:
{cmd}
""".format(
        date=datetime.now().isoformat(timespec='seconds'),
        task_id=task_id,
        job_id=job_id,
        cmd=cmd
    ))
    out_file.flush()
    task = subprocess.run(cmd, shell=True, stdout=out_file, stderr=err_file)
    pout = abs(task.returncode)

    out_file.write("""[{date}] Finished task {job_id}-{task_id}.""".format(
        date=datetime.now().isoformat(timespec='seconds'),
        task_id=task_id,
        job_id=job_id
    ))
    out_file.close()
    err_file.close()
    return pout
