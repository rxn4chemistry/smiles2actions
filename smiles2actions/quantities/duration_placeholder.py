import math
from typing import Optional, List

from pint import Quantity

from .duration_extractor import DurationExtractor
from .quantities_utils import get_unit_registry
from .quantity_binner import QuantityBinner
from .quantity_binning_limits import BinningInterval, QuantityBinningLimits
from ..placeholder_handler import PlaceholderHandler

u = get_unit_registry()
Q_ = u.Quantity

default_intervals = [
    BinningInterval(Q_(0, u.minute), Q_(30, u.minute), Q_(10, u.minute)),
    BinningInterval(Q_(30, u.minute), Q_(3, u.hour), Q_(1, u.hour)),
    BinningInterval(Q_(3, u.hour), Q_(10, u.hour), Q_(8, u.hour)),
    BinningInterval(Q_(10, u.hour), Q_(50, u.hour), Q_(1, u.day)),
    BinningInterval(Q_(50, u.hour), Q_(math.inf, u.hour), Q_(7, u.day)),
]


class DurationPlaceholder:
    """
    Handles the conversion to and from duration placeholders.
    """

    def __init__(self, intervals: Optional[List[BinningInterval]] = None):
        """
        Args:
            intervals: intervals for binning. Defaults to default_intervals.
        """
        if intervals is None:
            intervals = default_intervals

        self.limits = QuantityBinningLimits(intervals)
        self.duration_extractor = DurationExtractor()
        self.quantity_binner = QuantityBinner(self.limits.get_boundaries())
        self.placeholder_handler = PlaceholderHandler.for_durations()

    def to_placeholder(self, duration: str) -> str:
        quantity = self.duration_extractor.extract_duration(duration)
        return self.quantity_to_placeholder(quantity.value)

    def quantity_to_placeholder(self, quantity: Quantity) -> str:
        bin_index = self.quantity_binner.get_bin_index(quantity)
        return self.placeholder_handler.to_placeholder(bin_index + 1)
