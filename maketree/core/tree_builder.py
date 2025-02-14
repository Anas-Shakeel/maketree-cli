""" Contains logic for creating the directory structure on the file system,
based on the parsed data from the structure file. """

import os
from maketree.utils import _print
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
        no_color: bool = False,
    ) -> Tuple[int, int]:
        """
        ### Build
        Create the directories and files on the filesystem.

        #### Args:
        - `paths`: the paths dictionary
        - `skip`: skips existing files
        - `overwrite`: overwrites existing files
        - `verbose`: print messages while creating dirs/files
        - `no_color`: print messages without colors

        Returns a `tuple[int, int]` containing the number of
        dirs and files created, in that order.
        """
        # Create directories
        dirs_created = cls.create_dirs(
            paths["directories"], verbose=verbose, no_color=no_color
        )

        # Create Files
        files_created = cls.create_files(
            paths["files"],
            skip=skip,
            overwrite=overwrite,
            verbose=verbose,
            no_color=no_color,
        )

        return (dirs_created, files_created)

    @classmethod
    def create_dirs(
        cls,
        dirs: List[str],
        verbose: bool = False,
        no_color: bool = False,
    ) -> int:
        """Create files with names found in `files`. Returns the number of dirs created."""
        count = 0
        for path in dirs:
            try:
                os.mkdir(path)  # Create the directory
                count += 1
                _print("[D] Creating '%s'" % path, verbose, no_color, "light_green")

            except FileExistsError:
                _print(
                    "[D] Skipping '%s', already exists" % path,
                    verbose,
                    no_color,
                    "light_yellow",
                )
        return count

    @classmethod
    def create_files(
        cls,
        files: List[str],
        skip: bool = False,
        overwrite: bool = False,
        verbose: bool = False,
        no_color: bool = False,
    ) -> int:
        """Create files with names found in `files`. Returns the number of files created."""
        count = 0
        for path in files:
            try:
                # Create file
                with open(path, "x") as _:
                    _print("[f] Creating '%s'" % path, verbose, no_color, "light_green")

                count += 1
            except FileExistsError:
                # Skip file
                if skip:
                    _print(
                        "[F] Skipping '%s', already exists" % path,
                        verbose,
                        no_color,
                        "light_yellow",
                    )
                    continue

                # Overwrite file
                if overwrite:
                    count += 1
                    _print(
                        "[F] Overwriting '%s'" % path, verbose, no_color, "light_blue"
                    )
                    with open(path, "w") as _:
                        continue

        return count
