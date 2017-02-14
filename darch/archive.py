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
from .log import log, log_error
from .tree import Tree

from getpass import getpass

import glob
import os

class Archive(object):
    def __init__(self, dir_path, config=None):
        self.dir_path = dir_path
        self.config = default_config if config is None else config
        self.tarball_path = os.path.join(self.config['archive-dir'], dir_path + ".7z")
        self.fops = ReadOnlyFileOps() if self.config['dry-run'] else FileOps()
        self.data_path = os.path.join(self.dir_path, self.config['output-dir'])
        self.tree = Tree(self.data_path, self.fops)
        if os.path.exists(dir_path) and not os.path.isdir(dir_path):
            log_error("Extracted path is not a directory.")

    @staticmethod
    def _passwd_flag(confirm=False):
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
        log("Backing up archive...", True)
        self.fops.move(self.tarball_path, self.tarball_path + "~")

    def create(self):
        log("Creating archive...", True)
        arguments = [
            '7z',
            'a',
            '-t7z',
            '-mx=%d' % self.config['compression'],
        ]
        pflag = self._passwd_flag(True)
        if self.config['encrypted']:
            arguments.append(pflag)
        arguments.append(self.tarball_path)
        arguments.append(self.dir_path)

        if self.fops.call(arguments):
            log("Archive creation failed.")

        if self.config['test-archive']:
            arguments = [
                '7z',
                't',
                '-t7z',
            ]
            if self.config['encrypted']:
                arguments.append(pflag)
            arguments.append(self.tarball_path)

            if self.fops.call(arguments):
                log_error("Archive failed consistency test.")

    def update(self):
        log("Updating archive...", True)
        arguments = [
            '7z',
            'a',
            self.tarball_path,
        ]
        arguments += self.tree.dirty_files()

        if self.fops(arguments):
            log_error("Archive update failed.")
        tree.sync()

    def extract(self):
        log("Extracting archive...", True)
        arguments = [
            '7z',
            'x',
        ]
        if self.config['encrypted']:
            arguments.append(self._passwd_flag())
        arguments.append(self.tarball_path)

        if self.fops.call(arguments):
            log_error("Archive extraction failed.")

    def delete(self):
        log("Removing old files...", True)
        self.fops.remove_dir(self.dir_path)

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

