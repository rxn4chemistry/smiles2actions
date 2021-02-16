import re
from typing import List

from .filter import Filter
from ..regex_utils import RegexMatch, match_all, alternation

_descriptors = [
    r'\ba\b',  # article 'a'
    r'[Ee]nough',
    r'[Aa]bout',
    r'containing',
]


class DiverseFilter(Filter):
    """
    Looks for remaining words to filter out (that have not been extracted by the other Filter classes).
    """

    def __init__(self):
        regex_string = alternation(_descriptors)
        self.regex = re.compile(regex_string)

    def find_matches(self, chemical_name: str) -> List[RegexMatch]:
        return match_all(self.regex, chemical_name)
