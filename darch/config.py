#
# config.py
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
    'Config',
]

import hashlib

import yaml

from .log import log, log_error, log_warn

def _check(obj, name, ftype):
    try:
        field = getattr(obj, name)
    except AttributeError:
        log_error("No such field in config file: {}".format(name))
        exit(1)

    if not isinstance(field, ftype):
        log_error("The field '{}' is of type {!r}, needs {!r}".format(name, type(field), ftype))
        exit(1)

    return field

class Config:
    __slots__ = (
        'compression',
        'backup',
        'encrypted',
        'hash',
        'test_archive',
        'clear_recent',
        'extensions',
        'rename_extensions',
        'skip_extensions',
        'ignore_files',
        'archive_dir',
        'hasher',
        'data_dir',
        'tree_file',
        'logs',
        'use_trash',
        'ask_confirmation',
        'always_yes',
        'dry_run',
    )

    @classmethod
    def load(cls, fh):
        return Config(yaml.safe_load(fh))

    def __init__(self, obj):
        self.compression = Config.Compression(obj['compression'])
        self.backup = _check(obj, 'backup', bool)
        self.encrypted = _check(obj, 'encrypted', bool)
        self.hash = _check(obj, 'hash', bool)
        self.test_archive = _check(obj, 'test-archive', bool)
        self.clear_recent = _check(obj, 'clear-recent', bool)
        self.extensions = _check(obj, 'extensions', list)
        self.rename_extensions = _check(obj, 'rename-extensions', dict)
        self.skip_extensions = _check(obj, 'skin-extensions', list)
        self.ignore_files = _check(obj, 'ignore-files', list)
        self.archive_dir = _check(obj, 'archive-dir', str)
        hash_algo = _check(obj, 'hash-algorithm', str)
        self.data_dir = _check(obj, 'data-dir', str)
        self.tree_file = _check(obj, 'tree-file', str)
        self.logging = Config.Logging(obj['logging'])
        self.use_trash = _check(obj, 'use-trash', bool)
        self.ask_confirmation = _check(obj, 'ask-confirmation', bool)
        self.always_yes = _check(obj, 'always-yes', bool)
        self.dry_run = _check(obj, 'dry-run', bool)

        try:
            self.hasher = getattr(hashlib, hash_algo)
        except AttributeError:
            log_error("No such hash algorithm: {}".format(hash_algo))
            exit(1)

    class Compression:
        __slots__ = (
            'level',
            'format',
            'extension',
        )

        def __init__(self, obj):
            self.level = _check(obj, 'level', int)
            self.format = _check(obj, 'format', str)
            self.extension = _check(obj, 'extension', str)

            if self.level <= 0:
                log_error("Invalid compression level: {}".format(self.level))
                exit(1)

    class Logging:
        __slots__ = (
            'duplicates',
            'hashing',
        )

        def __init__(self, obj):
            duplicates_fn = _check(obj, 'duplicates', str)
            hashing_fn = _check(obj, 'hashing', str)

            self.duplicates = open(duplicates_fn, 'w')
            self.hashing = open(hasing_fn, 'w')

        def __del__(self):
            self.duplicates.close()
            self.hashing.close()
