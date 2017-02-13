#
# config.py
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

__all__ = [
    'default_config',
    'load_config',
    'sanity_check',
]

DEFAULT_CONFIG = {
    'encrypted': True,
    'clear-recent': True,

    'extensions': [
        'aac',
        'bmp',
        'gif',
        'jpeg',
        'jpg',
        'm4a',
        'mkv',
        'mpeg',
        'mp3',
        'mp4',
        'ogg',
        'opus',
        'png',
        'svg',
        'tif',
        'tiff',
        'webm',
        'webp',
        'wmv'
    ],

    'rename-extensions': {
        'jpeg': 'jpg',
    },

    'ignore-extensions': [
        'json',
        'pickle',
    ],

    'output-dir': '.darch',
    'archive-dir': '.',
    'hash-algorithm': 'sha1',
    'ignore-file': '.ignore',

    'write-hash-log': 'hashed.log',
    'ask-confirmation': True,
    'use-trash': False,
    'dry-run': False,
}

CONFIG_TYPES = {
    'encrypted': bool,
    'clear-recent': bool,

    'extensions': (list, str),
    'rename-extensions': (dict, None),
    'ignore-extensions': (list, str),

    'output-dir': str,
    'archive-dir': str,
    'hash-algorithm': str,
    'ignore-file': str,

    'write-hash-log': str,
    'ask-confirmation': bool,
    'use-trash': bool,
    'dry-run': bool,
}

from .log import log

import json

def default_config():
    return DEFAULT_CONFIG.copy()

def load_config(fn):
    if fn is None:
        config = default_config()
    else:
        with open(fn, 'r') as fh:
            config  = json.load(fh)
    sanity_check(config)
    return config

def sanity_check(config):
    def die(name, obj, join='for'):
        log("Error: invalid type %s '%s': %s" %
                (join, name, type(obj)), True)
        exit(1)

    for key in config.keys():
        try:
            true_type = CONFIG_TYPES[key]
        except KeyError:
            log("Warning: config option ignored: %s" % key, True)
            continue

        item = config[key]
        if type(true_type) is tuple:
            if type(item) != true_type[0]:
                die(key, item)
            if true_type[1]:
                for val in item:
                    if type(val) != true_type[1]:
                        die(val, item, 'in')
        else:
            if type(item) != true_type:
                die(key, item)
    for key in CONFIG_TYPES.keys():
        if key not in config:
            log("Error: key '%s' not in config" % key)
            exit(1)

