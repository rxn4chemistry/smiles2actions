from typing import List, Optional

from paragraph2actions.actions import Action, PH, Extract, Wash, Degas
from paragraph2actions.postprocessing.filter_postprocessor import FilterPostprocessor
from paragraph2actions.postprocessing.initial_makesolution_postprocessor import \
    InitialMakesolutionPostprocessor
from paragraph2actions.postprocessing.noaction_postprocessor import NoActionPostprocessor
from paragraph2actions.postprocessing.postprocessor_combiner import PostprocessorCombiner
from paragraph2actions.postprocessing.same_temperature_postprocessor import \
    SameTemperaturePostprocessor
from paragraph2actions.postprocessing.wait_postprocessor import WaitPostprocessor
from paragraph2actions.utils import (
    apply_to_temperatures, apply_to_durations, apply_to_atmospheres,
    remove_quantities
)

from .quantities.duration_placeholder import DurationPlaceholder
from .quantities.ph_binner import PHBinner
from .quantities.quantity_binner import BinningError
from .quantities.temperature_placeholder import TemperaturePlaceholder


class ActionSequenceRefiner:
    """
    Refines sequences of actions for use as training data for SMILES to actions.

    Does the following:
    * General postprocessing steps including removal of NoAction, merging
      unnecessarily duplicated actions, etc.
    * pH binning
    * temperature binning
    * duration binning
    * removal of quantities
    * ...
    """

    def __init__(self):
        self.processor = PostprocessorCombiner(
            postprocessors=[
                NoActionPostprocessor(),
                WaitPostprocessor(),
                FilterPostprocessor(),
                SameTemperaturePostprocessor(),
                InitialMakesolutionPostprocessor(),
            ]
        )
        self.duration_placeholders = DurationPlaceholder()
        self.temperature_placeholders = TemperaturePlaceholder()
        self.ph_binner = PHBinner()
        self.ph_bin_names = ['acidic', 'neutral', 'basic']

    def refine(self, actions: List[Action]) -> List[Action]:
        actions = self.general_action_postprocessing(actions)
        self.replace_unknown_durations(actions)
        self.bin_ph(actions)
        self.bin_durations(actions)
        self.bin_temperatures(actions)
        self.remove_repetitions_for_wash_and_extract(actions)
        self.maybe_remove_atmosphere(actions)
        remove_quantities(actions)
        return actions

    def general_action_postprocessing(self, actions: List[Action]) -> List[Action]:
        return self.processor.postprocess(actions)

    def bin_ph(self, actions: List[Action]) -> None:
        for a in actions:
            if isinstance(a, PH):
                if a.ph is None:
                    continue
                try:
                    bin_index = self.ph_binner.get_bin(a.ph)
                    a.ph = self.ph_bin_names[bin_index]
                except BinningError:
                    continue

    def bin_durations(self, actions: List[Action]) -> None:
        apply_to_durations(actions, self.duration_placeholders.to_placeholder)

    def bin_temperatures(self, actions: List[Action]) -> None:
        apply_to_temperatures(actions, self.temperature_placeholders.to_placeholder)

    def replace_unknown_durations(self, actions: List[Action]) -> None:
        """For some action types, replace unknown durations by None."""
        for a in actions:
            if isinstance(a, Degas):
                if a.duration == 'unknown':
                    a.duration = None

    def remove_repetitions_for_wash_and_extract(self, actions: List[Action]) -> None:
        for a in actions:
            if isinstance(a, (Wash, Extract)):
                a.repetitions = 1

    def maybe_remove_atmosphere(self, actions: List[Action]) -> None:
        """
        Remove the atmosphere, except if it is 'vacuum'.
        """

        def fn(atmosphere: str) -> Optional[str]:
            if atmosphere == 'vacuum':
                return atmosphere
            return None

        apply_to_atmospheres(actions, fn)
