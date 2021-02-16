import re
from typing import List

from .filter import Filter
from ..regex_utils import RegexMatch, match_all, alternation, optional

_optional_of = optional(' of')

_descriptors = [
    # solution
    f'solutions?{_optional_of}',
    fr'sol\.{_optional_of}',

    # mixture
    f'mixture{_optional_of}',

    # dispersion
    f'dispersion{_optional_of}',

    # suspension
    f'suspension{_optional_of}',

    # solvent
    f'solvent',
]


class MatterWordFilter(Filter):
    """
    Finds substantives for types of compounds/matter in compound names.
    """

    def __init__(self):
        self.regex = re.compile(alternation(_descriptors), re.IGNORECASE)

    def find_matches(self, chemical_name: str) -> List[RegexMatch]:
        return match_all(self.regex, chemical_name)
