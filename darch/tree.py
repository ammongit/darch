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

from .ignore import Ignore
from .log import log, log_error
from .mhash import MediaHasher
from .util import elide

import binascii
import hashlib
import os
import pickle

class Tree(object):
    def __init__(self, main_dir, config, fsops):
        self.files = {}
        self.dirty = {}
        self.to_remove = []
        self.metadata_files = []
        self.hashes = {}
        self.fsops = fsops
        self.config = config
        self.main_dir = main_dir
        self.data_dir = os.path.join(main_dir, self.config['data-dir'])
        self.ignore = Ignore()

        try:
            self._hash_func = getattr(hashlib, config['hash-algorithm'])
        except AttributeError:
            log_error("No such hash algorithm: %s" % config['hash-algorithm'])

        self.has_dir = os.path.isdir(self.main_dir)
        if self.has_dir:
            self._read()
        self.scan()

    def _check_data_dir(self):
        if self.has_dir:
            return
        if os.path.isdir(self.main_dir) and not os.path.isdir(self.data_dir):
            self.fops.mkdir(self.data_dir)
            self.no_dir = False

    def _hash(self, path):
        with self.fops.open(path, 'rb') as fh:
            return self._hash_func(fh.read()).digest()

    def purge_logs(self):
        self._check_data_dir()
        logs = ('duplicates-log', 'hash-log')
        files = map(lambda x: os.path.join(self.data_dir, self.config[x]), logs)
        for fn in files:
            self.fops.truncate(fn)

    def invalidate(self):
        self.files = {}
        self.dirty = {}
        self.to_remove = []
        self.metadata_files = []
        self.hashes = {}

    def scan(self):
        offset = len(self.main_dir) + 1
        visited = set()
        self.metadata_files = []
        for dirpath, dirnames, filenames in os.walk(self.main_dir):
            log("Scanning %s..." % elide(dirpath, end=''))
            if os.path.basename(dirpath) == self.config['data-dir']:
                y = lambda x: os.path.join(self.config['data-dir'], x)
                self.metadata_files += map(y, filenames)
                continue
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                path = full_path[offset:]
                visited.add(path)
                st = os.stat(full_path)
                ctime = int(st.st_ctime)
                mtime = int(st.st_mtime)

                if filename == self.config['ignore-file']:
                    with self.fops.open(full_path, 'r') as fh:
                        self.ignore.add(dirpath[offset:], fh.readlines())

                # Add files to dirty list
                try:
                    ctime2, mtime2, hashsum2 = self.files[path]
                    if ctime != ctime2 or mtime != mtime2:
                        # Might be modified, recheck hash
                        hashsum = self._hash(full_path)
                    else:
                        hashsum = hashsum2
                except KeyError:
                    # New file
                    hashsum = self._hash(full_path)
                    hashsum2 = None

                entry = (ctime, mtime, hashsum)
                if hashsum != hashsum2:
                    self.dirty[path] = entry
                    l = self.hashes.get(hashsum, [])
                    l.append(path)
                    self.hashes[hashsum] = l

        # Find removed files
        for path, entry in self.files.items():
            if path not in visited:
                self.to_remove.append(path)
                try:
                    hashsum = entry[2]
                    self.hashes[hashsum].remove(path)
                except (KeyError, ValueError):
                    pass

    def media_hash(self):
        self._check_data_dir()
        mhash = MediaHasher(self, self.fops, self.config)
        mhash.build_changes()
        mhash.apply_changes()

    def update(self):
        for path, entry in self.dirty.items():
            self.files[path] = entry
        for path in self.to_remove:
            del self.files[path]
        self.dirty = {}
        self.to_remove = []

    def sync(self):
        self._check_data_dir()
        path = os.path.join(self.data_dir, self.config['tree-file'])
        with self.fops.open(path, 'wb') as fh:
            pickle.dump(self.files, fh)

        path = os.path.join(self.data_dir, self.config['duplicates-log'])
        with self.fops.open(path, 'w') as fh:
            for hashsum, paths in self.hashes.items():
                if len(paths) >= 2:
                    hex_hash = binascii.hexlify(hashsum).decode('utf-8')
                    fh.write("%s: %s\n" % (hex_hash, ';'.join(paths)))

    def _read(self):
        self._check_data_dir()
        path = os.path.join(self.data_dir, self.config['tree-file'])
        if not os.path.exists(path):
            return
        with self.fops.open(path, 'rb') as fh:
            obj = pickle.load(fh)
        if type(obj) != dict:
            log_error("Unpickled object is not a dict.")
        self.files = obj
