#
# archive.py
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

from .fsops import FsOps
from .tree import Tree
import os

__all__ = [
    'Archive',
]

class Archive:
    __slots__ = (
        'dir_path',
        'tar_path',
        'meta_dir',
        'config',
        'fsops',
        'tree',
    )

    def __init__(self, archive, config):
        self.dir_path = os.path.join(config.archive_dir, archive)
        self.tar_path = os.path.extsep.join(self.dir_path, config.compression.extension)
        self.meta_dir = os.path.join(self.dir_path, config.data_dir)
        self.config = config
        self.fsops = FsOps.from_config(config)
        self.tree = Tree()

    def open_meta(self):
        raise NotImplementedError

    def clear_recent(self):
        raise NotImplementedError

    def purge_logs(self):
        raise NotImplementedError

    def build_tree(self):
        raise NotImplementedError

    def dir_exists(self):
        return os.path.isdir(self.dir_path)

    def dir_delete(self):
        self.fsops.remove_dir(self.dir_path)

    def tar_exists(self):
        return os.path.isfile(self.tar_path)

    def tar_create(self, passwd):
        raise NotImplementedError

    def tar_update(self, passwd):
        raise NotImplementedError

    def tar_delete(self):
        self.fsops.remove(self.tar_path)

    def tar_extract(self, passwd):
        raise NotImplementedError
