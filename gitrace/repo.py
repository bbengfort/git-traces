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

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
EMPTY_TREE_SHA   = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


##########################################################################
## Repository Manager
##########################################################################

class RepoManager(object):
    """
    A wrapper for a Git repository to handle extraction.
    """

    def __init__(self, path):
        self.repo   = None # Will be initialized by path setter
        self.path   = path # Will be normalized by path setter

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

    def branches(self):
        """
        Lists the branches that are known by the Git repository.
        """
        return [
            branch.replace("*", "").strip()
            for branch in self.repo.git.branch().splitlines()
        ]

    def versions(self, branch='master'):
        """
        Generator that yields commit, diff pairs. (Can be grouped by commit).
        """
        for commit in self.repo.iter_commits(branch):
            parent = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
            diffs  = {
                diff.a_path: diff for diff in commit.diff(parent)
            }

            for path, stats in commit.stats.files.items():
                diff = diffs.get(path)
                if not diff:
                    for diff in diffs.values():
                        if diff.b_path == path and diff.renamed:
                            break

                if diff.b_blob is None and diff.deleted_file:
                    size = diff.a_blob.size * -1
                elif diff.a_blob is None and diff.new_file:
                    size = diff.b_blob.size
                else:
                    size = diff.a_blob.size - diff.b_blob.size

                data = {
                    'commit': commit.hexsha,
                    'object': os.path.join(self.path, path),
                    'author': commit.author.email,
                    'timestamp': commit.authored_datetime.strftime(DATE_TIME_FORMAT),
                    'size': size,
                    'renamed': diff.renamed,
                    'deleted': diff.deleted_file,
                    'added': diff.new_file,
                }
                data.update(stats)
                yield data


if __name__ == '__main__':
    repo = RepoManager('~/Repos/tmp/redis')
    print repo.branches()
    for version in repo.versions(branch='unstable'):
        print version
