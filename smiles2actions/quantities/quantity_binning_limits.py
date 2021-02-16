import math
from typing import List

import attr
from paragraph2actions.utils import all_identical, pairwise
from pint import Quantity


@attr.s(auto_attribs=True)
class BinningInterval:
    """Holds a binning interval and the value to replace it by."""
    start: Quantity
    end: Quantity
    substitute: Quantity


class QuantityBinningLimits:
    """
    Holds the information about how a quantity space is binned and how it is
    to be unbinned.
    """

    def __init__(self, intervals: List[BinningInterval]):
        self.validate(intervals)
        self.intervals = intervals

    def validate(self, intervals: List[BinningInterval]) -> None:
        """Checks that the given intervals cover the space correctly.

        Raises:
             ValueError if the given intervals are invalid.
        """

        # Verify dimensions
        all_values = (
            [interval.start for interval in intervals] + [interval.end for interval in intervals] +
            [interval.substitute for interval in intervals]
        )
        dimensionalities = [b.dimensionality for b in all_values]
        if not all_identical(dimensionalities):
            raise ValueError('The interval limits have different dimensionalities')

        # Verify first value
        first_value = intervals[0].start.magnitude
        if first_value != -math.inf and first_value != 0.0:
            raise ValueError(
                f'First interval starts at {first_value} instead '
                f'of 0.0 or minus infinity.'
            )

        # Verify last value
        last_value = intervals[-1].end.magnitude
        if last_value != math.inf:
            raise ValueError(f'Last interval ends at {last_value} instead ' f'of infinity.')

        # Verify intersections
        for a, b in pairwise(intervals):
            if a.end != b.start:
                raise ValueError(
                    f'Adjacent intervals should end and start at '
                    f'the same value; {a} != {b}'
                )

        # Verify order of intervals, and substitute is in interval
        for interval in intervals:
            if not (interval.start <= interval.substitute <= interval.end):
                raise ValueError('Intervals not in order, or substitute not ' 'in interval.')

    def get_boundaries(self) -> List[Quantity]:
        boundaries = [interval.end for interval in self.intervals]
        # remove last one
        return boundaries[:-1]
