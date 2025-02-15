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
        console,
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
        # Console instance from CLI
        cls.console = console

        # Create directories
        dirs_created = cls.create_dirs(paths["directories"])

        # Create Files
        files_created = cls.create_files(
            paths["files"],
            skip=skip,
            overwrite=overwrite,
        )

        return (dirs_created, files_created)

    @classmethod
    def create_dirs(cls, dirs: List[str]) -> int:
        """Create files with names found in `files`.
        Returns the number of dirs created."""
        count = 0
        for path in dirs:
            try:
                os.mkdir(path)  # Create the directory
                count += 1
                cls.console.print("[D] Creating '%s'" % path, "light_green")

            except FileExistsError:
                cls.console.print(
                    "[D] Skipping '%s', already exists" % path,
                    "light_yellow",
                )
        return count

    @classmethod
    def create_files(
        cls,
        files: List[str],
        skip: bool = False,
        overwrite: bool = False,
    ) -> int:
        """Create files with names found in `files`. Returns the number of files created."""
        count = 0
        for path in files:
            try:
                # Create file
                with open(path, "x") as _:
                    cls.console.print("[f] Creating '%s'" % path, "light_green")

                count += 1
            except FileExistsError:
                # Skip file
                if skip:
                    cls.console.print(
                        "[F] Skipping '%s', already exists" % path,
                        "light_yellow",
                    )
                    continue

                # Overwrite file
                if overwrite:
                    count += 1
                    cls.console.print("[F] Overwriting '%s'" % path, "light_blue")
                    with open(path, "w") as _:
                        continue

        return count
