#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
# @Author: oesteban
# @Date:   2017-07-18 15:17:07


def get_parser():
    """ A trivial parser """
    from argparse import ArgumentParser, RawTextHelpFormatter
    from .. import __version__

    parser = ArgumentParser(description='compare two pandas dataframes',
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('input_file', action='store', help='input parametric job')

    # optional arguments
    parser.add_argument('--version', action='version',
                        version='dask-launcher v{}'.format(__version__))
    return parser


def main():
    """Entry point"""
    opts = get_parser().parse_args()
    print(opts.input_file)


if __name__ == '__main__':
    main()
