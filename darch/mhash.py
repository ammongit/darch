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
from .tree import Tree

class MediaHasher(object):
    def __init__(self, tree, fops, config):
        self.tree = tree
        self.fops = fops
        self.config = config
        self.confirm = True

    def _transform_ext(self, filename):
        pass

    def confirm(self, message="Ok"):
        if self.config['always-yes'] and not self.confirm:
            return True
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

    def undo(self):
        print("TODO")
        pass

