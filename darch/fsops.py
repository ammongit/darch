#
# fsops.py
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
    'FsOps',
    'ReadOnlyFsOps',
]

from .log import log_error

try:
    from send2trash import send2trash
except ImportError:
    def send2trash(path):
        log_error("'send2trash' module not found.")

import io
import os
import shutil
import subprocess

class FsOps:
    __slots__ = (
        'open',
        'tree',
        'use_trash',
        'rename',
    )

    @staticmethod
    def from_config(config) -> FsOps:
        if config.dry_run:
            return ReadOnlyFsOps()
        else:
            return FsOps(config.use_trash)

    def __init__(self, tree, use_trash=False):
        self.open = open
        self.tree = tree
        self.use_trash = use_trash
        self.rename = self.move

    def call(self, arguments, *args, **kwargs):
        return subprocess.call(arguments, *args, **kwargs)

    def copy(self, old_path, new_path):
        shutil.copy2(old_path, new_path)

    def move(self, old_path, new_path):
        os.rename(old_path, new_path)

    def remove(self, path):
        if self.use_trash:
            send2trash(path)
        else:
            os.remove(path)

    def remove_dir(self, path):
        shutil.rmtree(path)

    def mkdir(self, path):
        os.mkdir(path)

    def truncate(self, path, offset=0):
        os.truncate(path, offset)

def _bin_open(path, mode):
    try:
        with open(path, 'rb') as fh:
            data = fh.read()
    except IOError:
        data = b''
    return io.BytesIO(data)

def _str_open(path, mode):
    try:
        with open(path, 'r') as fh:
            text = fh.read()
    except IOError:
        text = ''
    return io.StringIO(text)

def _dummy_open(path, mode='r'):
    func = _bin_open if 'b' in mode else _str_open
    return func(path, mode)

class ReadOnlyFsOps(FsOps):
    def __init__(self):
        super().__init__(self)
        self.open = _dummy_open

    def call(self, arguments, *args, **kwargs):
        print("<CALL> %s" % (' '.join(arguments)))

    def copy(self, old_path, new_path):
        print("<COPY> %s <- %s" % (new_path, old_path))

    def move(self, old_path, new_path):
        print("<MOVE> %s -> %s" % (old_path, new_path))

    def remove(self, path):
        print("<REMOVE> %s" % path)

    def remove_dir(self, path):
        print("<RMDIR> %s" % path)

    def mkdir(self, path):
        print("<MKDIR> %s" % path)

    def truncate(self, path, offset=0):
        print("<TRUNCATE> %s [%d]" % (path, offset))
