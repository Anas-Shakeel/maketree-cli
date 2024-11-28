""" Contains logic for creating the directory structure on the file system,
based on the parsed data from the structure file. """

import os
from typing import List, Dict


class TreeBuilder:
    """Build the tree parsed from `.tree` file"""

    @classmethod
    def build(cls, paths: Dict[str, List[str]]):
        """Create the directories and files on the filesystem."""
        cls.create_dirs(paths["directories"])
        cls.create_files(paths["files"])

    @classmethod
    def create_dirs(cls, dirs: List[str]):
        """Create files with names found in `files`."""
        for path in dirs:
            # Create the directory
            os.mkdir(path)

    @classmethod
    def create_files(cls, files: List[str]):
        """Create files with names found in `files`."""
        for path in files:
            # Create the file
            with open(path, "x") as _:
                pass  # Empty file
