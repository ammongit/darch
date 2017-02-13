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

def get_ignored_files(path, ignore, ignoredirs):
    global errors

    try:
        with open(path, 'r') as fh:
            for line in fh.readlines():
                line = line.strip()
                if not line.startswith('#'):
                    if line.endswith(os.sep):
                        ignoredirs.add(os.path.dirname(path) + os.sep + line)
                    else:
                        ignore.add(os.path.dirname(path) + os.sep + line)
    except KeyboardInterrupt:
        exit(1)
    except SystemExit:
        exit(1)
    except:
        print("Error reading %s, skipping directory for safety." % path)
        errors += 1
        traceback.print_exc(None, err_fh)
        ignoredirs.add(path)
    finally:
        print("Got %d pattern%s from %s" % \
                (len(ignore) + len(ignoredirs), plural(len(ignore), len(ignoredirs)), path))


def confirmation(fn, config):
    if config["ask-for-confirmation"]:
        response = input("Would you like to remove \"%s\"?\n[Y/n/a/q] " % fn).lower()
        if response.startswith("a"):
            config["ask-for-confirmation"] = False
            return True
        elif response.startswith("n"):
            return False
        elif response.startswith("q"):
            print("Stopping hashing...")
            exit(1)
        else:
            return True
    else:
        return True


def plural(value):
    return "" if value == 1 else "s"


def get_hash(fn, config):
    with open(fn, "rb") as fh:
        return config["hash-algorithm"](fh.read()).hexdigest()


def process_file(fn, config):
    fn = fn.lower()

    for ext in config["ignore-extensions"]:
        if fn.endswith(".%s" % ext.lower()):
            return False

    for ext in config["extensions"]:
        if fn.endswith(".%s" % ext.lower()):
            return True

    return False


def wildcard_to_regex(pattern):
    return re.escape(pattern).replace(r"\*", r".*").replace(r"\?", r".?") + r"$"

def matches(pattern, string):
    nonpath_group = "[^%s]" % re.escape(os.path.sep)
    regex = re.escape(pattern) \
              .replace(r"\*\*", ".*") \
              .replace(r"\*", "%s*" % nonpath_group) \
              .replace(r"\?", "%s?" % nonpath_group)
    return bool(re.search(regex, string))


def dirify(directory):
    if not directory.endswith(os.path.sep):
        return directory + os.path.sep
    else:
        return directory

