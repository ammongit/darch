#
# mhash.py
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
    'MediaHasher',
]

from .log import log
from .util import elide

from typing import Optional
import binascii
import os

class MediaHasher:
    __slots__ = (
        'archv',
        'fsops',
        'config',
        'confirm_rest',
        'queued',
        'changed',
        'extensions',
        'skip_extensions',
    )

    def __init__(self, arch):
        self.archv = archv
        self.fsops = archv.fsops
        self.config = archv.config
        self.confirm_rest = False
        self.queued = []
        self.changed = {}
        self.extensions = frozenset(config.extensions)
        self.skip_extensions = frozenset(config.skip_extensions)

    def _new_filename(self, filename, hashsum) -> Optional[str]:
        name, ext = os.path.splitext(filename)
        ext = self.config.rename_extensions.get(ext, ext)

        if ext not in self.extensions or ext in self.skip_extensions:
            return None

        directory = os.path.dirname(name)
        new_name = binascii.hexlify(hashsum).decode('utf-8')
        filename = os.path.extsep.join(new_name, ext)
        return os.path.join(directory, filename)

    def confirm(self, message='Ok'):
        if self.config.always_yes or self.confirm_rest:
            return True

        response = input(">> {}?\n[Y/n/a/q] ".format(message))
        response = response.lower().strip()

        if response in ('', 'y', 'yes'):
            return True
        elif response in ('n', 'no'):
            return False
        elif response in ('a', 'always'):
            self.confirm_rest = True
            return True
        elif response in ('q', 'quit', 'exit'):
            exit(2)
        else:
            return False

    def build(self):
        log("Building hash changes...")
        for path, (ctime, mtime, hashsum) in self.tree.files.items():
            if self.tree.ignore.matches(path):
                log("Ignoring {}...".format(path))
                continue

            new_path = self._new_filename(path, hashsum)
            if new_path is None or path == new_path:
                continue

            self.queued.append((path, new_path))

    def apply(self):
        log("Applying hash changes...")
        for old_path, new_path in self.queued:
            log("'{}' -> '{}'".format(old_path, elide(os.path.basename(new_path))), True)
            if os.path.exists(new_path):
                if not self.confirm("Delete '{}'".format(new_path)):
                    continue

                log("Removed '{}'.".format(new_path), True)
                self.fsops.remove(new_path)
            self.fops.rename(old_path, new_path)
            self.changed[old_path] = new_path
        self.queued = []

        # Write to undo log
        self.archv.meta.hashed = self.changed

    def undo(self):
        # Read from undo log
        self.changed = self.archv.meta.hashed

        for old_path, new_path in self.changed.items():
            log("Undo: '{}' -> '{}'".format(new_path, elide(os.path.basename(old_path))), True)
            self.fops.rename(new_path, old_path)
