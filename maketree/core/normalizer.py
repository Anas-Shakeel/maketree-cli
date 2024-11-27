""" Normalizes the parsed tree and creates paths. """

from os.path import join as join_path
from typing import List, Dict, Set


class Normalizer:

    @classmethod
    def normalize(cls, tree: List[Dict]) -> Dict[str, Set[str]]:
        """
        Normalizes tree as paths and remove any duplicate paths.
        Returns a dictionary of Two Sets containing file and dir paths.

        ```
        # Output Dict
        {
            "directories": {'./src', './docs'}
            "files": {
                'index.html',
                'styles.css',
                'user-guide.md',
                'dev-guide.md'
            }
        }
        ```
        """
        dirs = set()  # Holds normalized dirs
        files = set()  # Holds normalized files

        def traverse(node: Dict, path: List):
            for child in node.get("children", []):
                name = child["name"]
                str_path = join_path(*path, name)

                if child["type"] == "directory":
                    dirs.add(str_path)
                    # Got Children?
                    if child["children"]:
                        traverse(child, path + [name])
                else:  # File
                    files.add(str_path)

        traverse(
            node={
                "type": "directory",
                "name": ".",
                "children": tree,
            },
            path=["."],
        )

        # Return as a dictionary
        return {
            "directories": dirs,
            "files": files,
        }
