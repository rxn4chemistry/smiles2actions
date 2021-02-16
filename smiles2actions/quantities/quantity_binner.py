from typing import List, Optional

import numpy as np
from pint import Quantity

from paragraph2actions.utils import all_identical


class BinningError(ValueError):
    """Exception raised for binning errors"""

    def __init__(self, text: str):
        super().__init__(text)


class QuantityBinner:
    """
    Convert quantities to bins.
    """

    def __init__(self, bin_boundaries: List[Quantity], bin_names: Optional[List[str]] = None):
        """
        Args:
            bin_boundaries: List of bin boundaries
            bin_names: names of the bins, defaults to "bin_0", "bin_1", etc.
        """
        assert len(bin_boundaries) > 0

        if bin_names is None:
            bin_names = ['bin_' + str(i) for i in range(len(bin_boundaries) + 1)]
        self.bin_names = bin_names

        if len(bin_names) != len(bin_boundaries) + 1:
            raise ValueError('Number of bin names is incompatible with number of bin boundaries')

        dimensionalities = [b.dimensionality for b in bin_boundaries]
        if not all_identical(dimensionalities):
            raise ValueError('The bin boundaries have different dimensionalities')

        self.dimensionality = dimensionalities[0]
        self.bin_boundaries = bin_boundaries
        self.unitless_bin_boundaries = [b.to_base_units().magnitude for b in bin_boundaries]

    def get_bin_index(self, quantity: Quantity) -> int:
        return self.digitize(quantity=quantity)

    def get_bin_name(self, quantity: Quantity) -> str:
        return self.bin_names[self.get_bin_index(quantity)]

    def digitize(self, quantity: Quantity) -> int:
        """
        Does the same as numpy.digitize, which is not compatible with pint.Quantity
        """
        if quantity.dimensionality != self.dimensionality:
            raise BinningError('Incompatible dimensionality')

        value = quantity.to_base_units().magnitude
        return int(np.digitize(value, self.unitless_bin_boundaries))
