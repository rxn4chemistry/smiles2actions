import re
from typing import List

from .filter import Filter
from ..regex_utils import RegexMatch, match_all, alternation, optional

_descriptors = [
    # distilled
    'distilled',
    'distd',
    r'dist\.',
    r'dist\b',

    # denatured
    'denatured',
    r'denat\.',

    # deionized
    'de-?ionized',
    'de-?ioned',

    # absolute
    'absolute',
    r'abs\.',

    # crude
    'crude',

    # anhydrous
    'anhydrous',
    r'anhyd\.',
    r'anhyd\b',
    r'anh\.',
    r'anh\b',

    # pure / purified
    f'{optional("un")}purified',
    rf'\b{optional("im")}pure\b',

    # fuming
    'fuming',
]

_dry_descriptors = [
    # dry
    r'\S+-dried',
    'predried',
    r'\bdried',
    r'\bdry\b',
]


class MaterialDescriptorFilter(Filter):
    """
    Finds descriptions/properties of a material in compound names.
    """

    def __init__(self):
        self.regex = re.compile(alternation(_descriptors), re.IGNORECASE)
        self.dry_regex = re.compile(alternation(_dry_descriptors), re.IGNORECASE)
        self.dry_ice_regex = re.compile(r'dry[- ]?ice', re.IGNORECASE)

    def find_matches(self, chemical_name: str) -> List[RegexMatch]:
        matches = match_all(self.regex, chemical_name)
        matches.extend(self.match_dry(chemical_name))
        return matches

    def match_dry(self, chemical_name: str) -> List[RegexMatch]:
        """'dry' is handled differently, because we don't want to catch 'dry ice'"""
        if self.dry_ice_regex.search(chemical_name) is not None:
            return []

        return match_all(self.dry_regex, chemical_name)
