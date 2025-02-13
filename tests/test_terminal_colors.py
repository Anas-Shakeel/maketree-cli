""" Tests for maketree/terminal_colors.py """

from pytest import raises
from maketree.terminal_colors import colored, get_color


def test_get_color():
    assert get_color("green", "fg") == 32
    assert get_color("yellow", "fg") == 33
    assert get_color("light_cyan", "fg") == 96
    assert get_color("white", "fg") == 97

    # All background colors 10 ahead of their foregrounds
    assert get_color("green", "bg") == 32 + 10
    assert get_color("yellow", "bg") == 33 + 10
    assert get_color("light_cyan", "bg") == 96 + 10
    assert get_color("white", "bg") == 97 + 10


def test_colored():
    # No matter what, reset code gets added (takes `if` to avoid, unnecessary)

    assert colored("This is string.", "blue") == "\x1b[34mThis is string.\x1b[0m"
    assert (
        colored("This is string.", "blue", "dark_grey")
        == "\x1b[100m\x1b[34mThis is string.\x1b[0m"
    )

    with raises(AssertionError):
        assert colored(4, "blue") == "\033[0m"

    with raises(AssertionError):
        assert colored("") == "\033[0m"
