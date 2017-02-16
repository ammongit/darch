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
HELP_DIRECTORY = "Switch to this directory before running anything."
HELP_DRYRUN    = "Don't actually do anything, just print the results."
HELP_UPDATE    = "Update the archive only, leaving the files extracted."
HELP_HASHONLY  = "Only run the media hash. Do not affect the archive. Ignores any -u options set."
HELP_TEST      = "Test the archive after modifying it."
HELP_FULL      = "Recreate the full archive. Doesn't use the difference algorithm."
HELP_NOBACKUP  = "Don't create a copy of the archive before updating it."
HELP_YES       = "Automatically answer 'yes' to every question prompt."
HELP_PURGELOGS = "Clean out the log files created by the archiver before running."
HELP_ARGUMENTS = "The archives you wish to operate on."

from .archive import Archive
from .config import default_config, load_config
from .log import log, log_error

import argparse
import os
import sys

def config_path():
    path = "%s/darch.json" % os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
    if os.path.exists(path):
        return path
    else:
        return None

def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-c', '--config', help=HELP_CONFIG)
    parser.add_argument('-d', '--directory', default=None, help=HELP_DIRECTORY)
    parser.add_argument('-n', '--dry-run', action='store_true', default=None, help=HELP_DRYRUN)
    parser.add_argument('-u', '--update-only', action='store_true', help=HELP_UPDATE)
    parser.add_argument('-m', '--hash-only', action='store_true', help=HELP_HASHONLY)
    parser.add_argument('-t', '--test', action='store_true', default=None, help=HELP_TEST)
    parser.add_argument('-F', '--full', action='store_true', help=HELP_FULL)
    parser.add_argument('-B', '--no-backup', action='store_true', help=HELP_NOBACKUP)
    parser.add_argument('-y', '--always-yes', action='store_true', default=None, help=HELP_YES)
    parser.add_argument('-P', '--purge-logs', action='store_true', help=HELP_PURGELOGS)
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
    if args.always_yes is not None:
        config['always-yes'] = args.always_yes
    if args.test is not None:
        config['test-archive'] = args.test

    for archive in archives:
        name = os.path.basename(archive)
        if args.directory:
            os.chdir(args.directory)
        archv = Archive(archive, config)

        if args.purge_logs:
            archv.purge()

        if args.hash_only:
            log("[Hashing] %s" % name, True)
            archv.hash()
            archv.clear_recent()
            exit()

        if archv.extracted():
            archv.hash()
            if archv.first():
                log("[Creating] %s" % name, True)
                archv.create()
            else:
                log("[Compressing] %s" % name, True)
                if not args.no_backup:
                    archv.backup()
                if args.full:
                    archv.invalidate()
                    archv.scan()
                    archv.create()
                else:
                    archv.update()
                if not args.update_only:
                    archv.delete()
        else:
            log("[Extracting] %s" % name, True)
            archv.extract()

        archv.clear_recent()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log_error("Interrupt by user.")

