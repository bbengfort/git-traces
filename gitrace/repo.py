# gitrace.repo
# Handles the interface to a Git repository for extraction.
#
# Author:   Benjamin Bengfort <bengfort@cs.umd.edu>
# Created:  Thu May 05 12:10:03 2016 -0400
#
# Copyright (C) 2016 University of Maryland
# For license information, see LICENSE.txt
#
# ID: repo.py [] benjamin@bengfort.com $

"""
Handles the interface to a Git repository for extraction.
"""

##########################################################################
## Imports
##########################################################################

import os
import git

EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


##########################################################################
## Repository Manager
##########################################################################

class RepoManager(object):
    """
    A wrapper for a Git repository to handle extraction.
    """

    def __init__(self, path, branch='master'):
        self.repo   = None # Will be initialized by path setter
        self.path   = path # Will be normalized by path setter
        self.branch = branch

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        """
        Sets the path an initializes the repository
        """
        path = os.path.expanduser(path)
        path = os.path.expandvars(path)
        path = os.path.abspath(path)

        if not os.path.isdir(path):
            raise Exception("'{}' is not a directory!".format(args.repo))

        self._path = path

        try:
            self.repo = git.Repo(path)
        except git.InvalidGitRepositoryError:
            raise Exception("'{}' is not a Git repository!".format(path))

    def versions(self):
        """
        Generator that yields commit, diff pairs. (Can be grouped by commit).
        """
        for commit in self.repo.iter_commits(self.branch):
            for path, stats in commit.stats.files.items():
                data = {
                    'commit': commit.hexsha,
                    'object': os.path.join(self.path, path),
                    'author': commit.author.email,
                    'timestamp': commit.authored_datetime.strftime("%Y-%m-%dT%H:%M:%S%z"),
                }
                data.update(stats)
                yield data
