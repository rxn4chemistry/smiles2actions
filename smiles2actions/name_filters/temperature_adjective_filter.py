import re
from typing import List

from .filter import Filter
from ..regex_utils import RegexMatch, match_all, alternation, optional

temperature_adjectives = [
    'boiling',
    'cold',
    'glacial',
    r'\bhot\b',
    r'\biced',
    'ice cold',
    'ice-cold',
]


class TemperatureAdjectiveFilter(Filter):
    """
    Looks for adjectives related to the temperature.
    """

    def __init__(self):
        temperature_in_parentheses = r'\(.*°.*\)'
        optional_suffix = optional(f' {temperature_in_parentheses}')
        regex_string = alternation(temperature_adjectives) + optional_suffix
        self.regex = re.compile(regex_string, re.IGNORECASE)

    def find_matches(self, chemical_name: str) -> List[RegexMatch]:
        return match_all(self.regex, chemical_name)
