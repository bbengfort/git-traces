# gitrace.extract
# Extracts the trace information from the various commit versions.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Thu May 05 18:00:03 2016 -0400
#
# Copyright (C) 2016 University of Maryland
# For license information, see LICENSE.txt
#
# ID: extract.py [] benjamin@bengfort.com $

"""
Extracts the trace information from the various commit versions.
"""

##########################################################################
## Imports
##########################################################################

import os
import csv

from gitrace.repo import RepoManager


##########################################################################
## Trace Extractor
##########################################################################

class TraceExtractor(object):

    # The default ordered list of fields to write out to the trace file.
    FIELDS = [
        'commit', 'author', 'object', 'size', 'timestamp',
        'lines', 'insertions', 'deletions', 'renamed', 'deleted', 'added'
    ]

    def __init__(self, stream, fields=None, header=False):
        """
        Initialize the extraction to a stream - which should be a file like
        object with permissions for writing (or appending).
        """
        self.stream = stream
        self.fields = fields or self.FIELDS
        self.writer = csv.DictWriter(self.stream, fieldnames=self.fields)

        if header:
            self.writer.writeheader()

    def extract(self, repos, branch='master'):
        """
        Performs the extraction using the RepoManager
        """
        # Find the common prefix of all the repositories
        prefix = os.path.commonprefix(repos)

        # Go through every passed in path
        for path in repos:

            # Construct the repository
            repo = RepoManager(path)

            # Write the version information to the trace
            for version in repo.versions(branch):

                # Update the repositories with the common root path.
                version['object'] = os.path.relpath(version['object'], prefix)
                self.writer.writerow(version)
