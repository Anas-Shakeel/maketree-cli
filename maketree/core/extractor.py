"""Extracts a directory tree and writes into a file. (preferably .tree)"""

import os
from pathlib import Path
from maketree.console import Console
from maketree.utils import incremented_filename, now

from typing import Optional, List, Tuple


class Extractor:
    """Extract the dir-tree and write to a file"""

    @classmethod
    def extract(
        cls,
        path: Path,
        console: Optional[Console] = None,
    ) -> List[Tuple[str, str, int]]:
        """
        ### Extract
        Extract the directory structure and return the extracted tree list.

        #### Args:
        - `path`: path to a directory (must be a `Path` object)

        #### Output Tree Structure:
        ```
        tree = [
            (TYPE, NAME, DEPTH),
        ]
        ```
        """
        path = path.absolute()  # Path to absolute
        tree: List[Tuple[str, str, int]] = []

        # Write stuff to stuff.stuff :)
        for root, _, files in os.walk(path):
            current_path = Path(root)

            depth = len(current_path.relative_to(path).parts)
            dir_name = current_path.name or root

            console.verbose("found %s/..." % dir_name)

            # Append directory line
            tree.append(("directory", dir_name, depth))

            # Append file lines
            for file in files:
                console.verbose("found %s..." % file)
                tree.append(("file", file, (depth + 1)))

        return tree
