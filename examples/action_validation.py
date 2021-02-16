from paragraph2actions.action_string_converter import ReadableConverter

from smiles2actions.action_sequence_validator import (
    ActionSequenceValidator, InvalidActionSequence
)

validator = ActionSequenceValidator()

converter = ReadableConverter(separator=' ; ', end_mark='')

action_strings = [
    'INVALIDACTION',
    'ADD water (10 ml) ; STIR for 10 minutes',
    'ADD water (10 ml) ; STIR for 10 minutes ; QUENCH with methanolic solution of HCl ; PURIFY ; YIELD product',
    'ADD A ; ADD B ; ADD C ; STIR for 10 minutes ; NOACTION ; YIELD D',
    'ADD A ; ADD B ; ADD C ; YIELD D ; STIR for 10 minutes ; YIELD E',
    'MAKESOLUTION with water and HCl ; ADD B ; ADD C ; STIR for 10 minutes ; YIELD E',
]

for action_sequence_string in action_strings:
    actions = converter.string_to_actions(action_sequence_string)

    try:
        validator.validate(actions)
        print('Action sequence is valid!')
    except InvalidActionSequence as e:
        print(f'Action sequence is invalid. {e.__class__.__name__}: {e}')
