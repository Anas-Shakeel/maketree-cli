""" Contains logic for creating the directory structure on the file system,
based on the parsed data from the structure file. """

import os
from typing import List, Dict


class TreeBuilder:
    """Build the tree parsed from `.tree` file"""

    @classmethod
    def build(cls, tree: List[Dict]):
        """Create the directories and files on the filesystem."""
        ...

    @classmethod
    def create_file(cls, filename: str):
        """Create a file with `filename` name."""
        ...
