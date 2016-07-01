# archive.py
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

import shutil
import subprocess

def add_files(name, archive_dir, created, config, passwd, icon="+"):
    created_list = []

    for fn in created:
        print("%s %s" % (icon, fn))
        created_list.append(os.path.join(name, os.path.basename(fn)))

    if not created_list:
        print("Warn: list of files to add is empty")
        return

    arguments = ["7z", "a", "-t7z", "-p%s" % passwd, "-mhe=on", "-mx=9", "-m0=lzma", config["archive-file"]]
    subprocess.Popen(arguments + created_list, stdout=subprocess.DEVNULL)
    print("Command: %s" % (arguments + created_list))


def remove_files(name, archive_dir, removed, config, passwd):
    removed_list = []

    for fn in removed:
        print("- %s" % fn)
        removed_list.append(os.path.join(name, os.path.basename(fn)))

    if not removed_list:
        print("Warn: list of files to remove is empty")
        return

    arguments = ["7z", "d", "-t7z", "-p%s" % passwd, "-mhe=on", "-mx=9", "-m0=lzma", config["archive-file"]]
    subprocess.Popen(arguments + removed_list, stdout=subprocess.DEVNULL)
    print("Command: %s" % (arguments + removed_list))


def create_archive(name, archive_dir, config, passwd):
    print("[New archive]")
    while True:
        passwd = getpass("Password: ")
        passwd2 = getpass("Password again: ")

        if passwd != passwd2:
            print("Passwords do not match.")
        else:
            break

    print("Hashing images...")
    subprocess.run([config["hash-script"], archive_dir])
    print("Adding files...")
    subprocess.run(["7z", "a", "-t7z", "-p%s" % passwd, "-mhe=on", "-mx=9", "-m0=lzma", config["archive-file"], archive_dir])
    print("Removing old files...")
    #shutil.rmtree(archive_dir)
    if config["clear-recent"]:
        clear_recent_documents()


def compress_archive(name, archive_dir, config):
    print("[Compressing]")
    passwd = getpass("Password: ")
    print("Hashing images...")
    subprocess.run([config["hash-script"], archive_dir])
    print("Checking file diff...")
    created, removed, changed, ignored = ft_diff.get_changed_files(archive_dir)
    print("Backing up old archive...")
    shutil.copy2(config["archive-file"], config["archive-file"] + "~")
    if created:
        print("Adding new files...")
        add_files(name, archive_dir, created, config, passwd)
    if removed:
        print("Removing deleted files...")
        remove_files(name, archive_dir, removed, config, passwd)
    if changed:
        print("Changing modified files...")
        add_files(name, archive_dir, changed, config, passwd, icon="~")
    print("Adding untracked files...")
    add_files(name, archive_dir, ignored, config, passwd, icon=">")
    if not (created or removed or changed):
        print("Note: no changes to archive.")
    if config["test-archive"]:
        print("Testing archive...")
        subprocess.run(["7z", "t", "-p%s" % passwd, config["archive-file"]])
    print("Removing old files...")
    #shutil.rmtree(archive_dir)
    if config["clear-recent"]:
        clear_recent_documents()


def extract_archive(name, archive_dir, config):
    print("[Extracting]")
    passwd = getpass("Password: ")
    subprocess.run(["7z", "x", "-p%s" % passwd, config["archive-file"]])

