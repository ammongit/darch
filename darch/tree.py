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

import hashlib
import os
import pickle

class Tree(object):
    def __init__(self, main_dir, config, fops):
        self.files = {}
        self.dirty = {}
        self.hashes = {}
        self.fops = fops
        self.config = config
        self.main_dir = main_dir
        self.data_dir = os.path.join(main_dir, self.config['data-dir'])
        self.ignore = None

        try:
            self._hash = getattr(hashlib, config['hash-algorithm'])
        except AttributeError:
            log_error("No such hash algorithm: %s" % config['hash-algorithm'])

        if not os.path.isdir(self.main_dir):
            log_error("Archive main directory does not exist: %s" % self.main_dir)
        if not os.path.isdir(self.data_dir):
            self.fops.mkdir(self.data_dir)
        self.scan()
        self._read()
        self.sync()

    def hash(self, path):
        with self.fops.open(path, 'rb') as fh:
            return self._hash(fh.read()).hexdigest()

    def scan(self):
        offset = len(self.main_dir) + 1
        for dirpath, dirnames, filenames in os.walk(self.main_dir):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                path = full_path[offset:]
                st = os.stat(full_path)
                hashsum = self.hash(full_path)

                # Add files to dirty list
                entry = (st.st_ctime, st.st_mtime, hashsum)
                try:
                    ctime, mtime, hashsum2 = self.files[path]
                    if hashsum != hashsum:
                        self.dirty[path] = entry
                except KeyError:
                    self.dirty[path] = entry

                self.hashes[hashsum] = self.hashes.get(hashsum, [])
                self.hashes[hashsum].append(path)

        # Remove old hashlist files
        new_hashes = {}
        for hashsum, paths in self.hashes.items():
            new_paths = []
            for path in paths:
                path = os.path.join(self.main_dir, path)
                if os.path.exists(path):
                    new_paths.append(path)
            self.hashes[hashsum] = new_paths

    def update(self):
        for path, entry in self.dirty:
            pass

    def sync(self):
        path = os.path.join(self.data_dir, 'tree.pickle')
        with self.fops.open(path, 'wb') as fh:
            pickle.dump(self.files, fh)

        path = os.path.join(self.data_dir, 'duplicates.txt')
        with self.fops.open(path, 'w') as fh:
            for hashsum, paths in self.hashes.items():
                if len(paths) >= 2:
                    fh.write("%s: %s\n" % (hashsum, ';'.join(paths)))

    def _read(self):
        path = os.path.join(self.data_dir, 'tree.pickle')
        if not os.path.exists(path):
            return
        with self.fops.open(path, 'rb') as fh:
            obj = pickle.load(fh)
        if type(obj) != dict:
            log_error("Unpickled object is not a dict.")

