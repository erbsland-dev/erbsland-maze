# Copyright (c) 2026 Tobias Erbsland - https://erbsland.dev
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SafeExecutable:
    """Result of a safe executable lookup."""

    name: str
    path: Path | None
    resolved_path: Path | None
    is_safe: bool
    warning: str | None = None


def find_safe_executable(name: str, allowed_directories: tuple[Path, ...]) -> SafeExecutable:
    """Find an executable and verify that its resolved path is in an allowed directory."""
    executable = shutil.which(name)
    if executable is None:
        return SafeExecutable(name, None, None, False, f"Could not find `{name}` in PATH.")
    path = Path(executable)
    resolved_path = path.resolve()
    for directory in allowed_directories:
        resolved_directory = directory.resolve()
        if resolved_path == resolved_directory or resolved_path.is_relative_to(resolved_directory):
            return SafeExecutable(name, path, resolved_path, True)
    allowed = ", ".join(str(directory) for directory in allowed_directories)
    return SafeExecutable(
        name,
        path,
        resolved_path,
        False,
        f"Refusing to run `{name}` from unsafe location: {resolved_path}. Allowed locations: {allowed}.",
    )


def safe_subprocess_environment() -> dict[str, str]:
    """Create a minimal environment for external tools."""
    allowed_names = {"HOME", "LANG", "LC_ALL", "LC_CTYPE", "PATH", "TMPDIR", "TEMP", "TMP"}
    return {name: value for name, value in os.environ.items() if name in allowed_names}
