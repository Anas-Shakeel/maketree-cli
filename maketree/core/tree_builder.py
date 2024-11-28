""" Contains logic for creating the directory structure on the file system,
based on the parsed data from the structure file. """

import os
from os.path import exists
from typing import List, Dict, Tuple


class TreeBuilder:
    """Build the tree parsed from `.tree` file"""

    @classmethod
    def build(cls, paths: Dict[str, List[str]], skip: bool = False) -> Tuple[int, int]:
        """
        ### Build
        Create the directories and files on the filesystem.

        #### Args:
        - `paths`: the paths dictionary
        - `skip`: skips existing files

        Returns a `tuple[int, int]` containing the number of
        dirs and files created, in that order.
        """
        dirs_created = cls.create_dirs(paths["directories"])
        files_created = cls.create_files(paths["files"], skip=skip)

        return (dirs_created, files_created)

    @classmethod
    def create_dirs(cls, dirs: List[str]) -> int:
        """Create files with names found in `files`. Returns the number of dirs created."""
        count = 0
        for path in dirs:
            try:
                # Create the directory
                os.mkdir(path)
                count += 1
            except FileExistsError:
                pass
        return count

    @classmethod
    def create_files(cls, files: List[str], skip: bool = False) -> int:
        """Create files with names found in `files`. Returns the number of files created."""
        count = 0
        for path in files:
            if skip and exists(path):
                continue

            # Create the file
            with open(path, "w") as _:
                pass  # Empty file
            count += 1

        return count
