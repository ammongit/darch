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

from .archive import Archive
from .config import Config
from .log import log, log_error

from getpass import getpass
import argparse
import os
import sys

def config_path():
    try:
        config_home = os.environ['XDG_CONFIG_HOME']
    except KeyError:
        config_home = os.path.expanduser('~/.config')

    path = os.path.join(config_home, 'darch.yaml')
    if not os.path.exists:
        log_error("Cannot find default darch config {}".format(path))
        exit(1)

    return path

def _override_cfg(config, args, attr):
    value = getattr(args, attr)
    if value  is not None:
        setattr(args, attr, value)

def print_operation(archv, args, name):
    if archv.dir_exists():
        if args.hash_only:
            operation = 'Hashing'
        elif args.full:
            operation = 'Recreating'
        elif archv.tar_exists():
            operation = 'Creating'
        else:
            operation = 'Updating'
    else:
        if archv.tar_exists():
            operation = 'Extracting'
        else:
            print("No archive at that location!")
            exit(1)

    log("[{}] {}".format(operation, name), True)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Manage a hashed media archive.")

    parser.add_argument('-c', '--config',
            help="Specify the configuration file.")
    parser.add_argument('-d', '--directory',
            help="Switch to this directory before running anything.")
    parser.add_argument('-n', '--dry-run',
            dest='dry_run', action='store_true', default=None,
            help="Don't actually do anything, just print the results.")
    parser.add_argument('-u', '--update-only',
            dest='update_only', action='store_true',
            help="Update the archive only, leaving the files extracted.")
    parser.add_argument('-m', '--hash-only',
            dest='hash_only', action='store_true',
            help="Only run the media hash. Do not affect the archive. Ignores any -u options set.")
    parser.add_argument('-t', '--test',
            dest='test_archive', action='store_true', default=None,
            help="Test the archive after modifying it.")
    parser.add_argument('-P', '--purge-logs',
            dest='purge_logs', action='store_true',
            help="Purge the archive's logs before doing anything.")
    parser.add_argument('-F', '--full',
            action='store_true',
            help="Recreate the full archive. Doesn't use the difference algorithm.")
    parser.add_argument('-b', '--no-backup',
            action='store_false', default=None,
            help="Back up the archive before modifying it.")
    parser.add_argument('-y', '--always-yes',
            dest='always_yes', action='store_true', default=None,
            help="Automatically answer 'yes' to every question prompt.")
    parser.add_argument('archive-dir', nargs='+',
            dest='archives',
            help="The archives you wish to operate on.")
    args = parser.parse_args()
    config = Config.load(args.config or config_path())

    # Override config options from args
    for attr in ('dry_run', 'always_yes', 'test_archive', 'backup'):
        _override_cfg(config, args, attr)

    if args.directory is not None:
        os.chdir(args.directory)

    # Operate on each of the passed archives
    for archive in args.archives:
        name = os.path.basename(archive)
        archv = Archive(archive, config)

        print_operation(archv, args, name)

        if archv.dir_exists():
            archv.open_meta()
            archv.build_tree()

            if args.purge:
                archv.purge_logs()

            if args.hash_only:
                archv.hash()
                if config.clear_recent:
                    archv.clear_recent()
                continue

            create = not archv.tar_exists() or args.full
            passwd = getpass("Password: ")
            if create:
                passwd2 = getpass("Confirm: ")
                if passwd != passwd2:
                    print("Passwords do not match!")
                    exit(1)

            if config.hash:
                archv.hash()

            if config.backup:
                archv.backup()

            if create:
                archv.tar_delete()
                archv.tar_create(passwd)
            else:
                archv.tar_update(passwd)

            if not args.update_only:
                archv.dir_delete()
        elif archv.tar_exists():
            passwd = getpass("Password: ")
            archv.tar_extract(passwd)

    archv.clear_recent()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        log_error("Interrupt by user.")

