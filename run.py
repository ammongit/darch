#!/usr/bin/env python3
# run.py
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

import darch
import ft_diff
import mhash
import os
import sys

MODULE_DICT = {
    "--darch": darch,
    "--ftdiff": ft_diff,
    "--mhash": mhash,
}

if __name__ == "__main__":
    module = None
    for i in range(1, len(sys.argv)):
        module = MODULE_DICT.get(sys.argv[i], None)

        if module:
            sys.argv.pop(i)
            module.main()

    if module is None:
        program_name = os.path.basename(sys.argv[0])

        if program_name == "ftdiff":
            ft_diff.main()
        elif program_name == "mhash":
            mhash.main()
        else:
            darch.main()

