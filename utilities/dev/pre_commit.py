# Copyright (c) 2026 Tobias Erbsland - https://erbsland.dev
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from dev.security_hashes import SecurityHashesApp
from lib.config import read_elcl_file
from lib.error import UtilityError
from lib.path_safety import (
    require_directory,
    require_safe_existing_file,
    resolve_project_path,
)
from lib.safe_tool import safe_subprocess_environment
from lib.utility import UtilityApp


@dataclass(frozen=True)
class GitLocalState:
    """A snapshot of local git state relevant for pre-commit checks."""

    status: bytes
    unstaged_diff: bytes
    staged_diff: bytes
    untracked_files: tuple[tuple[str, str, str], ...]


class PreCommitApp(UtilityApp):
    """Run pre-commit formatting and local checks."""

    description = "Run pre-commit formatting and local checks."

    def __init__(self) -> None:
        super().__init__()
        self.project_root = Path()
        self.black_options: list[str] = []
        self.black_directories: list[Path] = []
        self.black_files: list[Path] = []

    def handle_command_line_args(self, args) -> None:
        self.project_root = self.project_directory

    def read_config(self) -> None:
        """Read the pre-commit configuration."""
        self.print_verbose("Reading the configuration")
        config = read_elcl_file(self.config_file_path())
        black_config = config["black"]
        self.black_options = black_config.get_list("options", str, default=[])
        self.black_directories = [
            resolve_project_path(self.project_root, directory, "Black Directories")
            for directory in black_config.get_list("directories", str, default=[])
        ]
        self.black_files = [
            resolve_project_path(self.project_root, file, "Black Files")
            for file in black_config.get_list("files", str, default=[])
        ]
        self.validate_config()

    def validate_config(self) -> None:
        """Validate the pre-commit configuration."""
        for option in self.black_options:
            if not option:
                raise UtilityError("Black options must not contain empty values.")
        if not self.black_directories and not self.black_files:
            raise UtilityError("No black input paths configured.")
        for directory in self.black_directories:
            require_directory(directory, "Black Directories")
        for file in self.black_files:
            require_safe_existing_file(file, "Black Files")
            if not file.is_file():
                raise UtilityError(f"Black file does not exist or is not a regular file: {file}")

    def display_path(self, path: Path) -> str:
        """Create a user-friendly display path relative to the project."""
        try:
            return path.relative_to(self.project_root).as_posix()
        except ValueError:
            return str(path)

    def black_input_paths(self) -> list[str]:
        """Get configured black input paths for display and invocation."""
        paths = [*self.black_directories, *self.black_files]
        return [self.display_path(path) for path in paths]

    def run_black(self) -> None:
        """Run black over the configured Python sources."""
        input_paths = self.black_input_paths()
        if not input_paths:
            return
        print("Running black...")
        try:
            subprocess.run(
                [sys.executable, "-m", "black", *self.black_options, *input_paths],
                check=True,
                cwd=self.project_root,
                env=safe_subprocess_environment(),
            )
        except subprocess.CalledProcessError as error:
            raise UtilityError("black failed.") from error
        print("black completed.")

    def git_output(self, *args: str) -> bytes:
        """Run a git command and return its standard output."""
        try:
            result = subprocess.run(
                ["git", "-C", str(self.project_root), *args],
                check=True,
                capture_output=True,
                env=safe_subprocess_environment(),
            )
        except subprocess.CalledProcessError as error:
            message = error.stderr.decode("utf-8", errors="replace").strip()
            if not message:
                message = str(error)
            raise UtilityError(f"git {' '.join(args)} failed: {message}") from error
        return result.stdout

    def untracked_file_fingerprints(self) -> tuple[tuple[str, str, str], ...]:
        """Create content fingerprints for untracked files."""
        output = self.git_output("ls-files", "--others", "--exclude-standard", "-z")
        result = []
        for path_bytes in output.split(b"\0"):
            if not path_bytes:
                continue
            relative_path = os.fsdecode(path_bytes)
            path = self.project_root / relative_path
            if path.is_symlink():
                result.append((relative_path, "symlink", os.readlink(path)))
                continue
            if not path.exists():
                result.append((relative_path, "missing", ""))
                continue
            if not path.is_file():
                result.append((relative_path, "other", ""))
                continue
            digest = sha256(path.read_bytes()).hexdigest()
            result.append((relative_path, "file", digest))
        return tuple(sorted(result, key=lambda item: item[0].casefold()))

    def git_local_state(self) -> GitLocalState:
        """Capture the local git state before or after pre-commit tasks."""
        return GitLocalState(
            status=self.git_output("status", "--porcelain=v1", "-z", "--untracked-files=all"),
            unstaged_diff=self.git_output("diff", "--binary", "--no-ext-diff"),
            staged_diff=self.git_output("diff", "--cached", "--binary", "--no-ext-diff"),
            untracked_files=self.untracked_file_fingerprints(),
        )

    def require_unchanged_git_state(self, initial_state: GitLocalState) -> None:
        """Stop when pre-commit tasks changed the local git state."""
        final_state = self.git_local_state()
        if final_state == initial_state:
            return
        status = self.git_output("status", "--short", "--untracked-files=all").decode("utf-8", errors="replace")
        message = "Pre-commit made changes. Review the changes, then run pre_commit again."
        if status.strip():
            message += f"\n\nCurrent git status:\n{status.rstrip()}"
        raise UtilityError(message)

    def run_app(self, app: UtilityApp, name: str) -> None:
        """Run a child utility application."""
        print(f"Running {name}...")
        app.run(["--verbose"] if self.verbose else [])
        print(f"{name} completed.")

    def run(self, argv=None) -> None:
        """Run all pre-commit tasks."""
        super().run(argv)
        self.read_config()
        os.chdir(self.project_root)
        initial_git_state = self.git_local_state()
        try:
            self.run_black()
            self.run_app(SecurityHashesApp(), "security_hashes")
        finally:
            self.require_unchanged_git_state(initial_git_state)

        print("All pre-commit tasks completed successfully.")


def main():
    """Main entry point for pre-commit tasks."""
    raise SystemExit(PreCommitApp().main())


if __name__ == "__main__":
    main()
