""" Tests for maketree/core/parser.py """

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
            "type": "directory",
            "name": "src",
            "children": [
                {"type": "file", "name": "file1.txt"},
                {"type": "file", "name": "file2.txt"},
            ],
        },
        {"type": "file", "name": "LICENSE"},
        {"type": "file", "name": "README.md"},
    ]

    assert Parser._parse_lines(structure.splitlines()) == expected_tree
    assert Parser._parse_lines(["", "", ""]) == []  # Empty lines
