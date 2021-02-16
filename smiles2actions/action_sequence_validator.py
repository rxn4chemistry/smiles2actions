import itertools
from typing import List

from paragraph2actions.actions import (
    Action, FollowOtherProcedure, InvalidAction, Concentrate, Purify, Yield, NoAction,
    Recrystallize, OtherLanguage, MakeSolution
)
from paragraph2actions.utils import extract_chemicals


class InvalidActionSequence(ValueError):

    def __init__(self, msg: str):
        super().__init__(msg)


class UnsupportedActionType(InvalidActionSequence):

    def __init__(self, action: Action):
        super().__init__(action.action_name)


class TooShortActionSequence(InvalidActionSequence):

    def __init__(self, number_actions: int):
        super().__init__(str(number_actions))


class MultipleStepsInSequence(InvalidActionSequence):

    def __init__(self):
        super().__init__('The action sequence is likely to describe multiple reaction steps.')


class InconsistentMakeSolutionAndSLN(InvalidActionSequence):

    def __init__(self, number_makesolution: int, number_sln: int):
        super().__init__(
            f'Inconsistent number of MakeSolution actions ({number_makesolution}) '
            f'and "SLN" mentions ({number_sln}).'
        )


class ActionSequenceValidator:
    """
    Defines which action sequences can be used for training SMILES to actions
    models and which not.
    """

    def __init__(self):
        self.avoided_action_types = (InvalidAction, FollowOtherProcedure, OtherLanguage)
        self.admissible_between_yield_actions = (
            Yield, Purify, Concentrate, Recrystallize, NoAction
        )
        self.short_sequence_threshold = 5

    def validate(self, actions: List[Action]) -> None:
        """
        Raises InvalidActionSequence or subclass if the action sequence is not
        valid.
        """
        self.validate_forbidden_actions(actions)
        self.validate_short_sequences(actions)
        self.validate_multiple_reaction_steps(actions)
        self.validate_missing_sln(actions)

    def validate_forbidden_actions(self, actions: List[Action]) -> None:
        for action in actions:
            if isinstance(action, self.avoided_action_types):
                raise UnsupportedActionType(action)

    def validate_short_sequences(self, actions: List[Action]) -> None:
        actual_actions = [a for a in actions if not isinstance(a, NoAction)]
        if len(actual_actions) < self.short_sequence_threshold:
            raise TooShortActionSequence(len(actual_actions))

    def validate_multiple_reaction_steps(self, actions: List[Action]) -> None:
        """
        Raises if a list of actions is likely to actually contain several
        reaction steps.

        This is likely when there are multiple Yield actions that are separated
        by more than simple purification steps.
        """

        # All is fine if there is zero or one Yield action
        if len([a for a in actions if isinstance(a, Yield)]) <= 1:
            return

        # drop actions until first yield
        truncated_actions = list(itertools.dropwhile(lambda a: not isinstance(a, Yield), actions))
        # drop actions after last yield
        truncated_actions.reverse()
        truncated_actions = list(
            itertools.dropwhile(lambda a: not isinstance(a, Yield), truncated_actions)
        )
        truncated_actions.reverse()

        # Return False if all of the remaining actions are admissible, else True
        if not all(
            isinstance(action, self.admissible_between_yield_actions)
            for action in truncated_actions
        ):
            raise MultipleStepsInSequence()

    def validate_missing_sln(self, actions: List[Action]) -> None:
        number_makesolution = sum(1 for action in actions if isinstance(action, MakeSolution))
        number_sln = sum(
            1 for compound in extract_chemicals(actions, ignore_sln=False)
            if compound.name == 'SLN'
        )
        if number_makesolution != number_sln:
            raise InconsistentMakeSolutionAndSLN(
                number_makesolution=number_makesolution, number_sln=number_sln
            )
