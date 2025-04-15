#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
import re
from dataclasses import dataclass
from colorsys import hls_to_rgb, hsv_to_rgb

RE_HEX = re.compile(r"#([0-9a-f]{3,8})")
RE_RGB = re.compile(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([\d.]+))?\s*\)")
RE_HSL = re.compile(r"hsl\(\s*(\d+)\s*,\s*(\d+)%\s*,\s*(\d+)%\s*(?:,\s*([\d.]+))?\s*\)")


def clamp(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    """Clamp a float value between a minimum and a maximum."""
    return min(max(value, min_value), max_value)


@dataclass
class Color:
    """
    Represents an RGBA color with channels normalized between 0.0 and 1.0.
    """

    r: float = 0.0
    g: float = 0.0
    b: float = 0.0
    a: float = 1.0

    def __post_init__(self):
        invalid = [
            (name, val) for name, val in zip("rgba", (self.r, self.g, self.b, self.a)) if not (0.0 <= val <= 1.0)
        ]
        if invalid:
            name, val = invalid[0]
            raise ValueError(f"Color channel '{name}' out of range: {val} (expected 0.0 – 1.0)")

    @staticmethod
    def for_endpoint(index: int, total_count: int) -> "Color":
        """
        Create the default color for an endpoint.

        :param index: The index of the endpoint.
        :param total_count: The total number of endpoints.
        :return: A color object.
        """
        return Color(*hsv_to_rgb(index / (total_count + 1), 0.5, 0.8))

    @staticmethod
    def _hex_to_color_components(hex_val: str) -> tuple[float, float, float, float]:
        """
        Convert a hex string (of length 3, 4, 6, or 8) to RGBA components normalized between 0.0 and 1.0.
        Uses structural pattern matching based on the length of the hex string.
        """
        match len(hex_val):
            case 3:
                r, g, b = (int(c * 2, 16) / 255 for c in hex_val)
                a = 1.0
            case 4:
                r, g, b, a = (int(c * 2, 16) / 255 for c in hex_val)
            case 6:
                r = int(hex_val[0:2], 16) / 255
                g = int(hex_val[2:4], 16) / 255
                b = int(hex_val[4:6], 16) / 255
                a = 1.0
            case 8:
                r = int(hex_val[0:2], 16) / 255
                g = int(hex_val[2:4], 16) / 255
                b = int(hex_val[4:6], 16) / 255
                a = int(hex_val[6:8], 16) / 255
            case _:
                raise ValueError(f"Invalid hex string length: {len(hex_val)}")
        return r, g, b, a

    @staticmethod
    def from_text(value: str) -> "Color":
        """
        Create a Color instance from a string representation.

        Supported formats:
         - Hex: #RGB, #RGBA, #RRGGBB, #RRGGBBAA
         - RGB: rgb(r, g, b) or rgb(r, g, b, a)
         - HSL: hsl(h, s%, l%) or hsl(h, s%, l%, a)

        :param value: The color string.
        :returns: A new Color instance.
        :raises ValueError: If the format is unsupported or channels are out of range.
        """
        value = value.strip().lower()

        if hex_match := RE_HEX.fullmatch(value):
            hex_val = hex_match.group(1)
            r, g, b, a = Color._hex_to_color_components(hex_val)
            return Color(r, g, b, a)

        elif rgb_match := RE_RGB.fullmatch(value):
            r = int(rgb_match.group(1)) / 255
            g = int(rgb_match.group(2)) / 255
            b = int(rgb_match.group(3)) / 255
            a = float(rgb_match.group(4)) if rgb_match.group(4) else 1.0
            a = clamp(a)
            return Color(r, g, b, a)

        elif hsl_match := RE_HSL.fullmatch(value):
            h = int(hsl_match.group(1)) % 360 / 360
            s = int(hsl_match.group(2)) / 100
            l = int(hsl_match.group(3)) / 100
            a = float(hsl_match.group(4)) if hsl_match.group(4) else 1.0
            a = clamp(a)
            r, g, b = hls_to_rgb(h, l, s)
            return Color(r, g, b, a)

        raise ValueError(f"Unsupported color format: {value}")
