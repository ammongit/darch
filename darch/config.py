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
    'default_config',
    'load_config',
    'sanity_check',
]

DEFAULT_CONFIG = {
    'compression': {
        'level': 5,
        'format': '7z',
        'extension': '7z',
    },
    'encrypted': True,
    'test-archive': False,
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
        'wmv',
    ],

    'rename-extensions': {
        'jpeg': 'jpg',
    },

    'ignore-extensions': [
        'json',
        'pickle',
    ],

    'archive-dir': '.',
    'hash-algorithm': 'sha224',
    'ignore-file': '.ignore',

    'data-dir': '.darch',
    'tree-file': 'tree.pickle',
    'duplicates-log': 'duplicates.txt',
    'hash-log': 'hashed.log',
    'ask-confirmation': True,
    'use-trash': False,

    'always-yes': False,
    'dry-run': False,
}

CONFIG_TYPES = {
    'compression': (dict, {
        'level': int,
        'format': str,
        'extension': str,
    }),
    'encrypted': bool,
    'test-archive': bool,
    'clear-recent': bool,

    'extensions': (list, str),
    'rename-extensions': (dict, None),
    'ignore-extensions': (list, str),

    'archive-dir': str,
    'hash-algorithm': str,
    'ignore-file': str,

    'data-dir': str,
    'tree-file': str,
    'duplicates-log': str,
    'hash-log': str,
    'ask-confirmation': bool,
    'use-trash': bool,

    'always-yes': bool,
    'dry-run': bool,
}

from .log import log, log_error, log_warn

import json

def default_config():
    return DEFAULT_CONFIG.copy()

def load_config(fn):
    with open(fn, 'r') as fh:
        config  = json.load(fh)
    sanity_check(config)
    for key, val in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = val
    return config

def _die(name, obj, join='for'):
    log_error("invalid type %s '%s': %s" %
            (join, name, obj), True)

def _check_dict(real, expected, name):
    for key in expected.keys():
        if key not in real:
            log_error("option '%s' in '%s' not defined" % (key, name))

    for key, val in real.items():
        if key not in expected.keys():
            log_warn("option '%s' in '%s' ignored" % (key, name))
        if type(val) != expected[key]:
            _die(key, expected[key], 'in')

def _check_list(real, expected):
    for it in real:
        if type(it) != expected:
            _die(it, expected, 'in')

def sanity_check(config):
    for key in config.keys():
        try:
            true_type = CONFIG_TYPES[key]
        except KeyError:
            log_warn("config option ignored: %s" % key, True)
            continue

        item = config[key]
        if type(true_type) is tuple:
            if type(item) != true_type[0]:
                _die(key, type(item))
            if true_type[1]:
                if true_type[0] == dict:
                    _check_dict(item, true_type[1], key)
                else:
                    _check_list(item, true_type[1])
        else:
            if type(item) != true_type:
                _die(key, type(item))
    for key in CONFIG_TYPES.keys():
        if key not in config:
            log_error("key '%s' not in config" % key)

