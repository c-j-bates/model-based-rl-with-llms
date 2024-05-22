import json
from _predicates_tmp import *
from _operators_tmp import *

with open('_plan_vars_tmp_state.json', 'r') as fid:
    state = json.load(fid)

# Goal expressed as FOL formula
goal_state_str = "level_cleared(state)"

# Plan
actions = []

# Coordinates for forming the rule "flag is win" horizontally at (6,8)
rule_words = ["flag_word", "is_word", "win_word"]
start_coord = (6, 8)
orientation = "horizontal"
new_actions, new_state = form_rule(state, rule_words, start_coord, orientation)
actions.extend(new_actions)

# Move baba_obj to the flag_obj location
goal_coord = new_state['flag_obj'][0]
new_actions, new_state = move_to(new_state, "baba_obj", 0, goal_coord)
actions.extend(new_actions)

print("Actions to achieve goal:", actions)

actions_path = '_plan_vars_tmp_actions'
logger_path = '_plan_vars_tmp_logger'
goal_state_str_path = '_plan_vars_tmp_goal_state_str'
with open(actions_path, 'w') as fid:
    fid.write(str(actions))
with open(logger_path, 'w') as fid:
    fid.write(str(logger))
with open(goal_state_str_path, 'w') as fid:
    fid.write(goal_state_str)
