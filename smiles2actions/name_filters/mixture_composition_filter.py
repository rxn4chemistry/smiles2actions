import re
from typing import List

from .filter import Filter
from ..regex_utils import RegexMatch, match_all, alternation


class MixtureCompositionFilter(Filter):
    """
    Finds composition specifications in compound names.

    Such strings are often given for mixtures of compounds and give the composition as a fraction / proportions.
    """

    def __init__(self):
        number_regex = r'\d+'
        separator = alternation(['/', ':'])

        regex_string_without_parenthesis = fr'{number_regex}(?:{separator}{number_regex})+'
        regex_string_with_parenthesis = fr'\({regex_string_without_parenthesis}\)'
        regex_string = alternation(
            [regex_string_with_parenthesis, regex_string_without_parenthesis]
        )

        self.regex = re.compile(regex_string)

    def find_matches(self, chemical_name: str) -> List[RegexMatch]:
        return match_all(self.regex, chemical_name)
