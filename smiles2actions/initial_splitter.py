from typing import List


class InitialSplitter:
    """
    Splits a string into one or several strings, each of which is potentially containing a distinct chemical.

    This happens at the very beginning of the processing of compound names, hence the name InitialSplitter.
    """

    def __init__(self):
        self.simple_separators = [
            ' solution of ',
            ' salt of ',
            ' dispersion of ',
        ]
        self.compound_adjectives = [
            ('Methanolic', 'Methanol'),
            ('methanolic', 'methanol'),
            ('Ethanolic', 'Ethanol'),
            ('ethanolic', 'ethanol'),
            ('Ethereal', 'Ether'),
            ('ethereal', 'ether'),
        ]

    def split(self, name: str) -> List[str]:
        splits = [name]
        splits = self._process_simple_separators(splits)
        splits = self._process_adjectives(splits)
        return splits

    def _process_simple_separators(self, parts: List[str]) -> List[str]:
        # Consider each separator one after the other
        for separator in self.simple_separators:
            # Iterate through the current splits, and replace by new ones if a match is found
            for i, part in reversed(list(enumerate(parts))):
                splits = part.split(separator)
                if len(splits) == 2:
                    parts[i:i + 1] = [
                        splits[0],
                        splits[1],
                    ]
        return parts

    def _process_adjectives(self, parts: List[str]) -> List[str]:
        # Consider each separator one after the other
        for adj, compound in self.compound_adjectives:
            # Iterate through the current splits, and, if a match is found, split and replace the adjective
            # by the compound name
            for i, part in reversed(list(enumerate(parts))):
                splits = part.split(f'{adj} ')
                if len(splits) == 2:
                    parts[i:i + 1] = [
                        splits[0] + compound,
                        splits[1],
                    ]
            # if the adjective was at the end of a string there was no split, but we still need to replace it
            for i, part in enumerate(parts):
                if adj in part:
                    parts[i] = part.replace(adj, compound)
        return parts
