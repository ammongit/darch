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

from .log import log, log_next

class MediaHasher(object):
    def __init__(self, tree, fops, config):
        self.tree = tree
        self.fops = fops
        self.config = config
        self.confirm = True
        self.changes = {}

    def _rename_file(self, filename, hashsum):
        parts = filename.split('.')
        # No '.' in filename
        if len(parts) == 1:
            return None

        # Rename specified extensions
        ext = parts[-1].lower()
        try:
            ext = self.config['rename-extensions'][ext]
        except KeyError:
            pass

        pass

    def confirm(self, message="Ok"):
        if self.config['always-yes'] and not self.confirm:
            return True
        log_next()
        response = input("%s?\n[Y/n/a/q] " % message).lower().strip()
        if response in ('', 'y', 'yes'):
            return True
        elif response in ('n', 'no'):
            return False
        elif response in ('a', 'always'):
            self.confirm = False
            return True
        elif response in ('q', 'quit', 'exit'):
            raise KeyboardInterrupt
        else:
            return False

    def build_changes(self):
        log("Building hash changes...", True)
        for path, entry in self.tree.files.items():
            ctime, mtime, hashsum = entry
            new_path = self._rename_file(path, hashsum)
            if new_path is None:
                continue

    def apply_changes(self):
        log("Applying hash changes...", True)
        self.changes = {}

    def undo(self):
        print("TODO")
        pass

