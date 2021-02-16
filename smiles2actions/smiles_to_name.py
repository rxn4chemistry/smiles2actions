from abc import ABC, abstractmethod


class SmilesToNameError(ValueError):

    def __init__(self, smiles: str):
        super().__init__(f'No name can be determined for the SMILES string "{smiles}".')


class SmilesToName(ABC):
    """
    Interface for converting SMILES strings to compound names.
    """

    @abstractmethod
    def get_name(self, smiles: str) -> str:
        """
        Get the name corresponding to a given SMILES string.

        Args:
            smiles: SMILES string.

        Raises:
            SmilesToNameError if no name can be determined.

        Returns:
            Name corresponding to the given SMILES string.
        """

    def has_name(self, smiles: str) -> bool:
        """
        Whether a SMILES string has a corresponding name.

        The base class implementation calls get_name and catches the
        potential exception to determine this.
        Derived classes can override this behavior if needed.

        Args:
            smiles: SMILES string.

        Returns:
            Whether a name is available for the given SMILES string.
        """
        try:
            self.get_name(smiles)
            return True
        except SmilesToNameError:
            return False
