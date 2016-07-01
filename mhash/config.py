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

def get_configuration(args, path):
    if args.config:
        path = args.config
    else:
        path = os.path.join(path, "config.json")

    if os.path.exists(path):
        config = json.load(path)
    else:
        config = DEFAULT_CONFIG

    if args.dry_run is not None:
        config["dry-run"] = args.dry_run
    if args.no_confirm is not None:
        config["ask-confirmation"] = not args.no_confirm
    if args.use_trash is not None:
        config["use-trash"] = args.use_trash
    if args.hash_algorithm is not None:
        config["hash-algorithm"] = getattr(hashlib, args.hash_algorithm.lower())
    if args.pause is not None:
        config["pause"] = args.pause

    return config
