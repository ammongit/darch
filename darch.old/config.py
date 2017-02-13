# config.py
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

import json


def sanity_test_config(config):
    success = True

    if "archive-directory" not in config.keys():
        print("Key \"archive-directory\" not specified in config file.", file=sys.stderr)
        success = False
    elif not os.path.isdir(os.path.expanduser(config["archive-directory"])):
        print("Specified archive directory does not exist: %s" % config["archive-directory"], file=sys.stderr)
        success = False

    if "lock-file" not in config.keys():
        print("Key \"lock-file\" not found, using default.", file=sys.stderr)
        config["lock-file"] = ".%s.lock"

    if "hash-script" not in config.keys():
        print("Key \"hash-script\" not specified in config file.", file=sys.stderr)
        success = False

    if "back-up-old-archive" not in config.keys() or type(config["back-up-old-archive"]) != bool:
        print("Key \"back-up-old-archive\" not found or invalid, backing up archive anyways.", file=sys.stderr)
        config["back-up-old-archive"] = True

    if "clear-recent" not in config.keys() or type(config["clear-recent"]) != bool:
        print("Key \"clear-recent\" not found or invalid, not clearing recent files.", file=sys.stderr)
        config["clear-recent"] = False

    if "test-archive" not in config.keys() or type(config["test-archive"]) != bool:
        print("Key \"test-archive\" not found or invalid, not testing archive.", file=sys.stderr)
        config["test-archive"] = True

    config["archive-directory"] = os.path.expanduser(config["archive-directory"])
    config["hash-script"] = os.path.expanduser(config["hash-script"])
    config["archive-file"] = os.path.join(config["archive-directory"], name + ".7z")

    return success

