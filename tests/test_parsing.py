#  Copyright (c) 2026 Tobias Erbsland - https://erbsland.dev
#  SPDX-License-Identifier: Apache-2.0

import pytest

from erbsland_maze import (
    BlankModifier,
    Color,
    FrameModifier,
    PathEnd,
    Placement,
    RoomOffset,
    RoomSize,
    SvgFillMode,
)


def test_color_accepts_common_text_formats() -> None:
    hex_color = Color.from_text("#0f08")
    assert hex_color.r == pytest.approx(0.0)
    assert hex_color.g == pytest.approx(1.0)
    assert hex_color.b == pytest.approx(0.0)
    assert hex_color.a == pytest.approx(0x88 / 255)

    rgb_color = Color.from_text("rgb(255, 128, 0, 0.5)")
    assert rgb_color.r == pytest.approx(1.0)
    assert rgb_color.g == pytest.approx(128 / 255)
    assert rgb_color.b == pytest.approx(0.0)
    assert rgb_color.a == pytest.approx(0.5)

    hsl_color = Color.from_text("hsl(120, 100%, 50%)")
    assert hsl_color.r == pytest.approx(0.0)
    assert hsl_color.g == pytest.approx(1.0)
    assert hsl_color.b == pytest.approx(0.0)


def test_color_rejects_invalid_values() -> None:
    with pytest.raises(ValueError):
        Color(1.1, 0.0, 0.0)
    with pytest.raises(ValueError):
        Color.from_text("not-a-color")


def test_room_size_and_offset_parsing() -> None:
    assert RoomSize.from_text("medium") == RoomSize(3, 3)
    assert RoomSize.from_text("2x5") == RoomSize(2, 5)
    assert RoomOffset.from_text("3") == RoomOffset(3, 0, is_relative=True)
    assert RoomOffset.from_text("-4,2") == RoomOffset(-4, 2, is_relative=False)

    with pytest.raises(ValueError):
        RoomSize.from_text("0")
    with pytest.raises(ValueError):
        RoomOffset.from_text("1,2,3")


def test_placement_and_path_end_parsing() -> None:
    assert Placement.from_text("nw") is Placement.TOP_LEFT
    assert Placement.from_text("center") is Placement.CENTER

    path_end = PathEnd.from_text("se/2/x")
    assert path_end.placement is Placement.BOTTOM_RIGHT
    assert path_end.offset == RoomOffset(2, 0, is_relative=True)
    assert path_end.is_dead_end is True
    assert str(path_end) == "se/2/x"

    with pytest.raises(ValueError):
        PathEnd.from_text("r/1")


def test_modifier_parsing() -> None:
    blank = BlankModifier.from_text("c/3x2/-1,4")
    assert blank.placement is Placement.CENTER
    assert blank.size == RoomSize(3, 2)
    assert blank.offset == RoomOffset(-1, 4, is_relative=False)

    frame = FrameModifier.from_text("1,2,3,4")
    assert frame.insets.north == 1
    assert frame.insets.east == 2
    assert frame.insets.south == 3
    assert frame.insets.west == 4


def test_svg_fill_mode_aliases() -> None:
    assert SvgFillMode.from_text("se") is SvgFillMode.STRETCH_EDGE
    assert SvgFillMode.from_text("fixed_center") is SvgFillMode.FIXED_CENTER
