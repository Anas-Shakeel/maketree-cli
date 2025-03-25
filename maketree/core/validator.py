import sys
from maketree.utils import is_valid_dir, is_valid_file
from maketree.console import Console
from typing import Dict, List, Any, Optional


class Validator:
    @classmethod
    def validate(cls, tree: List[Dict], console: Optional[Console] = None):
        cls.console = console

        # Validate every item (dir/file)
        for item in tree:
            if item["type"] == "directory":
                valid = is_valid_dir(item["name"])
                # Print Error and Exit
                if valid is not True:
                    print(cls.format_error(item, error_message=valid))
                    sys.exit(1)

            else:  # File
                valid = is_valid_file(item["name"])
                # Print Error and Exit
                if valid is not True:
                    print(cls.format_error(item, error_message=valid))
                    sys.exit(1)

            # Recurse (if directory)
            if item.get("children"):
                cls.validate(item["children"], console)

    @classmethod
    def format_error(cls, item: Dict[str, Any], error_message: str) -> str:
        slash = "/" if item["type"] == "directory" else ""
        spacer = "    " * item["indent"]

        clr_error = cls.console.clr_error
        label = cls.console.colored("Error:", fgcolor=clr_error)
        reason_label = cls.console.colored("Reason:", fgcolor=cls.console.clr_primary)
        underline = cls.console.colored(
            "^" * len(item["name"]),
            fgcolor=clr_error,
        )

        # Construct
        return (
            f"{label} at line {item['line']}\n"
            f"{spacer}{item['name']}{slash}\n"
            f"{spacer}{underline}\n"
            f"{reason_label} {error_message}"
        )

        # return (
        #     f"At line {item['line']}\n"
        #     f"{spacer}{item['name']}{slash}\n"
        #     f"{spacer}{'^' * len(item['name'])}\n"
        #     f"Reason: {error_message}"
        # )
