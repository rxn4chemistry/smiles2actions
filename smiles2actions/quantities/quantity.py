import attr
from pint.quantity import Quantity


@attr.s(auto_attribs=True)
class RxnQuantity:
    """
    Physical quantity (temperature, duration, etc.).

    Currently, it is nothing more than a wrapper for the Quantity class
    defined in the Pint library.
    It can, however, be extended in the future to support ranges (between x
    and y) or other information (standard deviation, greater than, etc.).
    """
    value: Quantity

    def __attrs_post_init__(self) -> None:
        # Workaround for the Pint bug with unit comparison (https://github.com/hgrecco/pint/issues/1079)
        self.value.ito_base_units()
