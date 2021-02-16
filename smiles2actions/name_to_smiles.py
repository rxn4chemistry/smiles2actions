from abc import ABC, abstractmethod


class NameToSmilesError(ValueError):

    def __init__(self, name: str):
        super().__init__(f'No SMILES string can be determined for "{name}".')


class NameToSmiles(ABC):
    """
    Interface for converting compound names to SMILES strings.
    """

    @abstractmethod
    def get_smiles(self, name: str) -> str:
        """
        Get the SMILES string corresponding to a given name.

        Args:
            name: compound name.

        Raises:
            NameToSmilesError if no SMILES string can be determined.

        Returns:
            SMILES string corresponding to the given name.
        """

    def has_smiles(self, name: str) -> bool:
        """
        Whether a name has a corresponding SMILES.

        The base class implementation calls get_smiles and catches the
        potential exception to determine this.
        Derived classes can override this behavior if needed.

        Args:
            name: compound name.

        Returns:
            Whether a SMILES string is available.
        """
        try:
            self.get_smiles(name)
            return True
        except NameToSmilesError:
            return False
