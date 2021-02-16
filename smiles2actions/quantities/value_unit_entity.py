from typing import List, Optional

import attr
import quantulum3.classifier
import regex
from quantulum3 import parser
from quantulum3.classes import Quantity

from .quantities_utils import remove_space_after_initial_dash
from ..regex_utils import alternation, optional

# Without this, quantulum3 has a different behavior depending on the
# presence or absence of sklearn
quantulum3.classifier.USE_CLF = False


class VUEParseError(TypeError):

    def __init__(self):
        super().__init__()


@attr.s(auto_attribs=True)
class VUE:
    """
    Holds value, unit and entity parsed from a string.
    """
    v: str
    u: str
    e: str


@attr.s(auto_attribs=True)
class SpecialTerm:
    re: str
    vue: VUE


special_terms_dict = {
    'RT':
        SpecialTerm(
            re=alternation(
                [
                    '^[Rr].? ?[Tt].?$',
                    '[Rr]oom [Tt]emp.?' + optional('erature'),
                    '[Aa]mbient [Tt]emp.?' + optional('erature'),
                ]
            ),
            vue=VUE("25.0", "degree_Celsius", "temperature")
        ),
    'overnight':
        SpecialTerm(re=r'over\s?night', vue=VUE("16.0", "hour", "time")),
    'weekend':
        SpecialTerm(re=r'weekend', vue=VUE("48.0", "hour", "time")),
}

manual_check_dict = {
    'degree_celsius': dict(re=r'°?C', entity='temperature', units='degree_Celsius'),
    'degree_fahrenheit': dict(re=r'°F', entity='temperature', units='degree_fahrenheit'),
    'degree_kelvin': dict(re=r'(?:°)K', entity='temperature', units='kelvin'),
    'hour': dict(re=r' hour(?:s)?', entity='time', units='hour'),
    'minute': dict(re=r' minute(?:s)?| min\.| min(?:s)?| min\b', entity='time', units='minute'),
    'second': dict(re=r' second(?:s)?', entity='time', units='second'),
    'hr': dict(re=r'hr|h|h\.', entity='time', units='hour')
}


def get_quantulum(text: str) -> Optional[Quantity]:
    qp = parser.parse(text)
    if not qp:
        return None
    return qp[0]


def check_for_weird_values(text: str) -> Optional[str]:
    if unitary_fractional_values(text) is not None:
        return unitary_fractional_values(text)
    if check_for_to_terms(text) is not None:
        return check_for_to_terms(text)
    if check_degree_degree_celsius(text) is not None:
        return check_degree_degree_celsius(text)
    return None


def check_degree_degree_celsius(text: str) -> Optional[str]:
    rex = regex.search(r'(-?\d+)\s?°\s?-\s?(-?\d+)\s?°', text)
    if rex is None:
        return None
    return str((float(rex.group(1)) + float(rex.group(2))) / 2)


def check_for_to_terms(text: str) -> Optional[str]:
    """
    Checks for values of the form '20 to 30 mins, returns 25'
    """
    rex = regex.search(r'(-?\d+)\s?to\s?(-?\d+)', text)
    if rex is None:
        return None
    return str(float(rex.group(1)) + float(rex.group(2)) / 2)


def unitary_fractional_values(text: str) -> Optional[str]:
    """
    Checks for values of the form 121 / 2, returns 12.5
    """
    rex = regex.search(r'(\d+)1\s?\/\s?(\d+)', text)

    if rex is None:
        return None
    return str(float(rex.group(1)) + (1 / float(rex.group(2))))


def replace_weird_characters(text: str) -> str:
    special_characters_dict = {'×': 'x', '−': '-'}
    for character in special_characters_dict:
        text = text.replace(character, special_characters_dict[character])
    return text


def special_terms(text: str) -> Optional[VUE]:
    """
    Check for special strings like overnight, RT etc.
    """
    for key in special_terms_dict.keys():
        if regex.search(special_terms_dict[key].re, text):
            return special_terms_dict[key].vue
    return None


def manual_check_units(text: str) -> List[str]:
    """
    Regular expressions to search through the given sting to find units
    """
    for key in manual_check_dict.keys():
        if regex.search(manual_check_dict[key]['re'], text):
            return [manual_check_dict[key]['units'], manual_check_dict[key]['entity']]
    return ["None", "None"]


def get_vue(text: str) -> VUE:
    """
    Returns a list of value, unit and entity extracted from the given text.
    Raises VUEParseError in case of an error
    """
    text = replace_weird_characters(text)
    text = remove_space_after_initial_dash(text)
    special_term = special_terms(text)
    if special_term is not None:
        return special_term

    vue = VUE(v="None", u="None", e="None")
    vue.u, vue.e = manual_check_units(text)

    weird_value = check_for_weird_values(text)
    if weird_value is not None:
        vue.v = weird_value
        if vue.u != "None" and vue.e != "None":
            return vue

    qp = get_quantulum(text)
    # Quantulum did not find anything
    if qp is None:
        # If value was not found by check_for_weird_values or manual_check_units did not find a unit
        if vue.v == "None" or vue.u == "None" or vue.e == "None":
            raise VUEParseError
        return vue

    if vue.v == "None":
        vue.v = str(qp.value)

    if qp.unit.name != "dimensionless":
        vue.u = qp.unit.name.replace(" ", "_")
        vue.e = qp.unit.entity.name.replace(" ", "_")

    if vue.v == "None" or vue.u == "None" or vue.e == "None":
        raise VUEParseError
    return vue


def dimensionless_value_from_quantulum(text: str) -> float:
    """
    Convert a dimensionless value to a float.

    Args:
        text: quantity to convert to a float

    Raises:
        ValueError if the conversion fails
    """
    qp = get_quantulum(text)
    if qp is not None and qp.unit.name == 'dimensionless':
        return qp.value

    raise ValueError(text)
