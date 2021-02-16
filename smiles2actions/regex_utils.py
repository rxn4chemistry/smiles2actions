import re
from typing import Union, Pattern, List, Iterable

import attr

integer_number_regex = r'[+-]?[0-9]+'
real_number_regex = r'[+-]?[0-9]+(?:\.[0-9]+)?'


def capturing(initial_regex: str) -> str:
    """Add capturing parentheses to a regex string"""
    return f'({initial_regex})'


def alternation(choices: Iterable[str], capture_group=False) -> str:
    """OR operator"""

    inner_string = '|'.join(choices)

    if capture_group:
        return f'({inner_string})'
    else:
        return f'(?:{inner_string})'


def optional(initial_regex: str, capture_group=False) -> str:
    """Creates the regex string to make a group optional"""
    if capture_group:
        return f'({initial_regex})?'
    else:
        return f'(?:{initial_regex})?'


@attr.s(auto_attribs=True)
class RegexMatch:
    span: slice
    text: str


def match_all(regex: Union[str, Pattern], text: str, flags=0) -> List[RegexMatch]:
    """
    Similar to re.findall(), but it will not only return strings, but also their spans.

    When there are capturing groups, will still return the full matching string, irrespective of the capture group.
    """

    return [
        RegexMatch(span=slice(*match.span()), text=match.group(0))
        for match in re.finditer(regex, text, flags=flags)
    ]
