import re

import pint

from ..regex_utils import alternation
from ..utils import dash_characters


def get_unit_registry() -> pint.UnitRegistry:
    return pint.UnitRegistry()


def remove_space_after_initial_dash(text: str) -> str:
    """
    Remove the space directly after a dash at the beginning of a string.

    Necessary because quantulum struggles with "- 10 °C".

    Returns:
        same string, without the space if applicable
    """
    pattern = '^' + alternation(dash_characters, capture_group=True) + ' +'
    return re.sub(pattern, r'\1', text)
