from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Union, Generator

import attr
import numpy as np
from paragraph2actions.actions import Action
from paragraph2actions.utils import extract_chemicals

dash_characters = [
    '-',  # hyphen-minus
    '–',  # en dash
    '—',  # em dash
    '−',  # minus sign
    '­',  # soft hyphen
]


def remove_slices_of_string(slices: Iterable[slice], string: str) -> str:
    """Remove parts of a string"""

    # create mask of which characters to remove
    remove_index_mask = np.full(len(string), False)
    for s in slices:
        remove_index_mask[s] = True

    # convert string to a list
    lst = list(string)

    # remove characters
    for index, remove_index in enumerate(remove_index_mask):
        if remove_index:
            lst[index] = ''

    # convert back to a string
    return ''.join(lst)


def remove_prefix(text: str, prefix: str) -> str:
    """Removes a prefix from a string, if present at its beginning.

    Args:
        text: string potentially containing a prefix.
        prefix: string to remove at the beginning of text.
    """
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def remove_postfix(text: str, postfix: str) -> str:
    """Removes a postfix from a string, if present at its end.

    Args:
        text: string potentially containing a postfix.
        postfix: string to remove at the end of text.
    """
    if text.endswith(postfix):
        return text[:-len(postfix)]
    return text


@attr.s(auto_attribs=True)
class ReactionEquation:
    """
    Defines a reaction equation, as given by the molecules involved in a reaction.

    Attributes:
        reactants: SMILES strings for compounds on the left of the reaction arrow.
        agents: SMILES strings for compounds above the reaction arrow. Are
            sometimes merged with the reactants.
        products: SMILES strings for compounds on the right of the reaction arrow.
    """
    reactants: List[str]
    agents: List[str]
    products: List[str]

    def __iter__(self) -> Iterator[List[str]]:
        """Helper function to simplify functionality acting on all three
        compound groups"""
        return (i for i in (self.reactants, self.agents, self.products))

    @classmethod
    def from_string(
        cls, reaction_string: str, fragment_bond: Optional[str] = None
    ) -> 'ReactionEquation':
        """
        Convert a ReactionEquation from an "rxn" reaction SMILES.
        """

        smiles_groups = reaction_string.split('>')

        # split the groups
        groups = [smiles_group.split('.') for smiles_group in smiles_groups]

        # replace [''] by [] (for instance when there are no agents)
        groups = [group if group != [''] else [] for group in groups]

        # replace fragment bonds if necessary
        if fragment_bond is not None:
            groups = [[smi.replace(fragment_bond, '.') for smi in group] for group in groups]

        return cls(*groups)


def colorblind_color_palette(n: int) -> List[str]:
    """
    Get a colorblind-friendly color palette.

    Adapted from https://gist.github.com/thriveth/8560036.

    Args:
        n: size of the color palette. Up to 9 is allowed.

    Returns:
        List of RGB codes.
    """
    if n > 9:
        raise ValueError(f'Maximal color palette size allowed: 9. Requested: {n}')

    full_color_palette = [
        '#377eb8', '#4daf4a', '#f781bf', '#a65628', '#ff7f00', '#999999', '#984ea3', '#e41a1c',
        '#dede00'
    ]
    return full_color_palette[:n]


def load_list_from_file(filename: Union[Path, str]) -> List[str]:
    return list(iterate_lines_from_file(filename))


def iterate_lines_from_file(filename: Union[Path, str]) -> Generator[str, None, None]:
    with open(str(filename), 'rt') as f:
        for line in f:
            yield line.strip()


def detokenize_smiles(tokenized_smiles: str) -> str:
    """
    Detokenize a tokenized SMILES string (that contains spaces between the characters).

    Args:
        tokenized_smiles: tokenized SMILES, for instance 'C C ( C O ) = N >> C C ( C = O ) N'

    Returns:
        SMILES after detokenization, for instance 'CC(CO)=N>>CC(C=O)N'
    """
    return tokenized_smiles.replace(' ', '')
