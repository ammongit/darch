#
# ignore.py
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
    'Ignore',
]

from fnmatch import fnmatch
import pathspec
import re
import os

class Ignore:
    def __init__(self):
        self.specs = []

    def add(self, path_dir, lines):
        spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, lines)
        self.specs.append((spec, path_dir))

    # Returns True if the file should be ignored
    def matches(self, path):
        for spec, path_dir in self.specs:
            if path.startswith(path_dir):
                offset = len(path_dir) + 1
                path = path[offset:]
                if spec.match_file(path):
                    return True
        return False

