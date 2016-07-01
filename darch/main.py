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

import atexit
import signal


def handle_signal(signum, frame):
    clean_up(1)


def clean_up():
    if lock_file:
        os.unlink(lock_file)

def main():
    global lock_file
    lock_file = None

    atexit.register(clean_up)

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGHUP, handle_signal)

    if len(sys.argv) < 2:
        name = input("Which archive would you like to access? ")
    else:
        name = sys.argv[1]

    if len(sys.argv) < 3:
        config_file = "/usr/local/scripts/dat/varch.json"
    else:
        config_file = sys.argv[2]

    with open(config_file, "r") as fh:
        config = json.load(fh)

    if not sanity_test_config(config):
        exit(1)

    lock_file = os.path.join(config["archive-directory"], config["lock-file"] % name)

    if os.path.exists(lock_file):
        print("This archive is being processed by another process.")
        lock_file = None
        exit(1)

    with open(lock_file, "w") as fh:
        pass

    archive_extracted_dir = os.path.join(config["archive-directory"], name)

    if os.path.isdir(archive_extracted_dir):
        if not os.path.isfile(config["archive-file"]):
            create_archive(name, archive_extracted_dir, config)
        else:
            compress_archive(name, archive_extracted_dir, config)
    elif not os.path.isfile(config["archive-file"]):
        print("[Error]")
        print("Cannot find archive at \"%s\".", config["archive_file"])
        exit(1)
    else:
        extract_archive(name, archive_extracted_dir, config)

