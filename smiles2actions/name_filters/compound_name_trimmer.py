import re

from ..regex_utils import alternation, optional
from ..utils import remove_prefix, remove_postfix, dash_characters

_to_remove_in_empty_parenthesis = optional(alternation([',', r'\.']))
_empty_parenthesis_regex = rf'\( *{_to_remove_in_empty_parenthesis} *\)'

_equivalent_to_empty = [')', '(', '.', ',']
_noise_characters = [' ', ',', '.', ','] + dash_characters


class CompoundNameTrimmer:
    """
    Removes noise from compound names that substrings have been removed from.

    For instance, if the original string 'ice-cold NaCl (1M)' was post-processed to ' NaCl ()',
    the present class cleans it up to obtain 'NaCl'.
    """

    def trim(self, compound_name: str) -> str:
        """
        Cleans up the name iteratively
        """
        previous = ''
        while compound_name != previous:
            previous = compound_name
            compound_name = self._cleanup_iteration(compound_name)
        return compound_name.strip()

    def _cleanup_iteration(self, name: str) -> str:
        # remove trailing spaces
        name = name.strip(''.join(_noise_characters))

        # replace multiple spaces by a single one
        name = re.sub(r'  +', ' ', name)

        # remove empty parentheses
        name = re.sub(_empty_parenthesis_regex, '', name)

        # parenthesis sign at beginning or end of name in incorrect direction
        name = remove_prefix(name, ')')
        name = remove_postfix(name, '(')

        # remove lonely "of" at the beginning
        name = remove_prefix(name, 'of')
        name = remove_prefix(name, 'Of')

        # parenthesis character at beginning or end of name, with no matching parenthesis character
        if name.endswith(')') and '(' not in name:
            name = remove_postfix(name, ')')
        if name.startswith('(') and ')' not in name:
            name = remove_prefix(name, '(')

        if name in _equivalent_to_empty:
            return ''

        return name
