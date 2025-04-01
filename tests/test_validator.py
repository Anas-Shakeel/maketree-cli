"""Tests for maketree/core/validator.py"""

from sys import platform
from pytest import raises
from maketree.core.validator import Validator, ValidationError
from maketree.core.parser import Parser
from maketree.console import Console

# Create temporary files/folders inside this and delete aftwards
TEMP_DIR = "temp"


def test_validate():
    console = Console(verbose=False, no_color=True)

    # Valid
    Validator.validate(
        Parser()._parse_lines(["file1.txt", "file2.txt"]),
        console=console,
    )

    # Valid
    Validator.validate(
        Parser()._parse_lines(["src/", "index.html", "style.css"]),
        console=console,
    )

    # Invalid: character '/'
    with raises(ValidationError):
        Validator.validate(
            Parser()._parse_lines(["../file1.txt", "file2.txt"]),
            console=console,
        )

    # Invalid: invalid filename '.' or '..'
    with raises(ValidationError):
        Validator.validate(
            Parser()._parse_lines([".", ".."]),
            console=console,
        )

    # Invalid (only on windows): Windows Reserved name
    if platform == "win32":
        with raises(ValidationError):
            Validator.validate(
                Parser()._parse_lines(["CON", "AUX.txt"]),
                console=console,
            )

    # Invalid: invalid character '/' in directory
    if platform == "win32":
        with raises(ValidationError):
            Validator.validate(
                Parser()._parse_lines(["fold/er/", "folder\\2/"]),
                console=console,
            )
