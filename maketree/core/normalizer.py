""" Normalizes the parsed tree and creates paths. """

from os.path import join as join_path
from typing import List, Dict


class Normalizer:

    @classmethod
    def normalize(cls, tree: List[Dict], rootpath: str = ".") -> Dict[str, List[str]]:
        """
        Normalizes tree as paths and remove any duplicate paths.
        Returns a dictionary of Two Lists containing file and dir paths.

        ```
        # Output Dict
        {
            "directories": ['./src', './assets']
            "files": [
                './assets/logo.svg',
                './assets/image.png',
                './assets/font.ttf',
                './src/index.html',
                './src/styles.css',
                './user-guide.md',
                './dev-guide.md',
            ]
        }
        ```
        """
        dirs = []  # Holds normalized dirs
        files = []  # Holds normalized files

        def traverse(node: Dict, path: List):
            for child in node.get("children", []):
                name = child["name"]
                str_path = join_path(*path, name)

                if child["type"] == "directory":
                    # Add if not already
                    if str_path not in dirs:
                        dirs.append(str_path)
                    # Got Children?
                    if child["children"]:
                        traverse(child, path + [name])
                else:  # File
                    if str_path not in files:
                        files.append(str_path)

        traverse(
            node={
                "type": "directory",
                "name": rootpath,
                "children": tree,
            },
            path=[rootpath],
        )

        # Return as a dictionary
        return {
            "directories": dirs,
            "files": files,
        }
