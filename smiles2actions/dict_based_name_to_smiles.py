from typing import Dict, Callable, Optional

from .name_to_smiles import NameToSmiles, NameToSmilesError


class DictBasedNameToSmiles(NameToSmiles):
    """
    NameToSmiles based on a provided dictionary.
    """

    def __init__(
        self, mapping: Dict[str, str], normalize_fn: Optional[Callable[[str], str]] = None
    ):
        self.mapping = mapping
        self.normalize_fn = normalize_fn

        if self.normalize_fn is not None:
            self.mapping = {self.normalize_fn(key): value for key, value in self.mapping.items()}

    def get_smiles(self, name: str) -> str:
        try:
            if self.normalize_fn is not None:
                name = self.normalize_fn(name)
            return self.mapping[name]
        except KeyError as e:
            raise NameToSmilesError(name) from e
