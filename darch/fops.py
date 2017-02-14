#
# fops.py
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
    'FileOps',
    'ReadOnlyFileOps',
]

import io
import os
import shutil
import subprocess

class FileOps(object):
    def __init__(self):
        self.open = open

    def call(self, arguments, *args, **kwargs):
        return subprocess.call(arguments, *args, **kwargs)

    def copy(self, old_path, new_path):
        shutil.copy2(old_path, new_path)

    def move(self, old_path, new_path):
        os.rename(old_path, new_path)

    def remove(self, path):
        os.remove(path)

    def remove_dir(self, path):
        shutil.rmtree(path)

    def mkdir(self, path):
        os.mkdir(path)

    def truncate(self, path, offset=0):
        os.truncate(path, offset)

def _dummy_open(path, mode='r'):
    with open(path, 'r') as fh:
        text = fh.read()
    return io.BytesIO(text.encode('utf-8'))

class ReadOnlyFileOps(FileOps):
    def __init__(self):
        FileOps.__init__(self)
        self.open = _dummy_open

    def call(self, arguments, *args, **kwargs):
        print("call: %s" % (' '.join(arguments)))

    def copy(self, old_path, new_path):
        print("copy: %s <- %s" % (new_path, old_path))

    def remove(self, path):
        print("remove: %s" % path)

    def remove_dir(self, path):
        print("remove_dir: %s" % path)

    def mkdir(self, path):
        print("mkdir: %s" % path)

    def truncate(self, path, offset=0):
        print("truncate: %s [%d]" % (path, offset))

