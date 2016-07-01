## darch
Difference Archiver

### Synopsis
A tool that creates encrypted archives that saves on compression time by only updating altered files.

This program also includes two other Python tools:  
`mhash`, short for "media hash" is a program which recursively removes media files (e.g. images, videos, etc.) that are exact duplicates by renaming them to a hash of their contents. This is useful for, say, your wallpaper collection since it provides a consistent naming scheme and prevents inclusion of duplicate pictures.

`ft_diff`, short for "file tree difference", allows the user to determine the difference between a file tree and its former self, as recorded in a `filetree.pickle` file.

### Requirements
This program is written for Python 3.4 or later.

### Installation
(todo)

### Usage
To create/update an archive, use:
```
./darch.py [archive-name]
```

To use `mhash` by itself, use:
```
./mhash.py [directory]...
```

### Configuration
Each archive can have its own configuration file by placing an appropriately-formatted `darch.json` in the root directory.

There is also a per-user configuration that contains information beyond what the local config file provides. It is located in
`$XDG_CONFIG_HOME/darch.conf`, or `~/.config/darch.conf` if there is no `$XDG_CONFIG_HOME` environmental variable.

#### Ignoring files
`mhash` renames files, which destroys the original filename. Sometimes this is not a desirable behavior. For instance, a comic strip may number pages using the filename.
By creating a file called `.ignore` in a directory, you can specify which files and directories to pass over and not change.

#### Undoing renaming
If you accidentally run `mhash` on the wrong directory, the filename information of many files can be lost, and is potentially a big headache to reverse. By default, `mhash`
produces a log of all changed files in `hash-renamed-files.log` in the directory it was called on. By using `mhash --undo`, these changes can be done as long as the `hash-renamed-files.log`
file is present.  
_This operation cannot undo file deletion._

### License
This program is licensed under the GPL version 2 or later. See `LICENSE` for more details.

