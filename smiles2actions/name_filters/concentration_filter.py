import re
from typing import List

from .filter import Filter
from ..regex_utils import match_all, RegexMatch, real_number_regex, alternation, optional

_approx_symbol = optional('[~˜∼] ?')
_concentration_units = [
    r'M\b',
    r'-?[Mm]olar\b',
    r'N\b',
    r'-?[Nn]ormal\b',
    r'mol/L',
    r'mol/l',
    r'percent',
    r'% \(?[vVwW]/[vVwW]\)?',  # v/v, (v/v), (V/V), w/v, etc.
    r'\(?[vVwW]/[vVwW]\)? %',  # v/v, (v/v), (V/V), w/v, etc.
    r'% wt\.?',
    r'wt\.? %',
    r'volume %',
    r'%',  # last, otherwise it will have priority over other concentration units starting with %
]


class ConcentrationFilter(Filter):
    """Finds concentration specification (as numbers) in chemical names"""

    def __init__(self):
        unit_regex = alternation(_concentration_units)
        reg_string = fr'{_approx_symbol}\b{real_number_regex} ?{unit_regex}'
        self.regex = re.compile(reg_string)

    def find_matches(self, chemical_name: str) -> List[RegexMatch]:
        matches = match_all(self.regex, chemical_name)
        return matches
