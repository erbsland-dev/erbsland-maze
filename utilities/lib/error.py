# Copyright (c) 2026 Tobias Erbsland - https://erbsland.dev
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations


class UtilityError(Exception):
    """
    Base class for all utility script errors.

    Throw this exception for expected user-facing utility failures.
    """

    def __init__(self, message: str, *, exit_code: int = 1):
        super().__init__(message)
        self.exit_code = exit_code

    def get_exit_code(self) -> int:
        """
        Get the exit code associated with this error.
        """
        return self.exit_code

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return f"UtilityError(message='{self.args[0]}', exit_code={self.exit_code})"
