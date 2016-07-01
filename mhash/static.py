# static.py
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

DESCRIPTION = "A program that recursively removes media files that are exact duplicates (images, videos, etc.) by renaming them to a hash of their contents."
HELP_CONFIG_FILE = "Do not read the local configuration file but instead use this one."
HELP_DRY_RUN = "Do not make any changes on the filesystem, just print what would have changed."
HELP_NO_CONFIRM = "Do not prompt to make changes, just do them."
HELP_IGNORE_EXTENSIONS = "Operate on all files found regardless of file type."
HELP_USE_TRASH = "Instead of deleting files, put them in the trash instead."
HELP_HASH_ALGORITHM = "The hash algorithm to use. The default is SHA1."
HELP_PAUSE = "Pause after each directory specified is fully hashed."
HELP_DIRECTORY = "Operate on the following directory or directories."

DEFAULT_CONFIG = {
    "extensions": [
        "bmp",
        "gif",
        "jpeg",
        "jpg",
        "m4a",
        "mkv",
        "mp3",
        "mp4",
        "ogg",
        "png",
        "svg",
        "tif",
        "tiff",
        "webm",
        "webp",
        "wmv"
    ],

    "rename-extensions": {
        "jpeg": "jpg"
    },

    "ignore-extensions": [
        "json"
    ],

    "hash-algorithm": "sha1",

    "run-on-all-files": False,
    "ask-confirmation": True,
    "use-trash": False,
    "delete-in-other-dirs": True,
    "pause": False,
    "dry-run": False
}


