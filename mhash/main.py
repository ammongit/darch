# main.py
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

import argparse


def main():
    # Parse options with argparse
    argparser = argparse.ArgumentParser(description=DESCRIPTION)
    argparser.add_argument("-c", "--config", nargs="?", help=HELP_CONFIG_FILE)
    argparser.add_argument("-n", "--dry-run", default=None, action="store_true", help=HELP_DRY_RUN)
    argparser.add_argument("-y", "--no-confirm", default=None, action="store_true", help=HELP_NO_CONFIRM)
    argparser.add_argument("-a", "--ignore-extensions", default=None, action="store_true", help=HELP_IGNORE_EXTENSIONS)
    argparser.add_argument("-t", "--use-trash", default=None, action="store_true", help=HELP_USE_TRASH)
    argparser.add_argument("-H", "--hash-algorithm", nargs="?", help=HELP_HASH_ALGORITHM)
    argparser.add_argument("-P", "--pause", default=None, action="store_true", help=HELP_PAUSE)
    argparser.add_argument("directory", nargs="+", help=HELP_DIRECTORY)
    args = argparser.parse_args()

    errors = 0
    configs = {}
    for directory in args.directory:
        if not os.path.isdir(directory):
            print("No such directory: \"%s\"." % directory)
            exit(1)

        configs[directory] = get_configuration(args, directory)

    with open(os.path.join(os.path.dirname(sys.argv[0]), "hash-errors.log"), "a+") as err_fh:
        for directory, config in configs.items():
            with open("%s/hash-renamed-files.log" % directory, "a+") as old_files_fh:
                errors += hash_media(directory, old_files_fh, err_fh, config)

