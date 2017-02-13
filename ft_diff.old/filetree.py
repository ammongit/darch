# filetree.py
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

import codecs
import glob
import os
import pickle


def get_file_tree(directory, ignore):
    ignored = set()
    for ignore_file in ignore:
        ignored = ignored.union(glob.glob(os.path.join(directory, ignore_file), recursive=True))

    filetree = {}
    for root, dirs, files in os.walk(directory, followlinks=True):
        for fn in files:
            path = os.path.join(root, fn)
            if path in ignored:
                continue

            try:
                with open(path, "rb") as fh:
                    hashsum = hashlib.md5(codecs.encode(fh.read(), "hex_codec")).digest()
                filetree[path] = hashsum
            except IOError as err:
                print("Unable to get checksum of \"%s\": %s." % (fn, err))

    return filetree

def update_file_tree(directory, filetree):
    with open(tree_storage_file, "wb") as fh:
        pickle.dump(filetree, fh)
