import re
from typing import List

from .filter import Filter
from ..regex_utils import RegexMatch, match_all, alternation, optional
from ..utils import dash_characters

_optional_of = optional(' of')

_descriptors = [
    r'\b[Ss]olid\b' + _optional_of,
    r'\b[Ll]iquid\b' + _optional_of,
    r'\bgas\b',
    r'\(s\)',
    r'\(g\)',
    r'\b[Mm]etal' + optional('lic'),
]


class StateFilter(Filter):
    """
    Looks for substrings related to the state (solid, liquid, gaseous).
    """

    def __init__(self):
        regex_string = alternation(_descriptors)
        self.regex = re.compile(regex_string)

    def find_matches(self, chemical_name: str) -> List[RegexMatch]:
        matches = match_all(self.regex, chemical_name)
        return [m for m in matches if self._is_valid(m, chemical_name)]

    def _is_valid(self, match: RegexMatch, chemical_name: str) -> bool:
        """
        The regex matching in 'find_matches' is a bit too generous.
        This function checks whether the match should be kept.
        """
        # if "(s)" is followed by a dash, it probably refers to the chirality -> ignore it
        if match.text == '(s)':
            next_char_index = match.span.stop
            try:
                if chemical_name[next_char_index] in dash_characters:
                    return False
            except IndexError:
                pass

        return True
