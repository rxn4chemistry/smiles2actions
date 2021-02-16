from .quantities_utils import get_unit_registry
from .quantity import RxnQuantity
from .value_unit_entity import get_vue, VUE, VUEParseError

durations_dict = {
    'microsecond': 10e-7,
    'millisecond': 10e-4,
    'second': 1.0,
    'second_of_arc': 1.0,
    'minute': 60.0,
    "minute_of_arc": 60.0,
    'hour': 3600.0,
    'day': 86400.0,
    'dime': 86400.0,
    'week': 6048e2,
    'year': 31536e3
}

u = get_unit_registry()


class DurationExtractionError(ValueError):

    def __init__(self, duration: str):
        super().__init__(f'Conversion of duration failed for "{duration}".')


class DurationExtractor:

    def __init__(self):
        self.to_remove = ['additional ', 'more ', 'about ']

    def extract_duration(self, duration: str) -> RxnQuantity:
        for word_to_remove in self.to_remove:
            duration = duration.replace(word_to_remove, '')
        try:
            vue = get_vue(duration)
            return RxnQuantity(duration_to_float(duration, vue) * u.second)
        except VUEParseError as e:
            raise DurationExtractionError(duration) from e


def duration_to_float(duration: str, vue: VUE) -> float:
    if vue.e not in ["angle", "time", "currency"]:
        raise DurationExtractionError(duration)
    answer = 0.0
    try:
        answer += float(vue.v) * durations_dict[vue.u]
    except KeyError:
        raise DurationExtractionError(duration)
    return answer
