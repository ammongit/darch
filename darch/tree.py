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

__all__ = [
    'Tree',
]

from .log import log

import os
import pickle

class Tree(object):
    def __init__(self, directory, fops):
        self.files = {}
        self.dirty = {}
        self.fops = fops
        self.directory = directory

        self.scan()

    def scan(self):
        for dirpath, dirnames, filenames in os.walk(self.directory):
            print(dirpath, dirnames, filenames)

    def update(self):
        print("TODO tree.update")

    def sync(self):
        if not os.path.isdir(self.directory):
            self.fops.mkdir(self.directory)
        path = os.path.join(self.directory, "tree.pickle")
        with self.fops.open(path, 'wb') as fh:
            pickle.dump(self.files, fh)

