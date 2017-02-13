#
# __main__.py
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
    'main',
]

DESCRIPTION    = "Manage a hashed media archive."
HELP_DRYRUN    = "Don't actually do anything, just print the results."
HELP_CONFIG    = "Specify the configuration file."
HELP_ARGUMENTS = "The archives you wish to operate on."

from .config import load_config

import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-c', '--config', help=HELP_CONFIG)
    parser.add_argument('-n', '--dry-run', action='store_true', default=None, help=HELP_DRYRUN)
    parser.add_argument('archive-dir', nargs='+', help=HELP_ARGUMENTS)
    args = parser.parse_args()

    archives = getattr(args, 'archive-dir')
    config = load_config(args.config)

    if args.dry_run is not None:
        config['dry-run'] = args.dry_run

    print(config)

