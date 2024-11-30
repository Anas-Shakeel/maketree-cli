""" Tests for maketree/core/normalizer.py """

from os.path import normpath
from maketree.core.normalizer import Normalizer
from maketree.core.parser import Parser


def test_normalize():
    src = """
src/
    file.txt
    file.json
README.md
"""
    parsed_tree = Parser._parse_lines(src.splitlines())
    expected_paths = {
        "directories": [
            str(normpath("root/src/")),
        ],
        "files": [
            str(normpath("root/src/file.txt")),
            str(normpath("root/src/file.json")),
            str(normpath("root/README.md")),
        ],
    }

    assert Normalizer.normalize(parsed_tree, "root") == expected_paths
