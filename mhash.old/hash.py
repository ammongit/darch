# hash.py
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

def hash_media(directory, old_files_fh, err_fh, config):
    global errors
    start_time = time.time()

    changed = 0
    errors = 0
    ignoredirs = set()
    allfiles = {}

    os.chdir(directory)

    if config["dry-run"]:
        print("NOTE: This is a dry run, no files will be changed.")

    for cd, subdirs, files in os.walk(directory):
        ignorethis = False
        _dir = dirify(cd)

        for pattern in ignoredirs:
            if matches(pattern, _dir):
                print("Ignoring %s..." % _dir)
                ignorethis = True
                break

        if ignorethis:
            continue

        cd = dirify(os.path.abspath(cd))
        print("Entering \"%s\" (%d files)..." % (_dir, len(files)))

        del _dir, ignorethis

        ignore = set()

        # Added "_ignore" for Windows users, just like "_vimrc".
        for _fn in (".ignore", "_ignore"):
            if _fn in files and os.path.exists(cd + _fn):
                get_ignored_files(cd + _fn, ignore, ignoredirs)

        del _fn

        if cd + "*" in ignore:
            continue

        for fn in files:
            if not process_file(fn, config):
                continue

            abs_fn = cd + fn

            for pattern in ignore:
                if matches(pattern, abs_fn):
                    continue

            try:
                hashsum = get_hash(abs_fn)
            except KeyboardInterrupt:
                exit(1)
            except SystemExit:
                exit(1)
            except:
                print("Unable to calculate hash for \"%s\"." % fn)
                errors += 1
                traceback.print_exc(None, err_fh)
                continue

            new_fn = "%s.%s" % (hashsum, transform_file_ext(fn.split('.')[-1]))
            abs_new_fn = cd + new_fn

            if abs_fn != abs_new_fn:
                try:
                    if os.path.exists(abs_new_fn):
                        print("Found collision for \"%s\": removing \"%s\"..." % (new_fn, fn))
                        try:
                            if not DRY_RUN and confirmation(abs_fn):
                                os.remove(abs_fn)
                                old_files_fh.write("\"%s\" deleted.\n" % (abs_fn,))
                            changed += 1
                            continue
                        except KeyboardInterrupt:
                            exit(1)
                        except SystemExit:
                            exit(1)
                        except:
                            print("Unable to remove \"%s\"." % (fn,))
                            errors += 1
                            traceback.print_exc(None, err_fh)
                    else:
                        print("Renaming \"%s\" -> \"%s\"." % (abs_fn, abs_new_fn))
                        if not DRY_RUN:
                            os.rename(abs_fn, abs_new_fn)
                            old_files_fh.write("\"%s\" -> \"%s\"\n" % (abs_fn, abs_new_fn))
                        changed += 1
                except KeyboardInterrupt:
                    exit(1)
                except SystemExit:
                    exit(1)
                except:
                    print("Unable to rename \"%s\"." % fn)
                    traceback.print_exc(None, err_fh)
                    errors += 1

          # if new_fn in allfiles.viewkeys():
          #     print("Found collision for \"%s\" at \"%s\"..." % (new_fn, cd))
          #     print("(Original at \"%s\")" % (allfiles[new_fn],))
          #     try:
          #         if not DRY_RUN and confirmation(abs_new_fn):
          #             os.remove(abs_new_fn)
          #             old_files_fh.write("\"%s\" deleted\n" % (abs_fn,))
          #         changed += 1
          #         continue
          #     except:
          #         print("Unable to remove \"%s\"." % (fn,))
          #         errors += 1
          #         traceback.print_exc(None, err_fh)
          # else:
          #     allfiles[new_fn] = cd

    print("Done: %d files changed with %d errors in %.2f seconds." % (changed, errors, time.time() - start_time))

    if config["pause"]:
        raw_input("Press enter to continue: ")
        print("\r                        \r", end="")

    return errors

