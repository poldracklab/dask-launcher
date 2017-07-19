#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
# @Author: oesteban
# @Date:   2017-07-18 15:37:33
"""
Running bash commands
"""

def bash(cmd, log_level=30):
    """
    A task runner for bash
    """
    import subprocess
    from launcher import logging
    logging.getLogger().setLevel(log_level)
    log = logging.getLogger('launcher.tasks')
    log.log(25, 'Task started: "%s"', cmd)
    pout = abs(subprocess.run(cmd.split(' ')).returncode)
    log.log(25, 'Task finished: "%s"', cmd)
    return pout
