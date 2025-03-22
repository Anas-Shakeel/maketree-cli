"""Extracts a directory tree and writes into a file. (preferably .tree)"""

from pathlib import Path
from typing import Optional
from maketree.console import Console
from maketree.utils import incremented_filename, now


class Extractor:
    """Extract the dir-tree and write to a file"""

    @classmethod
    def extract(
        cls,
        path: Path,
        console: Optional[Console] = None,
    ) -> str:
        """
        ### Extract
        Extract the directory structure.

        #### Args:
        - `path`: path to a directory (must be a `Path` object)

        Returns the name of the file created. (filename taken from the root directory's name)
        """
        path = path.absolute()  # Path to absolute
        spacer = "    "  # Spacer for indentation

        # Non-Existent filename
        filename = path.name or now("%d%m%Y-%H%M%S")  # Folder-Name or Timestamp
        filename = incremented_filename("%s.tree" % filename)

        console.verbose("Creating %s..." % filename)

        # Write stuff to stuff.stuff :)
        with open(filename, "w", encoding="utf-8") as f:
            for current, _, files in path.walk():
                depth = len(current.relative_to(path).parts)  # Indent depth
                dir_name = current.name or str(current)  # Current dir name

                console.verbose("found %s/..." % dir_name)
                # Write directory line
                f.write("%s%s/\n" % (spacer * depth, dir_name))

                # Write file lines
                for file in files:
                    console.verbose("found %s..." % file)
                    f.write("%s%s\n" % (spacer * (depth + 1), file))

        return filename
