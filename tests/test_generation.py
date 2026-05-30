#  Copyright (c) 2026 Tobias Erbsland - https://erbsland.dev
#  SPDX-License-Identifier: Apache-2.0

import subprocess
import sys
from random import seed
from pathlib import Path

from erbsland_maze import BlankModifier, Generator, GeneratorSetup, SvgLayout, SvgSetup


def test_generator_writes_svg_file(tmp_path: Path) -> None:
    seed(1)
    output_path = tmp_path / "maze.svg"
    generator = Generator(
        SvgLayout(SvgSetup(width=40.0, height=40.0, start_end_mark=False)),
        GeneratorSetup(verbose=False),
    )

    generator.generate_and_save(output_path)

    text = output_path.read_text(encoding="utf-8")
    assert text.startswith("<?xml")
    assert "<svg" in text
    assert "<path" in text


def test_generator_layout_only_reflects_modifiers(tmp_path: Path) -> None:
    output_path = tmp_path / "layout.svg"
    generator = Generator(
        SvgLayout(SvgSetup(width=40.0, height=40.0, start_end_mark=False)),
        GeneratorSetup(
            modifiers=[BlankModifier.from_text("c/3")],
            verbose=False,
            layout_only=True,
        ),
    )

    generator.generate_and_save(output_path)

    text = output_path.read_text(encoding="utf-8")
    assert "<svg" in text
    assert "path" in text


def test_legacy_script_wrapper_exposes_help() -> None:
    result = subprocess.run(
        [sys.executable, "src/generate_maze.py", "--help"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "usage:" in result.stdout
    assert "--width" in result.stdout
