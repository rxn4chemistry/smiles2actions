from pint import Quantity

from .quantities_utils import get_unit_registry
from .quantity import RxnQuantity
from .value_unit_entity import get_vue, VUEParseError, VUE

u = get_unit_registry()


class TemperatureExtractionError(ValueError):

    def __init__(self, temperature: str):
        super().__init__(f'Conversion of temperature failed for "{temperature}".')


class TemperatureExtractor:

    def extract_temperature(self, temperature: str) -> RxnQuantity:
        try:
            vue = get_vue(temperature)
            return RxnQuantity(Quantity(temperature_to_float(temperature, vue), u.degC))
        except VUEParseError as e:
            raise TemperatureExtractionError(temperature) from e


def fahrenheit_to_celsius(temperature_in_fahrenheit: float) -> float:
    return (temperature_in_fahrenheit - 32) * 5 / 9


def temperature_to_float(temperature: str, vue: VUE) -> float:
    if vue.e not in ["temperature", "charge", "capacitance", "angle"]:
        raise TemperatureExtractionError(temperature)

    if vue.u == "degree_Celsius" or vue.u == "coulomb":
        return float(vue.v)

    if vue.u == "degree_fahrenheit" or vue.u == "farad":
        return fahrenheit_to_celsius(float(vue.v))

    if vue.u == "kelvin":
        return float(vue.v) - 273.15

    if vue.u == "degree_angle":
        # usually when there is a space between the degree symbol and "C" or "F"
        if temperature.endswith('C'):
            return float(vue.v)
        if temperature.endswith('F'):
            return fahrenheit_to_celsius(float(vue.v))
        # otherwise, we assume it was Celsius
        return float(vue.v)

    raise TemperatureExtractionError(temperature)
