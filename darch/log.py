#
# log.py
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
    'log',
    'log_error',
    'log_warn',
]

import sys

if sys.stdin.isatty():
    RED_COLOR    = '\033[31m'
    YELLOW_COLOR = '\033[33m'
    RESET_COLOR  = '\033[0m'
else:
    RED_COLOR    = ''
    YELLOW_COLOR = ''
    RESET_COLOR  = ''

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

    def print_error(self, string):
        self("%sError%s: %s" % (RED_COLOR, RESET_COLOR, string), True)
        exit(1)

    def print_warn(self, string):
        self("%sWarning%s: %s" % (YELLOW_COLOR, RESET_COLOR, string), True)

log = Logger()
log_error = log.print_error
log_warn = log.print_warn

