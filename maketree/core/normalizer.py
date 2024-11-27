""" Normalizes the parsed tree and creates paths. """

from os.path import join as join_path
from typing import List, Dict


class Normalizer:

    @classmethod
    def normalize(cls, tree: List[Dict]) -> Dict[str, List[str]]:
        """Normalizes tree as paths. Returns a dictionary of lists of file and dir paths."""
        dirs = []  # Holds normalized dirs
        files = []  # Holds normalized files

        def traverse(node: Dict, path: List):
            for child in node.get("children", []):
                name = child["name"]
                str_path = join_path(*path, name)

                if child["type"] == "directory":
                    dirs.append(str_path)
                    # Got Children?
                    if child["children"]:
                        traverse(child, path + [name])
                else:  # File
                    files.append(str_path)

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
