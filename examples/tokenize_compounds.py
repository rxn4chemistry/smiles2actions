from typing import Iterable

from paragraph2actions.action_string_converter import ReadableConverter
from paragraph2actions.actions import Action
from paragraph2actions.utils import extract_chemicals

from smiles2actions.dict_based_name_to_smiles import DictBasedNameToSmiles
from smiles2actions.molecule_position import MoleculePosition
from smiles2actions.placeholder_handler import PlaceholderHandler
from smiles2actions.utils import ReactionEquation

admissible_reagents = [
    'water',
    'brine',
]

# For illustration purposes - the chemical equations are not realistic
reactions = [
    (
        'CC.C>>CCC',
        'ADD ethane ; ADD methane ; STIR for 8 hours ; QUENCH with brine ; YIELD propane'
    ),
    (
        'CC.C.[Na+]~[Cl-]>>CCC',
        'ADD ethane ; ADD methane ; ADD sodium chloride ; STIR for 8 hours ; QUENCH with brine ; YIELD propane'
    ),
    (
        'CCCC.C>>CCC',
        'ADD butane ; ADD methane ; STIR for 8 hours ; QUENCH with brine ; YIELD propane'
    ),
    (
        'CC.C>>CCC',
        'ADD ethane ; ADD methane ; STIR for 8 hours ; QUENCH with HCl ; PURIFY ; YIELD propane'
    ),
    (
        'CCCC.C>>CCC',
        'ADD ethane ; ADD methane ; STIR for 8 hours ; QUENCH with HCl ; YIELD propane'
    ),
]

n2s = DictBasedNameToSmiles(
    {
        'ethane': 'CC',
        'methane': 'C',
        'propane': 'CCC',
        'sodium chloride': '[Na+].[Cl-]',
    }
)

converter = ReadableConverter(separator=' ; ', end_mark='')
compound_placeholder_handler = PlaceholderHandler.for_compounds()


def tokenize_compounds(actions: Iterable[Action]) -> None:
    """Tokenize the compound names of a list of actions, in-place."""
    for chemical in extract_chemicals(actions):
        if n2s.has_smiles(chemical.name):
            smiles = n2s.get_smiles(chemical.name)
            try:
                position = molecule_position.get_position_for_smiles(smiles)
                chemical.name = compound_placeholder_handler.to_placeholder(position)
                continue
            except ValueError:
                pass
        if chemical.name in admissible_reagents:
            continue
        raise ValueError(f'"{chemical.name}" is not admissible')


for reaction_smiles, actions_string in reactions:
    actions = converter.string_to_actions(actions_string)
    reaction_equation = ReactionEquation.from_string(reaction_smiles, fragment_bond='~')
    molecule_position = MoleculePosition(reaction_equation)

    print('\nOLD:', actions_string)
    try:
        tokenize_compounds(actions)
        print('NEW:', converter.actions_to_string(actions))
    except ValueError as e:
        print('ERROR:', str(e))
