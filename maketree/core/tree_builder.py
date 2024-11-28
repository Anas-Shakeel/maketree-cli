""" Contains logic for creating the directory structure on the file system,
based on the parsed data from the structure file. """

import os
from os.path import exists
from typing import List, Dict


class TreeBuilder:
    """Build the tree parsed from `.tree` file"""

    @classmethod
    def build(cls, paths: Dict[str, List[str]], skip: bool = False):
        """
        ### Build
        Create the directories and files on the filesystem.

        #### Args:
        - `paths`: the paths dictionary
        - `skip`: skips existing files
        """
        cls.create_dirs(paths["directories"])
        cls.create_files(paths["files"], skip=skip)

    @classmethod
    def create_dirs(cls, dirs: List[str]):
        """Create files with names found in `files`."""
        for path in dirs:
            try:
                # Create the directory
                os.mkdir(path)
            except FileExistsError:
                pass

    @classmethod
    def create_files(cls, files: List[str], skip: bool = False):
        """Create files with names found in `files`."""
        for path in files:
            if skip and exists(path):
                continue

            # Create the file
            with open(path, "w") as _:
                pass  # Empty file
