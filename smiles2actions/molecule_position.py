from collections import defaultdict
from typing import Dict, List

from .utils import ReactionEquation


class MoleculePosition:

    def __init__(self, reaction_equation: ReactionEquation):
        self.reaction_equation = reaction_equation
        self.molecule_position_dict: Dict[str, List[int]] = defaultdict(lambda: [])
        self.inverse_position_dict: Dict[int, str] = {}
        self.create_molecule_position_dict()

    def create_molecule_position_dict(self):
        for index, precursor in enumerate(
            self.reaction_equation.reactants + self.reaction_equation.agents, 1
        ):
            self.molecule_position_dict[precursor].append(index)
            self.inverse_position_dict[index] = precursor
        for index, product in enumerate(self.reaction_equation.products, 1):
            self.molecule_position_dict[product].append(-index)
            self.inverse_position_dict[-index] = product

    def get_positions_for_smiles(self, smiles: str) -> List[int]:
        try:
            return self.molecule_position_dict[smiles]
        except KeyError:
            return []

    def get_position_for_smiles(self, smiles: str) -> int:
        positions = self.get_positions_for_smiles(smiles)
        if len(positions) != 1:
            raise ValueError(f'Cannot get position for SMILES {smiles}')
        return positions[0]
