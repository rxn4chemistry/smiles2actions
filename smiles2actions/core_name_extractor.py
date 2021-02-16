from typing import List, Optional

from .name_filters.compound_name_trimmer import CompoundNameTrimmer
from .name_filters.concentration_filter import ConcentrationFilter
from .name_filters.diverse_filter import DiverseFilter
from .name_filters.filter import Filter
from .name_filters.material_descriptor_filter import MaterialDescriptorFilter
from .name_filters.matter_word_filter import MatterWordFilter
from .name_filters.mixture_composition_filter import MixtureCompositionFilter
from .name_filters.multiple_compound_detector import MultipleCompoundDetector
from .name_filters.referenced_compound_filter import ReferencedCompoundFilter
from .name_filters.solution_descriptor_filter import SolutionDescriptorFilter
from .name_filters.state_filter import StateFilter
from .name_filters.temperature_adjective_filter import \
    TemperatureAdjectiveFilter
from .utils import remove_slices_of_string


class CoreNameExtractor:
    """
    From the name of a chemical which may be too vague, this class will extract one or several essential
    names of molecules / compounds.

    Example:
        '2M solution of HCl in water' -> ['HCl', 'water']
    """

    def __init__(self, filters: Optional[List[Filter]] = None):
        if filters is None:
            filters = [
                TemperatureAdjectiveFilter(),
                ConcentrationFilter(),
                SolutionDescriptorFilter(),
                MaterialDescriptorFilter(),
                MatterWordFilter(),
                StateFilter(),
                MixtureCompositionFilter(),
                ReferencedCompoundFilter(),
                DiverseFilter(),
            ]
        self.filters = filters

        self.trimmer = CompoundNameTrimmer()
        self.multiple_compound_detector = MultipleCompoundDetector()

    def strip_compound(self, name: str) -> str:
        """
        Filters out substrings to remove, and trims the obtained compound name.
        """
        matches_to_remove = [match for f in self.filters for match in f.find_matches(name)]

        slices_to_remove = [n.span for n in matches_to_remove]
        name = remove_slices_of_string(slices_to_remove, name)

        return self.trimmer.trim(name)

    def split_stripped_compound(self, name: str) -> List[str]:
        """
        Split an already-stripped compound name.
        """
        return self.multiple_compound_detector.get_candidates(name)
