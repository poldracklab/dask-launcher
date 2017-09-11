#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
# @Author: oesteban
# @Date:   2017-07-18 15:37:33
"""
Running bash commands
"""

def bash(cmd):
    """
    A task runner for bash
    """
    import subprocess
    pout = abs(subprocess.run(cmd, shell=True).returncode)
    return pout
