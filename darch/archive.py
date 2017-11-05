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

import os

from .fsops import FsOps
from .log import log, log_error
from .meta import Meta
from .tree import Tree

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
        'meta',
        'tree',
    )

    def __init__(self, archive, config):
        tar = os.path.extsep.join(archive, config.compression.extension)
        self.tar_path = os.path.join(config.archive_dir, tar)
        if os.path.isabs(config.extract_dir):
            self.dir_path = os.path.join(config.extract_dir, archive)
        else:
            self.dir_path = os.path.join(config.archive_dir, config.extract_dir, archive)
        self.meta_dir = os.path.join(self.dir_path, config.data_dir)
        self.config = config
        self.fsops = FsOps.from_config(config)
        self.meta = Meta(self.dir_path, self.fsops)
        self.tree = Tree(self.dir_path, self.meta)

    def clear_recent(self):
        paths = (
            os.path.expanduser('~/.cache/thumbnails/normal'),
            os.path.expanduser('~/.cache/thumbnails/large'),
            os.path.expanduser('~/.thumbnails/normal'),
            os.path.expanduser('~/.thumbnails/large'),
            os.path.expanduser('~/.local/share/recently-used.xbel'),
            os.path.expanduser('~/.local/share/user-places.xbel'),
        )

        for path in paths:
            if not os.path.exists(path):
                continue

            if os.path.isdir(path):
                self.fsops.remove_dir(path)
            else:
                self.fsops.remove(path)

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
        log("Deleting archive...", True)
        self.fsops.remove(self.tar_path)

    def tar_extract(self, passwd):
        log("Extracting archive...", True)
        arguments = [
            '7z',
            'x',
            '-t{}'.format(self.config.compression.format),
            self.tar_path,
        ]
        if self.fsops.call(arguments, cwd=

    def tar_test(self, passwd):
        log("Testing archive...", True)
        arguments = [
            '7z',
            't',
            '-t{}'.format(self.config.compression.format),
        ]

        if self.config.encrypted:
            arguments.append('-p{}'.format(passwd))

        arguments.append(self.tar_path)

        if self.fsops.call(arguments):
            log_error("Archive failed consistency test!")
