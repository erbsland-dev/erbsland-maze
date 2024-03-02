#  Copyright © 2003-2024 Tobias Erbsland. Web: https://erbsland.dev/
#  SPDX-License-Identifier: GPL-3.0-or-later
from typing import cast

from .blank_modifier import BlankModifier
from .closing_modifier import ClosingModifier
from .frame_modifier import FrameModifier
from .merge_modifier import MergeModifier
from .modifier import Modifier
from .modifier_type import ModifierType


class Modifiers:
    """
    A collection of modifiers.
    """

    def __init__(self, modifiers: list[Modifier] = None):
        self._modifiers: list[Modifier] = modifiers or []

    def _get_modifiers(self, modifier_type: ModifierType) -> list[Modifier]:
        return [m for m in self._modifiers if m.modifier_type == modifier_type]

    def get_blank_modifiers(self) -> list[BlankModifier]:
        result = sorted(self._get_modifiers(ModifierType.BLANK), key=lambda m: m.placement.order_value)
        return cast(list[BlankModifier], result)

    def get_frame_modifiers(self) -> list[FrameModifier]:
        result = self._get_modifiers(ModifierType.FRAME)
        return cast(list[FrameModifier], result)

    def get_merge_modifiers(self) -> list[MergeModifier]:
        result = sorted(self._get_modifiers(ModifierType.MERGE), key=lambda m: m.placement.order_value)
        return cast(list[MergeModifier], result)

    def get_closing_modifiers(self) -> list[ClosingModifier]:
        result = self._get_modifiers(ModifierType.CLOSING)
        return cast(list[ClosingModifier], result)
