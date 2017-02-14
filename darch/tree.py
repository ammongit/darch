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

from .log import log, log_error

import os
import pickle

class Tree(object):
    def __init__(self, main_dir, config, fops):
        self.files = {}
        self.dirty = {}
        self.fops = fops
        self.config = config
        self.main_dir = main_dir
        self.data_dir = os.path.join(main_dir, self.config['data-dir'])
        self.ignore = None

        if not os.path.isdir(self.main_dir):
            log_error("Archive main directory does not exist: %s" % self.main_dir)
        if not os.path.isdir(self.data_dir):
            self.fops.mkdir(self.data_dir)
        self.scan()
        self.sync()

    def scan(self):
        for dirpath, dirnames, filenames in os.walk(self.main_dir):
            for dirname in dirnames:
                print("DIR %s" % dirname)
            for filename in filenames:
                print("FILE %s" % filename)

    def update(self):
        print("TODO tree.update")

    def sync(self):
        path = os.path.join(self.directory, "tree.pickle")
        with self.fops.open(path, 'wb') as fh:
            pickle.dump(self.files, fh)

