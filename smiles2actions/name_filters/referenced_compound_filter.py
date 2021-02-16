import itertools
import re
from typing import List

from .filter import Filter
from ..regex_utils import RegexMatch, match_all, alternation, optional, capturing
from ..utils import dash_characters


class ReferencedCompoundFilter(Filter):
    """Finds references to patent compounds in chemical names"""

    def __init__(self):
        # admissible subcomponent, f.i. 123, a, A, VII are admissible, but 123-AB is not in this context.
        number = r'\d+'
        single_letter = r'[a-zA-Z]'
        roman_number = r'[IVXL]+'  # 1, 5, 10, 50
        single_components = [number, single_letter, roman_number]

        # Combination of two subcomponents of different types
        permutation_tuples = list(itertools.permutations(single_components, 2))
        component_pairs = [f'{t[0]}{t[1]}' for t in permutation_tuples]
        self.one_or_two_components = alternation(single_components + component_pairs)

        # Combination of two groups of one or two subcomponents separated by a delimiter
        separator = alternation([r'\.', ' '] + dash_characters)
        self.one_or_two_groups = f'{self.one_or_two_components}{optional(separator + self.one_or_two_components)}'

    def find_matches(self, chemical_name: str) -> List[RegexMatch]:
        matches = self._find_impl(f' {chemical_name}')
        # remove the space at the beginning of the match, but account for the additional space introduced
        matches = [
            RegexMatch(span=slice(m.span.start, m.span.stop - 1), text=m.text.strip())
            for m in matches
        ]
        matches = [m for m in matches if not self._is_exception(m.text)]
        return matches

    def _find_impl(self, name: str) -> List[RegexMatch]:
        # combination of two with separator
        matches = match_all(rf' {self.one_or_two_groups}$', name)
        if matches:
            return matches

        # simple match of one or two components, with optional hash
        matches = match_all(rf' #?{self.one_or_two_components}$', name)
        if matches:
            return matches

        # combination of two with with parenthesis or bracket
        matches = match_all(rf' [\(\[] ?{self.one_or_two_groups} ?[\)\]]$', name)
        if matches:
            return matches

        return []

    def _is_exception(self, s: str) -> bool:
        # check for oxidation numbers in parentheses
        parenthesis_regex = rf'\({capturing(".*")}\)'
        roman_number_match = re.match(rf'^{parenthesis_regex}$', s)
        if roman_number_match is not None:
            content = roman_number_match.group(1)
            if content in ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']:
                return True

        return False
