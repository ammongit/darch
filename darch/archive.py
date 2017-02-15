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
from .fops import get_fops
from .log import log, log_error
from .tree import Tree

from getpass import getpass
import glob
import os
import subprocess

class Archive(object):
    def __init__(self, dir_path, config=None):
        self.config = default_config if config is None else config
        self.work_path = os.path.basename(dir_path)
        self.dir_path = dir_path
        self.tarball_path = os.path.join(self.config['archive-dir'], dir_path + ".7z")

        self._dir_check()
        self.fops = get_fops(self.config)
        self.tree = Tree(self.dir_path, self.config, self.fops)

    @staticmethod
    def _passwd_flag(confirm=False):
        passwd = getpass("Enter your password: ")
        if confirm:
            passwd2 = getpass("Enter it again: ")
            if passwd != passwd2:
                log_error("Passwords do not match.")
        return '-p' + passwd

    @staticmethod
    def _print_files(text, paths):
        if not paths:
            return
        log("Files to %s:" % text, True)
        for path in paths:
            log("* %s" % path, True)

    def _dir_check(self):
        dir_exists = os.path.exists(self.dir_path)
        tar_exists = os.path.exists(self.tarball_path)

        if dir_exists and not os.path.isdir(self.dir_path):
            log_error("Extracted path is not a directory.")
        if not (dir_exists or tar_exists):
            log_error("Neither archive nor directory exists.")

    def _test(self, pflag):
        if self.config['test-archive']:
            log("Testing archive...", True)
            arguments = [
                '7z',
                't',
            ]
            if self.config['encrypted']:
                arguments.append(pflag)
            arguments.append(self.tarball_path)

            if self.fops.call(arguments, stdout=subprocess.DEVNULL):
                log_error("Archive failed consistency test.")

    def invalidate(self):
        self.tree.invalidate()

    def scan(self):
        self.tree.scan()

    def extracted(self):
        return os.path.exists(self.dir_path)

    def first(self):
        return not os.path.exists(self.tarball_path)

    def backup(self):
        log("Backing up archive...", True)
        self.fops.move(self.tarball_path, self.tarball_path + "~")

    def create(self):
        log("Creating archive...", True)
        oldcwd = os.getcwd()
        os.chdir(self.dir_path)
        arguments = [
            '7z',
            'a',
            '-mx=%d' % self.config['compression'],
        ]
        files = os.listdir('.')
        self._print_files('create', files)
        pflag = self._passwd_flag(True)
        if self.config['encrypted']:
            arguments.append(pflag)
        arguments.append(self.tarball_path)
        arguments += files

        if self.fops.call(arguments, stdout=subprocess.DEVNULL):
            log("Archive creation failed.")
        os.chdir(oldcwd)
        self.tree.update()
        self.tree.sync()
        self._test(pflag)

    def update(self):
        log("Updating archive...", True)
        oldcwd = os.getcwd()
        os.chdir(self.dir_path)

        dirty = self.tree.dirty.keys()
        self._print_files('update', dirty)
        removed = self.tree.to_remove
        self._print_files('remove', removed)
        metadata = self.tree.metadata_files
        if not dirty and not removed:
            log("Nothing to do.", True)
            return
        pflag = self._passwd_flag()

        if metadata:
            arguments = [
                '7z',
                'a',
            ]
            arguments.append(pflag)
            arguments.append(self.tarball_path)
            arguments += self.tree.metadata_files

            if self.fops.call(arguments, stdout=subprocess.DEVNULL):
                log_error("Archive metadata update failed.")

        if dirty:
            arguments = [
                '7z',
                'a',
            ]
            arguments.append(pflag)
            arguments.append(self.tarball_path)
            arguments += dirty

            if self.fops.call(arguments, stdout=subprocess.DEVNULL):
                log_error("Archive updates failed.")

        if removed:
            arguments = [
                '7z',
                'd',
            ]
            arguments.append(pflag)
            arguments.append(self.tarball_path)
            arguments += removed

            if self.fops.call(arguments, stdout=subprocess.DEVNULL):
                log_error("Archive deletions failed.")

        if not dirty and not removed:
            log("Nothing to update.", True)

        os.chdir(oldcwd)
        self.tree.update()
        self.tree.sync()
        self._test(pflag)

    def extract(self):
        log("Extracting archive...", True)
        arguments = [
            '7z',
            'x',
        ]
        if self.config['encrypted']:
            arguments.append(self._passwd_flag())
        arguments.append(self.tarball_path)

        if self.fops.call(arguments, stdout=subprocess.DEVNULL):
            log_error("Archive extraction failed.")

    def delete(self):
        log("Removing old files...", True)
        self.fops.remove_dir(self.dir_path)

    def hash(self):
        self.tree.media_hash()

    def clear_recent(self):
        log("Clearing recent documents...", True)
        path = os.path.expanduser('~/.local/share/recently-used.xbel')
        self.fops.truncate(path)

        path = os.path.expanduser('~/.thumbnails')
        if os.path.isdir(path):
            path = os.path.expanduser('~/.thumbnails/normal/*')
            for fn in glob.glob(path):
                self.fops.remove(fn)

            path = os.path.expanduser('~/.thumbnails/large/*')
            for fn in glob.glob(path):
                self.fops.remove(fn)
        else:
            path = os.path.expanduser('~/.cache')
            cache_dir = os.environ.get('XDG_CACHE_HOME', path)

            path = os.path.expanduser('~/.cache/thumbnails/normal/*')
            for fn in glob.glob(path):
                self.fops.remove(fn)

            path = os.path.expanduser('~/.cache/thumbnails/large/*')
            for fn in glob.glob(path):
                self.fops.remove(fn)

