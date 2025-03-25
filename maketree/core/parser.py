"""Responsible for reading and parsing the structure file (in `.tree` format),
that users provide to define the directory structure."""

from maketree.utils import is_valid_dir, is_valid_file
from typing import List


class ParseError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.args = args


class Parser:

    @classmethod
    def parse_file(cls, filepath: str):
        """Parse `filepath` .tree file and return the tree in a usable format (e.g, `dict` or `list`)"""
        with open(filepath, encoding="utf-8") as srcfile:
            raw_data = srcfile.readlines()

        return Parser._parse_lines(raw_data)

    @classmethod
    def _parse_lines(cls, lines: List[str]):
        """Parse `lines` into tree structure"""
        stack = []  # Keep track of parent dirs
        tree = []  # Final parsed tree (list of dicts)

        for i, line in enumerate(lines):
            line = line.rstrip()

            # Empty line?
            if not line:
                continue

            # Indentation level of current entry
            indent_level: int = (len(line) - len(line.lstrip())) // 4

            if line.endswith("/"):  # Its a Directory
                item = {
                    "name": line.strip()[:-1],  # Remove `/` too
                    "type": "directory",
                    "line": i + 1,
                    "indent": indent_level,
                    "children": [],
                }

                # Pop from stack til the correct parent
                while stack and stack[-1]["indent_level"] >= indent_level:
                    stack.pop()

                if stack:
                    # Add this dir to its parent's children
                    stack[-1]["item"]["children"].append(item)
                else:
                    # Top Level directory, stack is empty
                    tree.append(item)

                # Push this dir onto stack
                stack.append({"item": item, "indent_level": indent_level})

            else:  # Its a File
                item = {
                    "name": line.strip(),
                    "type": "file",
                    "line": i + 1,
                    "indent": indent_level,
                }

                # Pop from stack til the correct parent
                while stack and stack[-1]["indent_level"] >= indent_level:
                    stack.pop()

                if stack:
                    # Add this file to current parent's children
                    stack[-1]["item"]["children"].append(item)
                else:
                    # Top Level file, stack empty
                    tree.append(item)

        return tree
