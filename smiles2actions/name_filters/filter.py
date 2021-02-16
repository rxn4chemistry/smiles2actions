from abc import ABC, abstractmethod
from typing import List

from ..regex_utils import RegexMatch


class Filter(ABC):
    """Base class for extracting a piece of information from a compound name"""

    @abstractmethod
    def find_matches(self, chemical_name: str) -> List[RegexMatch]:
        """Detect substring(s) in a compound name that correspond to the aspect defined by derived classes"""
