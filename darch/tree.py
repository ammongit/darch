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
from .mhash import MediaHasher

import binascii
import hashlib
import os
import pickle

class Tree(object):
    def __init__(self, main_dir, config, fops):
        self.files = {}
        self.dirty = {}
        self.to_remove = []
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
        self._read(True)
        self.scan()

    def hash(self, path):
        with self.fops.open(path, 'rb') as fh:
            return self._hash(fh.read()).digest()

    def scan(self):
        offset = len(self.main_dir) + 1
        visited = set()
        for dirpath, dirnames, filenames in os.walk(self.main_dir):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                path = full_path[offset:]
                visited.add(path)
                st = os.stat(full_path)
                ctime = int(st.st_ctime)
                mtime = int(st.st_mtime)

                # Add files to dirty list
                try:
                    ctime2, mtime2, hashsum2 = self.files[path]
                    ctime2 = int(ctime2)
                    mtime2 = int(mtime2)

                    if ctime != ctime2 or mtime != mtime2:
                        hashsum = self.hash(full_path)
                    else:
                        hashsum = hashsum2
                except KeyError:
                    hashsum = self.hash(full_path)
                    hashsum2 = None

                entry = (ctime, mtime, hashsum)
                if hashsum != hashsum2:
                    self.dirty[path] = entry
                    self.hashes[hashsum] = self.hashes.get(hashsum, [])
                    self.hashes[hashsum].append(path)

        # Find removed files
        for path, entry in self.files.items():
            if path not in visited:
                self.to_remove.append(path)
                try:
                    hashsum = entry[2]
                    self.hashes[hashsum].remove(path)
                except KeyError:
                    pass

    def media_hash(self):
        self.
        mhash = MediaHasher(self, self.fops, self.config)
        print("TODO")

    def update(self):
        for path, entry in self.dirty.items():
            self.files[path] = entry

        for path in self.to_remove:
            del self.files[path]

        self.dirty = {}
        self.to_remove = []

    def sync(self):
        path = os.path.join(self.data_dir, self.config['tree-file'])
        with self.fops.open(path, 'wb') as fh:
            pickle.dump(self.files, fh)

        path = os.path.join(self.data_dir, self.config['duplicates-log'])
        with self.fops.open(path, 'w') as fh:
            for hashsum, paths in self.hashes.items():
                if len(paths) >= 2:
                    hex_hash = binascii.hexlify(hashsum).decode('utf-8')
                    fh.write("%s: %s\n" % (hex_hash, ';'.join(paths)))

    def _read(self, write=False):
        path = os.path.join(self.data_dir, self.config['tree-file'])
        if not os.path.exists(path):
            if write:
                self.sync()
            return
        with self.fops.open(path, 'rb') as fh:
            obj = pickle.load(fh)
        if type(obj) != dict:
            log_error("Unpickled object is not a dict.")
        self.files = obj

