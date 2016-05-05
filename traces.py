#!/usr/bin/env python
# traces
# The console utility for executing git-traces commands.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Thu May 05 11:55:50 2016 -0400
#
# Copyright (C) 2016 University of Maryland
# For license information, see LICENSE.txt
#
# ID: traces.py [] benjamin@bengfort.com $

"""
The console utility for executing git-traces commands.
"""

##########################################################################
## Imports
##########################################################################

import sys
import gitrace
import argparse

##########################################################################
## Module Constants
##########################################################################

DESCRIPTION = "A utility for extracting file access traces from Git repositories"
EPILOG  = "Any bugs or issues please report on GitHub"
VERSION = "traces.py beta"

##########################################################################
## Create Parser
##########################################################################

def create_parser(**kwargs):
    """
    Returns the argument parser.
    """
    # Construct the parser
    parser = argparse.ArgumentParser(
        description=DESCRIPTION, epilog=EPILOG, version=VERSION,
    )

    # Define the arguments
    args = {
        ('-o', '--outpath'): {
            'metavar': 'PATH',
            'default': sys.stdout,
            'type': argparse.FileType('a'),
            'help': 'location to append the traces to',
        },
        ('-b', '--branch'): {
            'default': 'master',
            'help': 'the branch to list commits from'
        },
        ('-H', '--header'): {
            'action': 'store_true',
            'default': False,
            'help': 'write a header row to the trace file.',
        },
        'repos': {
            'metavar': 'repo',
            'nargs': '+',
            'help': 'path to repository to extract trace from'
        },
    }

    # Construct the arguments
    for pargs, kwargs in args.items():
        if not isinstance(pargs, tuple):
            pargs = (pargs,)
        parser.add_argument(*pargs, **kwargs)

    return parser


def main(*args):
    """
    Runs the Git trace extractor.
    """
    parser  = create_parser()
    options = parser.parse_args()

    try:
        extractor = gitrace.TraceExtractor(options.outpath, header=options.header)
        extractor.extract(options.repos, options.branch)
    except Exception as e:
        parser.error(str(e))


if __name__ == '__main__':
    main(*sys.argv[1:])
