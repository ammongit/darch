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
from .log import log_error
from .tree import Tree

from getpass import getpass

import glob
import os

class Archive(object):
    def __init__(self, dir_path, config=None):
        if config is None:
            config = default_config()

        self.dir_path = dir_path
        self.tarball_path = os.path.join(config['archive-dir'], dir_path + ".7z")
        self.config = config
        self.tree = Tree()

        if config['dry-run']:
            self.fops = ReadOnlyFileOps()
        else:
            self.fops = FileOps()

        if os.path.exists(dir_path) and not os.path.isdir(dir_path):
            log_error("Extracted path is not a directory.")

    def _passwd_flag(self, confirm=False):
        passwd = getpass("Enter your password: ")
        if confirm:
            passwd2 = getpass("Enter it again: ")
            if passwd != passwd2:
                log_error("Passwords do not match.")
        return '-p' + passwd

    def exists(self):
        return os.path.exists(self.tarball_path)

    def extracted(self):
        return os.path.exists(self.dir_path)

    def backup(self):
        self.fops.move(self.tarball_path, self.tarball_path + "~")

    def create(self):
        arguments = [
            '7z',
            'a',
            '-t7z',
            '-mx=%d' % self.config['compression'],
        ]
        if self.config['encrypted']:
            arguments.append(self._passwd_flag(True))
        arguments.append(self.tarball_path)
        arguments.append(self.dir_path)

        if self.fops.call(arguments):
            log("Archive creation failed.")

        if self.config['test-archive']:
            arguments = [
                '7z',
                't'
                '-t7z',
            ]
            if self.config['encrypted']:
                arguments.append(self._passwd_flag())
            arguments.append(self.tarball_path)

            if self.fops.call(arguments):
                log_error("Archive failed consistency test.")

    def extract(self):
        arguments = [
            '7z',
            'x',
        ]
        if self.config['encrypted']:
            arguments.append(self._passwd_flag())
        arguments.append(self.tarball_path)

        if self.fops.call(arguments):
            pass

    def update(self):
        print("TODO: update")

    def delete(self):
        print("TODO: delete")

    def clear_recent(self):
        log("Clearing recent documents...", True)
        path = os.path.expanduser("~/.local/share/recently-used.xbel")
        self.fops.truncate(path)

        path = os.path.expanduser("~/.thumbnails")
        if os.path.isdir(path):
            path = os.path.expanduser("~/.thumbnails/normal/*")
            for fn in glob.glob(path):
                self.fops.remove(fn)

            path = os.path.expanduser("~/.thumbnails/large/*")
            for fn in glob.glob(path):
                self.fops.remove(fn)
        else:
            path = os.path.expanduser("~/.cache")
            cache_dir = os.environ.get('XDG_CACHE_HOME', path)

            path = os.path.expanduser("~/.cache/thumbnails/normal/*")
            for fn in glob.glob(path):
                self.fops.remove(fn)

            path = os.path.expanduser("~/.cache/thumbnails/large/*")
            for fn in glob.glob(path):
                self.fops.remove(fn)

