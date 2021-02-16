import math
from typing import Optional, List

from pint import Quantity

from .quantities_utils import get_unit_registry
from .quantity_binner import QuantityBinner
from .quantity_binning_limits import BinningInterval, QuantityBinningLimits
from .temperature_extractor import TemperatureExtractor
from ..placeholder_handler import PlaceholderHandler

u = get_unit_registry()
Q_ = u.Quantity

default_intervals = [
    BinningInterval(Q_(-math.inf, u.degC), Q_(-50, u.degC), Q_(-70, u.degC)),
    BinningInterval(Q_(-50, u.degC), Q_(-10, u.degC), Q_(-30, u.degC)),
    BinningInterval(Q_(-10, u.degC), Q_(+10, u.degC), Q_(+00, u.degC)),
    BinningInterval(Q_(+10, u.degC), Q_(+40, u.degC), Q_(+25, u.degC)),
    BinningInterval(Q_(+40, u.degC), Q_(+80, u.degC), Q_(+60, u.degC)),
    BinningInterval(Q_(+80, u.degC), Q_(+math.inf, u.degC), Q_(+100, u.degC)),
]


class TemperaturePlaceholder:
    """
    Handles the conversion to and from temperature placeholders.
    """

    def __init__(self, intervals: Optional[List[BinningInterval]] = None):
        """
        Args:
            intervals: intervals for binning. Defaults to default_intervals.
        """
        if intervals is None:
            intervals = default_intervals

        self.limits = QuantityBinningLimits(intervals)
        self.temperature_extractor = TemperatureExtractor()
        self.quantity_binner = QuantityBinner(self.limits.get_boundaries())
        self.placeholder_handler = PlaceholderHandler.for_temperatures()

    def to_placeholder(self, temperature: str) -> str:
        quantity = self.temperature_extractor.extract_temperature(temperature)
        return self.quantity_to_placeholder(quantity.value)

    def quantity_to_placeholder(self, quantity: Quantity) -> str:
        bin_index = self.quantity_binner.get_bin_index(quantity)
        return self.placeholder_handler.to_placeholder(bin_index + 1)
