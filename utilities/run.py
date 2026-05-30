# Copyright (c) 2026 Tobias Erbsland - https://erbsland.dev
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import importlib
import sys
from dataclasses import dataclass
from shutil import get_terminal_size
from textwrap import TextWrapper


@dataclass(frozen=True)
class RegisteredUtility:
    display_name: str
    module_path: str
    class_name: str
    help: str | None = None


REGISTERED_UTILITIES = {
    "github_workflows": RegisteredUtility(
        "GitHub Workflows",
        "dev.github_workflows",
        "GitHubWorkflowsApp",
        help="Audit GitHub workflow action pins and version annotations.",
    ),
    "pre_commit": RegisteredUtility(
        "Pre-Commit",
        "dev.pre_commit",
        "PreCommitApp",
        help="Run pre-commit formatting and local checks.",
    ),
    "security_hashes": RegisteredUtility(
        "Security Hashes",
        "dev.security_hashes",
        "SecurityHashesApp",
        help="Generate or verify security hashes for infrastructure files.",
    ),
}


def show_help() -> None:
    print("Usage: python3 utilities/run.py <utility_name> [<utility_arguments>]")
    print("Available utilities:")
    help_indent = 8
    term_width = get_terminal_size(fallback=(80, 24)).columns
    wrapper = TextWrapper(
        width=term_width - help_indent,
        initial_indent=" " * help_indent,
        subsequent_indent=" " * help_indent,
    )
    for identifier, utility in REGISTERED_UTILITIES.items():
        print(f"- {identifier} - {utility.display_name}")
        if utility.help:
            print(wrapper.fill(utility.help))


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        show_help()
        return 1
    if argv[0] in {"-h", "--help"}:
        show_help()
        return 0
    if argv[0] not in REGISTERED_UTILITIES:
        print(f"Unknown utility: {argv[0]}", file=sys.stderr)
        show_help()
        return 1
    utility = REGISTERED_UTILITIES[argv[0]]
    module = importlib.import_module(utility.module_path)
    app_class = getattr(module, utility.class_name)
    app = app_class()
    app.program_name = f"utilities/run.py {argv[0]}"
    return app.main(argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
