## darch
Difference Archiver

### Synopsis
A tool that creates media archives that saves on compression time by only updating altered files. It hashes filenames by renaming them to their equivalent hash sum to remove duplicates, and loads/stores the result in a 7z archive.

### Requirements
This program is written for Python 3.4 or later.

Optionally requires send2trash. If the module is available this program can trash duplicate files instead of deleting them.

### Usage
To create, extract or update an archive, use:
```
python -m darch [flags] archive-name...
```

There are a number of options available. Here are a couple that may be of interest:
```
| Flag | Description                                       |
|------|---------------------------------------------------|
| `-u` | Update the archive only, leaving files on disk.   |
| `-m` | Perform media hash only, no archive manipulation. |
| `-n` | Dry run. No changes are made on the filesystem.   |
| `-F` | Full run. Recreate the archive from scratch.      |
```

### Configuration
Each archive can have its own configuration file by placing an appropriately-formatted `darch.json` in the root directory.

There is also a per-user configuration that contains information beyond what the local config file provides. It is located in `$XDG_CONFIG_HOME/darch.json`, or `~/.config/darch.json` if there is no `$XDG_CONFIG_HOME` environmental variable.

#### Ignoring files
Since files are renamed, the original filename is destroyed. Sometimes this is not desirable behavior. For instance, a comic strip folder would have images inside in a specific order based on the filename.
By creating a file called `.ignore` in a directory, you can specify which files and directories to pass over and not change.

#### Undoing renaming
If you accidentally run the media hasher on the wrong directory, the filename information of many files can be lost, which may be a big headache to reverse. So by default, all changed files are logged in `.darch/hashed.log` so you could renamed them back if necessary.

### License
This program is licensed under the GPL version 2 or later. See `LICENSE` for more details.

