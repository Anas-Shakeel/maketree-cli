"""Tests for maketree/core/parser.py"""

from maketree.core.parser import Parser


def test_parse_lines():
    structure = """
src/
    file1.txt
    file2.txt
LICENSE
README.md
"""
    expected_tree = [
        {
            "name": "src",
            "type": "directory",
            "line": 1,
            "indent": 0,
            "children": [
                {"name": "file1.txt", "type": "file", "line": 2, "indent": 1},
                {"name": "file2.txt", "type": "file", "line": 3, "indent": 1},
            ],
        },
        {"name": "LICENSE", "type": "file", "line": 4, "indent": 0},
        {"name": "README.md", "type": "file", "line": 5, "indent": 0},
    ]

    parsed_tree = Parser._parse_lines(structure.splitlines())

    assert len(parsed_tree) == len(expected_tree)
    assert parsed_tree[0]["name"] == expected_tree[0]["name"]
    assert parsed_tree[1]["type"] == expected_tree[1]["type"]
    assert Parser._parse_lines(["", "", ""]) == []  # Empty lines
