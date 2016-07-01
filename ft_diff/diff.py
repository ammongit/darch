# diff.py
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

import itertools


def compare_file_trees(old_tree, new_tree, ignored):
    created_files = set()
    removed_files = set()
    changed_files = set()

    for fn in set(itertools.chain(old_tree.keys(), new_tree.keys())):
        if fn in ignored:
            continue

        was_present = fn in old_tree.keys()
        is_present = fn in new_tree.keys()

        if not was_present and is_present:
            created_files.add(fn)
        elif was_present and not is_present:
            removed_files.add(fn)
        elif old_tree[fn] != new_tree[fn]:
            changed_files.add(fn)

    return created_files, removed_files, changed_files, ignored


def get_changed_files(directory,
        tree_storage_file=FILE_TREE_FILE,
        tree_ignore_file=FILE_TREE_IGNORE_FILE):

    if os.path.exists(tree_ignore_file):
        ignore = []
        try:
            with open(tree_ignore_file, "r") as fh:
                line = fh.readline()

                while line:
                    ignore.append(line.rstrip())
                    line = fh.readline()
        except:
            print("Unable to read ignore file \"%s\"." % tree_ignore_file)
            exit(1)
    else:
        ignore = DEFAULT_IGNORE_TARGETS
        try:
            with open(tree_ignore_file, "w") as fh:
                for ignore_file in DEFAULT_IGNORE_TARGETS:
                    fh.write(ignore_file)
                    fh.write("\n")
        except:
            print("Unable to write to ignore file \"%s\"." % tree_ignore_file)

    filetree = get_file_tree(directory, ignore)

    if os.path.exists(tree_storage_file):
        try:
            with open(tree_storage_file, "rb") as fh:
                oldfiletree = pickle.load(fh)
        except:
            print("Unable to read old directory tree in \"%s\"." % tree_storage_file)
            oldfiletree = {}
    else:
        oldfiletree = {}

    return compare_file_trees(oldfiletree, filetree, ignore)


