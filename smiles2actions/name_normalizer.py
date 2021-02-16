import re
from typing import Callable, List

from .regex_utils import alternation
from .utils import dash_characters


class NameNormalizer:
    """
    Normalizes chemical names by performing a different kinds of substitutions.

    This reduces the slight variations in compound names:
    - character used for prime / dash
    - uppercase / lowercase
    - etc
    """

    def __init__(
        self,
        normalize_subscripts: bool = False,
        normalize_case: bool = False,
        normalize_dashes: bool = False,
        normalize_primes: bool = False,
        normalize_greek_letters: bool = False,
        normalize_potential_ocr_errors: bool = False,
        remove_spaces: bool = False,
        remove_dashes: bool = False,
        remove_primes: bool = False,
        remove_special_characters: bool = False
    ):
        """
        Args:
            normalize_subscripts: converts subscript digits to normal digits
            normalize_case: converts letters to lowercase
            normalize_dashes: replaces all kinds of dashes by a simple hyphen. Not necessary if remove_dashes=True
            normalize_primes: replaces all kinds of primes by a simple apostrophe. Not necessary if remove_primes=True
            normalize_greek_letters: replaces 'alpha', 'beta', etc., by 'α', 'β', etc.
            normalize_potential_ocr_errors: avoids confusion with 0/O, 1/I/l, etc
            remove_spaces: removes spaces
            remove_dashes: removes all kinds of dashes
            remove_primes: removes all kinds of primes
            remove_special_characters: removes other special characters
        """

        self.normalization_fns: List[Callable[[str], str]] = []
        self.subscript_digitmap = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
        self.dash_regex = re.compile(alternation(dash_characters))
        self.default_dash_character = '-'
        self.prime_regex = re.compile(alternation(['\'', 'ʹ', '′', '’', '″', 'ʺ']))
        self.default_prime_character = '\''
        self.special_character_regex = re.compile(
            alternation([c for c in '±↑⊐×°□®™●•·⋅˙\u200C'] + [r'\*'])
        )

        if normalize_subscripts:
            self.normalization_fns.append(self.normalize_subscripts)

        if normalize_potential_ocr_errors:
            self.normalization_fns.append(self.normalize_potential_ocr_errors)

        if normalize_case:
            self.normalization_fns.append(self.normalize_case)

        if normalize_dashes:
            self.normalization_fns.append(self.normalize_dashes)

        if normalize_primes:
            self.normalization_fns.append(self.normalize_primes)

        if normalize_greek_letters:
            self.normalization_fns.append(self.normalize_greek_letters)

        if remove_spaces:
            self.normalization_fns.append(self.remove_spaces)

        if remove_dashes:
            self.normalization_fns.append(self.remove_dashes)

        if remove_primes:
            self.normalization_fns.append(self.remove_primes)

        if remove_special_characters:
            self.normalization_fns.append(self.remove_special_characters)

    def __call__(self, name: str) -> str:
        return self.normalize(name)

    def normalize(self, name: str) -> str:
        for fn in self.normalization_fns:
            name = fn(name)
        return name

    def normalize_subscripts(self, name: str) -> str:
        return name.translate(self.subscript_digitmap)

    def normalize_case(self, name: str) -> str:
        return name.lower()

    def normalize_dashes(self, name: str) -> str:
        return self.dash_regex.sub(self.default_dash_character, name)

    def normalize_primes(self, name: str) -> str:
        return self.prime_regex.sub(self.default_prime_character, name)

    def normalize_greek_letters(self, name: str) -> str:
        name = re.sub(r'\balpha\b', 'α', name)
        name = re.sub(r'\bbeta\b', 'β', name)
        name = re.sub(r'\bgamma\b', 'γ', name)
        return name

    def normalize_potential_ocr_errors(self, name: str) -> str:
        name = name.replace('I', 'l')
        name = name.replace('1', 'l')
        name = name.replace('0', 'O')
        return name

    def remove_spaces(self, name: str) -> str:
        return name.replace(' ', '')

    def remove_dashes(self, name: str) -> str:
        return self.dash_regex.sub('', name)

    def remove_primes(self, name: str) -> str:
        return self.prime_regex.sub('', name)

    def remove_special_characters(self, name: str) -> str:
        return self.special_character_regex.sub('', name)

    @classmethod
    def default_normalizer(cls) -> 'NameNormalizer':
        # Normalizes everything
        return NameNormalizer(
            normalize_subscripts=True,
            normalize_case=True,
            normalize_dashes=False,
            normalize_primes=False,
            normalize_greek_letters=True,
            normalize_potential_ocr_errors=True,
            remove_spaces=True,
            remove_dashes=True,
            remove_primes=True,
            remove_special_characters=True
        )
