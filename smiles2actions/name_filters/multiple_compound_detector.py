import re
from typing import List, Tuple, Pattern

from .compound_name_trimmer import CompoundNameTrimmer
from ..regex_utils import alternation
from ..utils import dash_characters


class MultipleCompoundDetector:
    """
    This class splits a compound name in several parts, that may each be a different compound.

    In its implementation, this class keeps track of indices where to split the compound names, which
    are saved as slice objects.

    This class applies a cleanup after splitting.
    """

    def __init__(self):
        self.delimiters_regex = self._compute_delimiters_regex()
        self.left_exceptions_regex = self._compute_left_exceptions_regex()
        self.right_exceptions_regex = self._compute_right_exceptions_regex()
        self.appended_parenthesis_regex = self._compute_appended_parenthesis_regex()

        self.trimmer = CompoundNameTrimmer()

    def get_candidates(self, compound_name: str) -> List[str]:
        splits = self._slices_for_appended_parentheses(
            compound_name
        ) + self._slices_for_delimiters(compound_name)
        splits.sort()

        splits = self._filter_out_slices(splits, compound_name)
        return self._subcompounds_from_splits(compound_name, splits)

    def _filter_out_slices(self, slices: List[slice], name: str) -> List[slice]:
        """
        Iteratively removes splits that are not needed.
        """
        slices = list(slices)  # copy to avoid overwriting the original list
        current_number_slices = 0

        while len(slices) != current_number_slices:
            current_number_slices = len(slices)
            slices_and_neighbors = self._slice_and_neighbors_for_split(name, slices)
            for s, left, right in slices_and_neighbors:
                separator = name[s]
                if not self.keep_split(separator, left, right):
                    slices.remove(s)
                    break
        return slices

    def keep_split(self, separator: str, left: str, right: str) -> bool:
        """
        Checks whether a split must be kept or not.
        """
        if left == '' or right == '':
            return False
        if self._is_likely_part_of_compound_name(left=left, right=right, separator=separator):
            return False
        if self._is_exception(separator=separator, left=left, right=right):
            return False
        return True

    def _subcompounds_from_splits(self, name: str, splits: List[slice]) -> List[str]:
        if not splits:
            return [name]

        # Define slices for parts of the name that are in between our splits (which are also given as slices)
        parts = [slice(i.stop, j.start) for i, j in zip(splits, splits[1:])]

        # Add first and last parts for the name
        parts = [slice(0, splits[0].start)] + parts + [slice(splits[-1].stop, len(name))]

        # convert slices to strings
        components = [name[p] for p in parts]

        # apply cleanup
        return [self.trimmer.trim(c) for c in components]

    def _slice_and_neighbors_for_split(self, name: str,
                                       splits: List[slice]) -> List[Tuple[slice, str, str]]:
        components = self._subcompounds_from_splits(name, splits)

        # there is always one component more than there are splits, we just need to link them
        return [(splits[i], components[i], components[i + 1]) for i in range(len(splits))]

    def _slices_for_appended_parentheses(self, name: str) -> List[slice]:
        """
        Often, the solvent in which something is solved is added as a parenthesis, such as "HCl (THF)"
        This function gets a delimiter slice corresponding to the opening and the closing parenthesis.
        """
        slices: List[slice] = []
        for m in self.appended_parenthesis_regex.finditer(name):
            # make sure that this is not an oxidation number
            in_parenthesis = m.group(1).strip()
            if in_parenthesis in ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']:
                continue

            start, end = m.span()
            slices += [slice(start + 1, start + 2), slice(end - 1, end)]
        return slices

    def _slices_for_delimiters(self, name: str) -> List[slice]:
        return [slice(*m.span()) for m in self.delimiters_regex.finditer(name)]

    def _is_likely_part_of_compound_name(self, left: str, right: str, separator: str) -> bool:
        """
        Follow a few heuristic rules to check whether the split is justified.

        For instance, the following are often part of chemical names:
            - tert-
            - 1H-
            - butyl-
            - ...
        """
        if separator not in dash_characters:
            return False

        if self.left_exceptions_regex.search(left) is not None:
            return True

        if self.right_exceptions_regex.search(right) is not None:
            return True

        return False

    def _is_exception(self, separator: str, left: str, right: str) -> bool:
        # Pd/C and Pt/C
        admissible_pd_c_separators = dash_characters + ['/']
        if left in ['Pd', 'Pt'] and right == 'C' and any(
            c in separator for c in admissible_pd_c_separators
        ):
            return True

        # dry-ice
        if left.endswith('dry') and right.startswith('ice'):
            return True

        return False

    def _compute_delimiters_regex(self) -> Pattern:
        remaining_delimiters = [
            '/', ':', r'\bin\b', ' and ', ' with ', ' salt of '
        ] + dash_characters
        return re.compile(alternation(remaining_delimiters))

    def _compute_left_exceptions_regex(self) -> Pattern:
        left_exceptions = [
            r'yl$',  # methyl, butyl
            r'[tT]ert$',  # tert
            r'[mM]eta$',  # meta
            r'[pP]ara$',  # para
            r'[dD]i$',  # di
            r'[aA]za$',  # aza
            r'[aA]lpha$',  # alpha
            r'[bB]eta$',  # beta
            r'ec$',  # sec
            r'[bBcC]is$',  # cis, bis
            r'[tT]rans$',  # trans
            r'[tT]ris?$',  # tri, tris
            r'o$',  # hydro, chloro, iodo, fluoro
            r'ox[ay]$',  # methoxy, dioxa
            r'\b.$',  # single character
            r'\d$',  # digit
            r'\)$',  # closing parenthesis
            r'\]$',  # closing bracket
            r'\d[Hab]$',  # 1H-XXX, 2a-XXX, 3b-XXX, etc
            r'[cC]bz$',  # Cbz
            r'[αβ]$',  # Greek letters
            alternation(['Boc', 'boc', 'BOC']),  # Boc
        ]
        return re.compile(alternation(left_exceptions))

    def _compute_right_exceptions_regex(self) -> Pattern:
        right_exceptions = [
            r'^\d',  # digit
            r'^.\b',  # single character
            r'^\(',  # opening parenthesis
            r'^\[',  # opening bracket
        ]
        return re.compile(alternation(right_exceptions))

    def _compute_appended_parenthesis_regex(self) -> Pattern:
        allowed_after_parenthesis = alternation(['$', ' ', '/'])
        return re.compile(fr' \((.*?)\){allowed_after_parenthesis}')
