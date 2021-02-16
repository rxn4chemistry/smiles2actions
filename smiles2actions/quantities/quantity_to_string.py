from pint import Quantity

from .quantities_utils import get_unit_registry

u = get_unit_registry()


class QuantityToString:
    """
    Class for the conversion of pint.Quantity to strings.

    The functions forward the pint.errors.DimensionalityError when the units
    are incorrect.
    """

    @staticmethod
    def to_celsius(quantity: Quantity) -> str:
        magnitude = quantity.to(u.degC).magnitude
        return f'{magnitude} °C'

    @staticmethod
    def to_seconds(quantity: Quantity) -> str:
        magnitude = quantity.to(u.seconds).magnitude
        return f'{magnitude} s'
