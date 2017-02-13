#
# log.py
#
# darch - Difference Archiver
# Copyright (c) 2015-2016 Ammon Smith
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
    'log',
]

import sys

class Logger(object):
    def __init__(self):
        self.line_length = 0;
        self.needs_newline = False

    def __call__(self, string, perm=False):
        if perm:
            self.line_length = 0
            if self.needs_newline:
                print("\n")
            print(string)
        else:
            if log.line_length:
                print("\r%s\r" % (' ' * log.line_length), end='')
            print(string, end='')
            log.line_length = len(string)
            sys.stdout.flush()
        log.needs_newline = not perm

log = Logger()

