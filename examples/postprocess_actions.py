from paragraph2actions.action_string_converter import ReadableConverter

from smiles2actions.action_sequence_refiner import ActionSequenceRefiner

refiner = ActionSequenceRefiner()

converter = ReadableConverter(separator=' ; ', end_mark='')

action_strings = [
    'ADD water (10 ml) ; STIR for 10 minutes',
    'ADD water (10 ml) ; STIR for 10 minutes ; QUENCH with methanolic solution of HCl ; PURIFY ; YIELD product',
    'ADD A ; ADD B ; ADD C ; STIR for 10 minutes ; NOACTION ; YIELD D',
    'ADD A ; ADD B ; ADD C under nitrogen ; DRYSOLID under vacuum ; YIELD D',
    'ADD A ; ADD B at 10 °C ; ADD C at same temperature ; YIELD D',
    'ADD A ; FILTER ; DRYSOLUTION with sodium sulphate ; YIELD D',
    'ADD A ; STIR at 50 °C ; WAIT for 10 hours ; YIELD D',
    'MAKESOLUTION with CHCl2 (2 ml) and water (3 ml) ; ADD SLN ; STIR for 3 hours ; PH with acetic acid to pH 9.3 ; YIELD product',
]

for action_sequence_string in action_strings:
    actions = converter.string_to_actions(action_sequence_string)

    refined_actions = refiner.refine(actions)

    print()
    print('OLD:', converter.actions_to_string(actions))
    print('NEW:', converter.actions_to_string(refined_actions))
