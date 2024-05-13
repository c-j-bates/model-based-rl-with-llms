import json
from _predicates_tmp import *
from _operators_tmp import *

with open('_plan_vars_tmp_state.json', 'r') as fid:
    state = json.load(fid)

# Based on the current state, the winning condition in the game is already set with "Flag is Win"
# and the player controls Baba as indicated by "Baba is You". The flag is at (7,4) while Baba is
# currently at (2,4). Based on these positions, the shortest route for Baba to reach the flag is
# to move towards the right.

# Goal
goal_state_str = "level_cleared(state)" # Callable with exec

# Plan
actions = []
new_actions, new_state = move_to(state, 'baba_obj', 0, (7, 4))
actions.extend(new_actions)

actions_path = '_plan_vars_tmp_actions'
logger_path = '_plan_vars_tmp_logger'
goal_state_str_path = '_plan_vars_tmp_goal_state_str'
with open(actions_path, 'w') as fid:
    fid.write(str(actions))
with open(logger_path, 'w') as fid:
    fid.write(str(logger))
with open(goal_state_str_path, 'w') as fid:
    fid.write(goal_state_str)
