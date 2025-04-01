"""Contains logic for writing extracted tree structure into a .tree file"""

from os.path import join, exists
from maketree.console import Console
from maketree.utils import incremented_filename

from typing import List, Tuple, Optional


class TreeWriter:
    """Write the tree extracted by `maketree.core.extractor`
    into a `.tree` file"""

    @classmethod
    def write(
        cls,
        extracted_tree: List[Tuple[str, str, int]],
        console: Console,
        save_to: str = ".",
    ) -> str:
        """
        ### Write
        Write the `extracted_tree` into a `.tree` file and return the filename.

        #### Args:
        - `extracted_tree`: the tree list extracted by `Extractor` class
        - `save_to`: where to save the final `.tree` file
        """
        assert exists(save_to), "'%s' does not exists" % save_to

        spacer = "    "  # Spacer for indentation

        # Non-Existent filename (Folder-Name or Timestamp)
        filename = join(save_to, extracted_tree[0][1])
        filename = incremented_filename("%s.tree" % filename)

        console.verbose("Creating %s..." % filename)

        # Write the tree
        with open(filename, "w", encoding="utf-8") as f:
            console.verbose("Writing tree to %s..." % filename)
            for entry in extracted_tree:
                f.write(
                    "%s%s%s\n"
                    % (
                        spacer * entry[2],
                        entry[1],
                        "/" if entry[0] == "directory" else "",
                    )
                )

        return filename
