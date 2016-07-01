# util.py
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

import glob
import os

def clear_recent_documents():
    print("Clearing recent documents...")
    with open(os.path.expanduser("~/.local/share/recently-used.xbel"), "w") as fh:
        pass

    print("Clearing thumbnails...")
    if os.path.isdir(os.path.expanduser("~/.thumbnails")):
        for fn in glob.glob(os.path.expanduser("~/.thumbnails/normal/*")):
            os.unlink(fn)
        for fn in glob.glob(os.path.expanduser("~/.thumbnails/large/*")):
            os.unlink(fn)
    else:
        for fn in glob.glob(os.path.expanduser("~/.cache/thumbnails/normal/*")):
            os.unlink(fn)
        for fn in glob.glob(os.path.expanduser("~/.cache/thumbnails/large/*")):
            os.unlink(fn)

