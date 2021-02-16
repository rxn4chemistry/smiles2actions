from typing import List, Generator, Set, Tuple

from .core_name_extractor import CoreNameExtractor
from .initial_splitter import InitialSplitter


class NameSimplifier:
    """
    This class simplifies a compound name iteratively.

    Simplifying a compound name is not trivial because of the many ways it can be formulated in. To give a
    few examples, it could be one of:
     - "sodium chloride"
     - "1M sodium chloride in water"
     - "20% w/w aqueous solution of sodium chloride"
     - "sodium chloride-ammonia"
     - "saturated sodium chloride/ammonia (1/1)"
     - etc.

    To get information out of it (f.i. SMILES string), it is best to try subsequent simplifications of the compound
    name, and check every time if the current name is found (f.i. in a SMILES database).

    This class can produce an iterator over compound names that are simplified more and more, whereby the
    risk of oversimplification increases at every step.
    """

    def __init__(self):
        self.initial_splitter = InitialSplitter()
        self.core_name_extractor = CoreNameExtractor()

    def simplify(self, name: str) -> Generator[List[str], None, None]:
        """
        Returns iterator over simplifications of a given name, without duplication.

        The iterator is over a list of strings, since the original compound name may contain several
        different compounds.
        """

        seen: Set[Tuple[str, ...]] = set()

        for simplified_name in self._simplify_with_potential_repetition(name):
            simplified_name = [name for name in simplified_name if name]
            # Only yield if the name has not been yielded before
            if tuple(simplified_name) not in seen:
                seen.add(tuple(simplified_name))
                yield simplified_name

    def _simplify_with_potential_repetition(self, name: str) -> Generator[List[str], None, None]:
        # original name
        yield [name]

        # name after initial splitting
        initial_splits = self.initial_splitter.split(name)
        yield initial_splits

        # strip each one of them
        stripped_names = [self.core_name_extractor.strip_compound(n) for n in initial_splits]
        yield stripped_names

        # Try to split them
        stripped_compound_splits = [
            split for stripped_name in stripped_names
            for split in self.core_name_extractor.split_stripped_compound(stripped_name)
        ]
        yield stripped_compound_splits
