# Copyright (c) 2026 Tobias Erbsland - https://erbsland.dev
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from .error import UtilityError


class UtilityApp:
    """
    The base class for all utility scripts.
    This base class makes sure utility scripts follow common guidelines and conventions.
    All utility scripts must derive from this class and are invoked like this:

    <code>
    if __name__ == "__main__":
        ws = ExampleApp()
        ws.main()
    </code>
    """

    description = "Run a development utility."

    def __init__(self) -> None:
        """Create a new utility application instance."""
        self.verbose = False
        self.program_name: str | None = None

    @property
    def project_directory(self) -> Path:
        """Access the project root directory."""
        return Path(__file__).resolve().parents[2]

    def config_file_path(self) -> Path:
        """Get the standard configuration path for this utility."""
        module = sys.modules[self.__class__.__module__]
        module_file = getattr(module, "__file__", None)
        if module_file is None:
            raise UtilityError(f"Cannot determine configuration file for {self.__class__.__name__}.")
        module_path = Path(module_file)
        return module_path.parent.parent / "conf" / f"{module_path.stem}.elcl"

    def print_verbose(self, message: str) -> None:
        """Print a message if verbose mode is enabled."""
        if self.verbose:
            print(message)

    def add_command_line_args(self, parser: argparse.ArgumentParser) -> None:
        """
        Add command line arguments to the parser for the utility script.
        Override this method to customize command line parsing for the utility script.
        """

    def handle_command_line_args(self, args: argparse.Namespace) -> None:
        """
        Handle the parsed command line arguments.
        Override this method to customize argument handling for the utility script.
        """

    def parse_command_line(self, argv: Sequence[str] | None = None) -> argparse.Namespace:
        """
        Parses the command line arguments and sets up the utility script.
        Extend or override this method to customize command line parsing for the utility script.
        """
        parser = argparse.ArgumentParser(prog=self.program_name, description=self.description)
        parser.add_argument("-v", "--verbose", action="store_true", help="Print progress details.")
        self.add_command_line_args(parser)
        args = parser.parse_args(argv)
        self.verbose = args.verbose
        self.handle_command_line_args(args)
        return args

    def run(self, argv: Sequence[str] | None = None) -> None:
        """
        Runs the individual stages of the utility script.
        Extend or override this method to implement the specific functionality of the utility script.
        """
        self.parse_command_line(argv)

    def main(self, argv: Sequence[str] | None = None) -> int:
        """
        The main method that should be called if the script is run from the command line.
        """
        try:
            self.run(argv)
            return 0
        except UtilityError as error:
            print(error, file=sys.stderr)
            return error.get_exit_code()
        except KeyboardInterrupt:
            print("Interrupted.", file=sys.stderr)
            return 130
        except Exception as error:
            if self.verbose:
                raise
            print(f"Unexpected error: {error}", file=sys.stderr)
            return 1
