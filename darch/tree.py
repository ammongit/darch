#
# tree.py
#
# darch - Difference Archiver
# Copyright (c) 2015-2017 Ammon Smith
#
# darch is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# darch is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with darch.  If not, see <http://www.gnu.org/licenses/>.
#

import os

from .log import log
from .util import elide

__all__ = [
    'FileAttrs',
    'Tree',
]

class FileAttrs:
    __slots__ = (
        'path',
        'ctime',
        'mtime',
        'hashsum',
    )

    def __init__(self, path, ctime, mtime, hashsum):
        self.path = path
        self.ctime = ctime
        self.mtime = mtime
        self.hashsum = hashsum

class Tree:
    __slots__ = (
        'path',
        'fsops',
        'files',
    )

    def __init__(self, path, meta, config, fsops):
        self.path = path
        self.fsops = fsops

        for dirpath, dirnames, filenames in os.walk(path):
            log("Scanning {}...".format(elide(dirpath, end='')))
            if os.path.basename(dirpath) == self.config.data_dir:
                continue

            for filename in filenames:
                full_path = os.path.join(path, dirpath, filename)
                if filename in self.config.ignore_files:
                    with # add to ignore
                self.files[full_path] = FileAttrs(full_path, config.hasher, fsops)
                # if mtime or ctime change, recheck hash
