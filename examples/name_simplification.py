from smiles2actions.dict_based_name_to_smiles import DictBasedNameToSmiles
from smiles2actions.dict_based_smiles_to_name import DictBasedSmilesToName
from smiles2actions.name_normalizer import NameNormalizer
from smiles2actions.name_simplifier import NameSimplifier

# Construct the name-to-SMILES and SMILES-to-name mappings
n2s = DictBasedNameToSmiles(
    {
        'water': 'O',
        'H2O': 'O',
        'HCl': 'Cl',
        'DCM': 'ClCCl',
        'methanol': 'CO',
        'sulfuric acid': 'OS(=O)(=O)O',
        'H2SO4': 'OS(=O)(=O)O',
    },
    normalize_fn=NameNormalizer.default_normalizer()
)
s2n = DictBasedSmilesToName(
    {
        'O': 'water',
        'Cl': 'HCl',
        'ClCCl': 'DCM',
        'CO': 'methanol',
        'OS(=O)(=O)O': 'H2SO4',
    }
)

# The name simplifier strips unnecessary information from compound names
name_simplifier = NameSimplifier()


def is_valid_compound_name(name: str) -> bool:
    """Names are considered to be valid if they are present in the name-to-SMILES mapping."""
    return n2s.has_smiles(name)


def get_synonym(name: str) -> str:
    """Apply name-to-SMILES followed by SMILES-to-name in order to get the most common synonym."""
    return s2n.get_name(n2s.get_smiles(name))


names_to_simplify = [
    'concentrated HCl',
    'conc. HCl',
    '~1 M HC1',
    'HCI (l)',
    'solution of HCl in water',
    'WATER - HCl (10:1)',
    '1.2M solution of WATER and methanol',
    'hot 1M HCl solution',
    'methanol-h₂o',
    'DCM solution of HCl',
    'methanolic HCl',
    'dcm solution of 1:1 water / 30% sulfuric acid',
    'dcm solution of 1:1 water / sat. brine',
]

for name_to_simplify in names_to_simplify:
    print(f'\nProcessing the name "{name_to_simplify}"')

    # We try to iteratively simplify the original compound name, until a
    # fully-valid match is found.
    for names in name_simplifier.simplify(name_to_simplify):
        print(f'  Checking the following simplification: {", ".join(names)}')
        if all(is_valid_compound_name(c) for c in names):
            print(f'Simplified name(s): {", ".join(names)}')
            synonyms = [get_synonym(simplified_name) for simplified_name in names]
            print(f'Replaced by synonym(s): {", ".join(synonyms)}')
            break
    else:
        print('The name could not be simplified.')
