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
        tarball_name = '.'.join((dir_path, self.config['compression']['extension']))
        self.tarball_path = os.path.join(self.config['archive-dir'], tarball_name)
        self.tarball_path = os.path.abspath(self.tarball_path)

        self._dir_check()
        self.fops = get_fops(self.config)
        self.tree = Tree(self.dir_path, self.config, self.fops)

    @staticmethod
    def _passwd_flag(confirm=False):
        passwd = getpass("Enter your password: ")
        if confirm:
            passwd2 = getpass("Verify your password: ")
            if passwd != passwd2:
                log_error("Passwords do not match.")
        return '-p' + passwd

    @staticmethod
    def _print_files(text, paths, bullet='*'):
        if not paths:
            return
        log("Files to %s:" % text, True)
        for path in paths:
            log("%s %s" % (bullet, path), True)

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
                '-t%s' % self.config['compression']['format'],
            ]
            if self.config['encrypted']:
                arguments.append(pflag)
            arguments.append(self.tarball_path)

            if self.fops.call(arguments):
                log_error("Archive failed consistency test.")

    def purge(self):
        self.tree.purge_logs()

    def invalidate(self):
        self.tree.invalidate()

    def scan(self):
        self.tree.scan()

    def extracted(self):
        return os.path.exists(self.dir_path)

    def first(self):
        return not os.path.exists(self.tarball_path)

    def backup(self, move=False):
        log("Backing up archive...", True)
        source = self.tarball_path
        dest = self.tarball_path + '~'
        if move:
            self.fops.move(source, dest)
        else:
            self.fops.copy(source, dest)

    def test(self):
        self._test(self._passwd_flag())

    def create(self):
        log("Creating archive...", True)
        oldcwd = os.getcwd()
        os.chdir(self.tree.main_dir)
        arguments = [
            '7z',
            'a',
            '-t%s' % self.config['compression']['format'],
            '-mx=%d' % self.config['compression']['level'],
        ]
        files = os.listdir('.')
        self._print_files('create', files, '+')
        pflag = self._passwd_flag(True)
        if self.config['encrypted']:
            arguments.append(pflag)
        arguments.append(self.tarball_path)
        arguments += files
        print(arguments)

        if self.fops.call(arguments):
            log("Archive creation failed.")
        os.chdir(oldcwd)
        self.tree.update()
        self.tree.sync()
        self._test(pflag)

    def update(self):
        log("Updating archive...", True)
        oldcwd = os.getcwd()
        os.chdir(self.tree.main_dir)

        dirty = self.tree.dirty.keys()
        self._print_files('update', dirty, '+')
        removed = self.tree.to_remove
        self._print_files('remove', removed, '-')
        metadata = self.tree.metadata_files
        if not dirty and not removed:
            log("Nothing to do.", True)
            return
        pflag = self._passwd_flag()

        if dirty:
            arguments = [
                '7z',
                'a',
                '-t%s' % self.config['compression']['format'],
            ]
            arguments.append(pflag)
            arguments.append(self.tarball_path)
            arguments += dirty
            print(arguments)

            if self.fops.call(arguments):
                log_error("Archive updates failed.")

        if removed:
            arguments = [
                '7z',
                'd',
                '-t%s' % self.config['compression']['format'],
            ]
            arguments.append(pflag)
            arguments.append(self.tarball_path)
            arguments += removed
            print(arguments)

            if self.fops.call(arguments):
                log_error("Archive deletions failed.")

        if metadata:
            arguments = [
                '7z',
                'a',
                '-t%s' % self.config['compression']['format'],
            ]
            arguments.append(pflag)
            arguments.append(self.tarball_path)
            arguments += metadata
            print(arguments)

            if self.fops.call(arguments):
                log_error("Archive metadata update failed.")

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
            '-t%s' % self.config['compression']['format'],
        ]
        if self.config['encrypted']:
            arguments.append(self._passwd_flag())
        arguments.append(self.tarball_path)

        if self.fops.call(arguments):
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

