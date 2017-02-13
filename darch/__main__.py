#
# __main__.py
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

__all__ = []

DESCRIPTION    = "Manage a hashed media archive."
HELP_CONFIG    = "Specify the configuration file."
HELP_DRYRUN    = "Don't actually do anything, just print the results."
HELP_UPDATE    = "Update the archive only, leaving the files extracted."
HELP_HASHONLY  = "Only run the media hash. Do not affect the archive. Ignores any -u options set."
HELP_FULL      = "Recreate the full archive. Doesn't use the difference algorithm."
HELP_ARGUMENTS = "The archives you wish to operate on."

from .archive import Archive
from .config import default_config, load_config

import argparse
import os
import sys

def config_path():
    path = "%s/darch.json" % os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
    if os.path.exists(path):
        return path
    else:
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-c', '--config', help=HELP_CONFIG)
    parser.add_argument('-n', '--dry-run', action='store_true', default=None, help=HELP_DRYRUN)
    parser.add_argument('-u', '--update-only', action='store_true', help=HELP_UPDATE)
    parser.add_argument('-m', '--hash-only', action='store_true', help=HELP_HASHONLY)
    parser.add_argument('-F', '--full', action='store_true', help=HELP_FULL)
    parser.add_argument('archive-dir', nargs='+', help=HELP_ARGUMENTS)
    args = parser.parse_args()

    archives = getattr(args, 'archive-dir')
    if args.config:
        config = load_config(args.config)
    else:
        path = config_path()
        if path:
            config = load_config(path)
        else:
            config = default_config()

    if args.dry_run is not None:
        config['dry-run'] = args.dry_run

    for archive in archives:
        archv = Archive(archive, config)
        if archv.exists():
            archv.create()
            exit()

        if args.hash_only:
            archv.hash()
            exit()

        if archv.extracted():
            archv.update()
            if not args.update_only:
                archv.delete()
        else:
            archv.extract()

