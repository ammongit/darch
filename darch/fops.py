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

class FileOps(object):
    def __init__(self):
        self.open = open

    def exists(self, path):
        return os.path.exists(path)

    def stat(self, path):
        return os.stat(path)

def _dummy_open(path, mode='r'):
    with open(path, 'r') as fh:
        text = fh.read()
    return io.StringIO(text)

class ReadOnlyFileOps(FileOps):
    def __init__(self):
        FileOps.__init__(self)
        self.open = _dummy_open

