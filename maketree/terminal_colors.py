""" Responsible for coloring the text (ANSI stuff) """

from typing import List

# ANSI Attribute codes
ATTRIBUTES = {
    "bold": 1,
    "dark": 2,
    "italic": 3,
    "underline": 4,
    "blink": 5,
    "reverse": 7,
    "concealed": 8,
    "strike": 9,
    "double-underline": 21,
    "overline": 53,
}

# Standard Foreground Colors (4-bit)
COLORS = {
    "black": 30,
    "grey": 30,  # Actually black but kept for backwards compatibility
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "light_grey": 37,
    "dark_grey": 90,
    "light_red": 91,
    "light_green": 92,
    "light_yellow": 93,
    "light_blue": 94,
    "light_magenta": 95,
    "light_cyan": 96,
    "white": 97,
}


def get_color(color: str, mode: str = "fg") -> int:
    """Returns color code of `color` based on mode `fg` or `bg`"""
    assert mode in ["fg", "bg"], f"mode '{mode}' is not a valid mode."

    if mode == "fg":
        return COLORS[color]
    return COLORS[color] + 10


def colored(
    text: str,
    fgcolor: str = None,
    bgcolor: str = None,
    attrs: List[str] = None,
) -> str:
    """Colorize and return text."""
    assert isinstance(text, str), "text must be str"
    assert text, "text must not be empty"

    # Ansi Format string
    FMT_STR = "\033[%dm%s"

    result = text

    # Apply foreground color
    if fgcolor:
        result = FMT_STR % (get_color(fgcolor), result)

    # Apply background color
    if bgcolor:
        result = FMT_STR % (get_color(bgcolor, "bg"), result)

    # Apply attributes
    if attrs:
        for attr in attrs:
            result = FMT_STR % (ATTRIBUTES[attr], result)

    return result + "\033[0m"


def printc(
    text: str,
    fgcolor: str = None,
    bgcolor: str = None,
    attrs: List[str] = None,
):
    """Colorize and then print text"""
    print(colored(text, fgcolor, bgcolor, attrs))
