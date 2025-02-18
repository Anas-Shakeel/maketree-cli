"""Tests for maketree/console.py"""

from maketree.console import Console

console = Console(verbose=False, no_color=True)


def test_colored():
    """This Function only colors a string when NO_COLOR is False"""

    s = "This is a dummy string."
    assert console.colored(s, fgcolor="light_yellow", bgcolor="dark_grey") == s

    console.NO_COLOR = False
    assert console.colored(s, fgcolor="light_yellow", bgcolor="dark_grey") != s


def test_color_substrs():
    """This function colors all sub-strings found in a string."""
    # Doesn't Color, When NO_COLOR set to True
    console.NO_COLOR = True
    s = "This is a dummy string."
    colored_s = console.color_substrs(s, substrs=["is", "in"], fgcolor="green")
    assert colored_s == s

    # Colors, When NO_COLOR set to False
    console.NO_COLOR = False
    colored_s = console.color_substrs(s, substrs=["is", "in"], fgcolor="green")
    assert (
        colored_s
        == "Th\x1b[32mis\x1b[0m \x1b[32mis\x1b[0m a dummy str\x1b[32min\x1b[0mg."
    )
