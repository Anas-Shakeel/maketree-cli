""" Contains logic for creating the directory structure on the file system,
based on the parsed data from the structure file. """

import os
from os.path import exists
from maketree.utils import print_on_true
from typing import List, Dict, Tuple


class TreeBuilder:
    """Build the tree parsed from `.tree` file"""

    @classmethod
    def build(
        cls,
        paths: Dict[str, List[str]],
        skip: bool = False,
        overwrite: bool = False,
        verbose: bool = False,
    ) -> Tuple[int, int]:
        """
        ### Build
        Create the directories and files on the filesystem.

        #### Args:
        - `paths`: the paths dictionary
        - `skip`: skips existing files
        - `overwrite`: overwrites existing files
        - `verbose`: print messages while creating dirs/files

        Returns a `tuple[int, int]` containing the number of
        dirs and files created, in that order.
        """
        dirs_created = cls.create_dirs(paths["directories"], verbose=verbose)
        files_created = cls.create_files(
            paths["files"], skip=skip, overwrite=overwrite, verbose=verbose
        )

        return (dirs_created, files_created)

    @classmethod
    def create_dirs(cls, dirs: List[str], verbose: bool = False) -> int:
        """Create files with names found in `files`. Returns the number of dirs created."""
        count = 0
        for path in dirs:
            try:
                # Create the directory
                os.mkdir(path)
                count += 1

                print_on_true("Created directory '%s'" % path, verbose)
            except FileExistsError:
                print_on_true("Skipped directory '%s', already exists" % path, verbose)
                pass
        return count

    @classmethod
    def create_files(
        cls,
        files: List[str],
        skip: bool = False,
        overwrite: bool = False,
        verbose: bool = False,
    ) -> int:
        """Create files with names found in `files`. Returns the number of files created."""
        count = 0
        for path in files:
            if skip and exists(path):
                print_on_true("Skipped file '%s', already exists" % path, verbose)
                continue

            count += 1

            # Overwrite file
            if overwrite:
                print_on_true("Overwriting file '%s'" % path, verbose)
                with open(path, "w") as _:
                    pass  # Empty file
                continue

            # Create file
            print_on_true("Created file '%s'" % path, verbose)
            with open(path, "x") as _:
                pass  # Empty file

        return count
