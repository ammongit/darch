#
# darch.py
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
    'Archive',
]

from .config import default_config
from .fops import FileOps, ReadOnlyFileOps

class Archive(object):
    def __init__(self, dir_path, config=None):
        if config is None:
            config = default_config()

        self.dir_path = dir_path
        self.tarball_path = os.path.join(config['archive-dir'], dir_path + ".7z")
        self.config = config

        if config['dry-run']:
            self.fops = ReadOnlyFileOps()
        else:
            self.fops = FileOps()

    def exists(self):
        return self.fops.exists(self.tarball_path)

    def extracted(self):
        return self.fops.exists(self.dir_path)

    def backup(self):
        self.fops.copy(self.tarball_path, self.tarball_path + "~")

