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

import binascii
import os

class MediaHasher(object):
    def __init__(self, tree, fops, config):
        self.tree = tree
        self.fops = fops
        self.config = config
        self.do_confirm = True
        self.changes = []
        self.extensions = frozenset(config['extensions'])

    def _rename_file(self, filename, hashsum):
        parts = filename.split('.')
        # No '.' in filename
        if len(parts) == 1:
            return None

        # Rename specified extensions
        base = '.'.join(parts[:-1])
        ext = parts[-1].lower()
        try:
            ext = self.config['rename-extensions'][ext]
        except KeyError:
            pass

        if ext not in self.extensions:
            return None

        directory = os.path.dirname(base)
        hashsum = binascii.hexlify(hashsum).decode('utf-8')
        return os.path.join(directory, '.'.join((hashsum, ext)))

    def confirm(self, message="Ok"):
        if self.config['always-yes'] and not self.do_confirm:
            return True
        response = input("\n%s?\n[Y/n/a/q] " % message).lower().strip()
        if response in ('', 'y', 'yes'):
            return True
        elif response in ('n', 'no'):
            return False
        elif response in ('a', 'always'):
            self.do_confirm = False
            return True
        elif response in ('q', 'quit', 'exit'):
            raise KeyboardInterrupt
        else:
            return False

    def build_changes(self):
        log("Building hash changes...", True)
        for path, entry in self.tree.files.items():
            log("Considering %s..." % path)
            ctime, mtime, hashsum = entry
            if self.tree.ignore.check(path):
                continue
            new_path = self._rename_file(path, hashsum)
            if new_path is None or path == new_path:
                continue

            # Modify file tree
            self.changes.append((path, new_path))
            self.tree.to_remove.append(path)
            self.tree.dirty[new_path] = entry

    def apply_changes(self):
        log("Applying hash changes...", True)
        old_cwd = os.getcwd()
        os.chdir(self.tree.main_dir)
        to_log = []
        for old_path, new_path in self.changes:
            log("'%s' -> '%s'" % (old_path, os.path.basename(new_path)), True)
            to_log.append("%s:%s" % (old_path, new_path))
            if os.path.exists(new_path):
                if not self.confirm("Delete '%s'" % new_path):
                    continue
                log("Removed '%s'." % new_path, True)
                self.fops.remove(new_path)
            self.fops.rename(old_path, new_path)
        self.changes = []
        hashed_file = os.path.join(self.tree.data_dir, self.config['hash-log'])
        with self.fops.open(hashed_file, 'a') as fh:
            fh.write('~\n')
            fh.write('\n'.join(to_log))
        os.chdir(old_cwd)

    def undo(self):
        raise NotImplementedError

