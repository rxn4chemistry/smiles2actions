import re
from typing import List

from .filter import Filter
from ..regex_utils import RegexMatch, match_all, alternation, optional

_optional_half_or_semi = optional(alternation(['half', 'semi']) + '[- ]?')

_saturated_descriptors = [
    'sature?(?:at)?ed?',  # saturated, satured, saturate, satureated, sature
    r'sat\.?[\'′]?d',  # satd, sat'd, sat′d
    r'sat\.',
    r'sat\b',
]

_concentrated_descriptors = [
    'concentrated',
    r'concd\.?',
    r'conc\.',
    r'conc\b',
]

_saturated_regex = _optional_half_or_semi + alternation(_saturated_descriptors)
_concentrated_regex = _optional_half_or_semi + alternation(_concentrated_descriptors)

_other_descriptors = [
    # dilute
    '(?:un)?diluted?',
    r'dil\.',
    r'\bdil\b',

    # aqueous
    'aqueous',
    'aqeuous',
    'aqeous',
    'aqueos',
    'aquous',
    r'aqu?\.',
    r'aq\b',
]


class SolutionDescriptorFilter(Filter):
    """
    Looks for adjectives related to solutions.
    """

    def __init__(self):
        regex_string = alternation(_other_descriptors + [_saturated_regex, _concentrated_regex])
        self.regex = re.compile(regex_string, re.IGNORECASE)

    def find_matches(self, chemical_name: str) -> List[RegexMatch]:
        matches = match_all(self.regex, chemical_name)
        return matches
