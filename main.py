#!/usr/bin/env python

import darch
import ft_diff
import mhash
import os
import sys

if __name__ == "__main__":
    program_name = os.path.basename(sys.argv[0])

    if program_name == "ft_diff":
        ft_diff.main()
    elif program_name == "mhash":
        mhash.main()
    else:
        darch.main()

