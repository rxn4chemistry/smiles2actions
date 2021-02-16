from typing import Optional, List

from pint import Quantity

from .quantities_utils import get_unit_registry
from .quantity_binner import QuantityBinner, BinningError
from .value_unit_entity import dimensionless_value_from_quantulum

u = get_unit_registry()


class PHBinner:
    """
    Binner for pH values.
    Currently returns one of three bins: acidic (0), neutral (1), basic (2).

    The pH values usually are given as strings representing numbers or stating 'acidic', 'basic', 'neutral'
    """

    def __init__(
        self,
        bin_boundaries: Optional[List[float]] = None,
        ph_for_acidic: float = 3.0,
        ph_for_basic: float = 11.0,
        ph_for_neutral: float = 7.0
    ):
        """
        Args:
            bin_boundaries: defaults to [6.5, 7.5] (i.e. 3 bins with limits at 6.5 and 7.5).
            ph_for_acidic: pH value to convert the adjective "acidic" to
            ph_for_basic: pH value to convert the adjective "basic" to
            ph_for_neutral: pH value to convert the adjective "neutral" to
        """
        if bin_boundaries is None:
            bin_boundaries = [6.5, 7.5]

        self.quantity_binner = QuantityBinner(
            [Quantity(v, u.dimensionless) for v in bin_boundaries]
        )

        self.conversions = {
            'acidic': ph_for_acidic,
            'basic': ph_for_basic,
            'neutral': ph_for_neutral,
        }

    def get_bin(self, quantity: str) -> int:
        try:
            ph_value = self.string_to_ph(quantity)
            return self.quantity_binner.get_bin_index(Quantity(ph_value, u.dimensionless))
        except ValueError as e:
            raise BinningError(quantity) from e

    def string_to_ph(self, quantity: str) -> float:
        if quantity in self.conversions:
            return self.conversions[quantity]

        return dimensionless_value_from_quantulum(quantity)
