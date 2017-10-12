#
# meta.py
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

__all__ = [
    'Meta',
]

import json

HASHED_FILE = 'hashed.json'

class Meta:
    __slots__ = (
        'dir_path',
        'hashed_path',
        'fsops',
        '_hashed',
    )

    def __init__(self, dir_path, fsops):
        self.dir_path = dir_path
        self.hashed_path = os.path.join(self.dir_path, HASHED_FILE)
        self.fsops = fsops
        self._hashed = None

        # Initialization
        if not os.path.isdir(path):
            self.fsops.mkdir(dir_path)

        if os.path.exists(self.hashed_path):
            self.get_hashed()
        else:
            self.set_hashed({})

    def get_hashed(self):
        with self.fops.open(self.hashed_path, 'r') as fh:
            self._hashed = json.load(fh)

        return self._hashed

    def set_hashed(self, obj):
        self._hashed = obj
        with self.fops.open(self.hashed_path, 'w') as fh:
            json.dump(obj, fh)

    hashed = property(get_hashed, set_hashed, None)
