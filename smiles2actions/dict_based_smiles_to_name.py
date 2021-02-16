from typing import Dict

from .smiles_to_name import SmilesToName, SmilesToNameError


class DictBasedSmilesToName(SmilesToName):
    """
    SmilesToName based on a provided dictionary.
    """

    def __init__(self, mapping: Dict[str, str]):
        self.mapping = mapping

    def get_name(self, smiles: str) -> str:
        try:
            return self.mapping[smiles]
        except KeyError as e:
            raise SmilesToNameError(smiles) from e
