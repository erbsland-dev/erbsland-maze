#  Copyright (c) 2026 Tobias Erbsland - https://erbsland.dev
#  SPDX-License-Identifier: Apache-2.0

import pytest

from erbsland_maze import Parity, RoomLocation, RoomSize, SvgFillMode, SvgLayout, SvgSetup


def test_svg_setup_validates_dimensions_and_types() -> None:
    setup = SvgSetup(width=40.0, height=60.0)
    assert setup.get_size().width == pytest.approx(40.0)
    assert setup.get_size().height == pytest.approx(60.0)

    with pytest.raises(ValueError):
        SvgSetup(width=0.5, height=60.0)
    with pytest.raises(TypeError):
        SvgSetup(width=40.0, height=60.0, width_parity="odd")
    with pytest.raises(ValueError):
        SvgSetup(width=40.0, height=60.0, side_length=1.0, wall_thickness=0.8)


def test_svg_layout_calculates_room_count_and_rectangles() -> None:
    layout = SvgLayout(
        SvgSetup(
            width=42.0,
            height=42.0,
            side_length=4.0,
            width_parity=Parity.ODD,
            height_parity=Parity.ODD,
        )
    )

    size = layout.initialize()
    assert size == RoomSize(9, 9)

    first_rect = layout.get_location_rectangle(RoomLocation(0, 0))
    assert first_rect.pos.x == pytest.approx(0.0)
    assert first_rect.pos.y == pytest.approx(0.0)
    assert first_rect.size.width == pytest.approx(42.0 / 9)
    assert first_rect.size.height == pytest.approx(42.0 / 9)


def test_svg_layout_fixed_center_keeps_requested_room_size() -> None:
    layout = SvgLayout(
        SvgSetup(
            width=42.0,
            height=40.0,
            side_length=4.0,
            fill_mode=SvgFillMode.FIXED_CENTER,
            width_parity=Parity.NONE,
            height_parity=Parity.NONE,
        )
    )

    size = layout.initialize()
    assert size == RoomSize(10, 10)

    first_rect = layout.get_location_rectangle(RoomLocation(0, 0))
    assert first_rect.pos.x == pytest.approx(1.0)
    assert first_rect.pos.y == pytest.approx(0.0)
    assert first_rect.size.width == pytest.approx(4.0)
    assert first_rect.size.height == pytest.approx(4.0)
