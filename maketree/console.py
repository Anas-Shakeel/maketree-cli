import sys
from maketree.terminal_colors import printc, colored
from typing import List, Optional


class Console:
    """
    ### Console
    class for Input/Output

    #### ARGS:
    - `verbose`: decides whether to print verbose messages or not
    - `no_color`: decides whether to use colors in output or not

    """

    def __init__(
        self,
        verbose,
        no_color,
    ):
        self.VERBOSE = verbose
        self.NO_COLOR = no_color

        self.clr_info = "light_blue"
        self.clr_error = "light_red"
        self.clr_success = "light_green"
        self.clr_warning = "light_yellow"
        self.clr_primary = "light_magenta"
        self.clr_secondary = "yellow"

    def error(self, message: str):
        """Print `message` and exit with status `1`. Use for errors only."""
        print(colored("Error:", self.clr_error, attrs=["bold"]), message)
        sys.exit(1)

    def info(self, message: str):
        """Print `message`. Use for informational messages."""
        # print(colored("[INFO]", self.clr_info, attrs=["bold"]), message)
        printc(message, self.clr_info)

    def verbose(self, message: str):
        """Print `message`. Use for verbose messages."""
        if self.VERBOSE:
            print(colored("[INFO]", self.clr_info, attrs=["bold"]), message)
        # printc(message, self.clr_info)

    def warning(self, message: str):
        """Print `message`. Use for warning messages."""
        print(colored("Warning:", self.clr_warning, attrs=["bold"]), message)
        # printc(message, self.clr_warning)

    def success(self, message: str):
        """Print `message`. Use for success messages."""
        print(colored("Success:", self.clr_success, attrs=["bold"]), message)
        # printc(message, self.clr_success)

    def print(
        self,
        text: str,
        fgcolor: Optional[str] = None,
        bgcolor: Optional[str] = None,
        attrs: Optional[List[str]] = None,
        *,
        force_print: bool = False,
        sep: Optional[str] = " ",
        end: str = "\n",
        flush: bool = False,
    ):
        """
        ### Print
        Custom print function that prints `text`.

        ####  ARGS:
        - `text`: the text to print
        - `fgcolor`: foreground color of text
        - `bgcolor`: background color of text
        - `attrs`: attributes to apply to text
        - `force_print`: overrides VERBOSE, force prints text
        """
        # if not force_print:
        #     if not self.VERBOSE:
        #         return
        if not force_print and not self.verbose:
            return

        if self.NO_COLOR:
            print(text)
            return

        print(colored(text, fgcolor, bgcolor, attrs), sep=sep, end=end, flush=flush)

    def print_lines(
        self,
        lines: List[str],
        prefix: str = "",
        suffix: str = "",
        color: Optional[str] = None,
    ):
        """
        Print lines (list of strings).

        #### Args:
        - `lines`: list of strings
        - `prefix`: prefix string to add at the start of each line
        - `suffix`: suffix string to add at the end of each line
        - `color`: foreground color of strings
        """
        for line in lines:
            self.print(
                "%s%s%s" % (prefix, line, suffix),
                fgcolor=color,
            )

    def input_confirm(self, message: str, fgcolor: Optional[str] = None) -> bool:
        """Confirm and return `true` or `false`"""
        while True:
            try:
                self.print(message, fgcolor=fgcolor, force_print=True, end="")
                answer = input().lower()
                if answer == "y" or answer == "yes":
                    return True
                elif answer == "n" or answer == "no":
                    return False

                # Otherwise just repeat

            except KeyboardInterrupt:
                # Force quit
                sys.exit(1)
            except:
                continue
