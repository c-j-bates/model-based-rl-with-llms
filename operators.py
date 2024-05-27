from copy import deepcopy
from planners import low_level_planner
from predicates import check_rule

logger = []  # Stack for logging planner failures


def move_to(state, entity_name, token_idx, goal_coord):
    # Move token of entity_name to goal_coord
    initial_coord = state[entity_name][token_idx]
    if initial_coord == goal_coord:
        logger.append({'operator': 'move_to', 'message': 'Already at goal_coord'})
        return [], state

    # Define goal as a predicate
    goal_cond = lambda state_, name, init_coord, goal_coord: goal_coord in state_[name] and init_coord not in state_[name]

    # Use world model to search exhaustively over action sequences to reach goal
    actions, new_state = low_level_planner(state, goal_cond, entity_name, initial_coord, goal_coord)

    if goal_cond(new_state, entity_name, initial_coord, goal_coord):
        message = 'Success'
    else:
        message = 'Failure'
    logger.append({'operator': 'move_to', 'message': message})

    return actions, new_state

def push_to(state, patient_name, token_idx, goal_coord):
    initial_coord = state[patient_name][token_idx]  # Get the specific token of patient_name
    controlled_entities = state.get('controlled', [])
    if initial_coord == goal_coord:
        logger.append({'operator': 'push_to', 'message': 'Already at goal_coord'})
        return [], state

    if patient_name in controlled_entities:
        logger.append({'operator': 'push_to', 'message': 'Can only push non-controlled entities'})
        return [], state

    # Define goal as a predicate
    goal_cond = lambda state_, name, init_coord, goal_coord: goal_coord in state_[name] and init_coord not in state_[name]

    # Use world model to search exhaustively over action sequences to reach goal
    actions, new_state = low_level_planner(state, goal_cond, patient_name, initial_coord, goal_coord)

    if goal_cond(new_state, patient_name, initial_coord, goal_coord):
        message = 'Success'
    else:
        message = 'Failure'
    logger.append({'operator': 'push_to', 'message': message})
    return actions, new_state

def form_rule(state, rule_words, start_coord, orientation):
     """
    You can form rules with this operator. It will take the starting coordinate
    as the final place where the rule_words will begin from and go either horizontally or vertically.
    Try to notice if any of the words from rule_words are already close and if they are try to think
    of a start_coord and orientation that allows you to form the rule with the least number of push_to actions. Also remember
    if some of the rules are at the boundaries/corners of the map then you can't push them into certain locations.

    Example
    --------
    
    Let's say you want to form the rule "Flag is Win" from [flag_word is_word win_word]
    Let's say the initial coordinate for these words are as follows: flag_word (4, 3), is_word (7, 1), win_word (8, 1)
    In this case the easiest way to form the rule "Flag is Win" would be to use the form_rule operator with the start_coord as (6, 1).
    This because is_word and win_word are already together. So by setting the start_coord as (6, 1) and
    setting the orientation to horizontal, form_rule would push the flag_word to (6, 1) and easily horizontally form the rule 
    "Flag is Win"
 
    """
    if check_rule(state, rule_words):
        logger.append({'operator': 'form_rule', 'message': 'Rule already formed'})
        return [], state

    final_coords = [start_coord]
    if orientation == 'horizontal':
        # Line the words up horizontally
        for word in rule_words[1:]:
            final_coords.append((final_coords[-1][0] + 1, final_coords[-1][1]))
    else:
        for word in rule_words[1:]:
            final_coords.append((final_coords[-1][0], final_coords[-1][1] + 1))
        # Line the words up vertically

    actions = []
    new_state = deepcopy(state)
    # Push each word in turn to its final coordinate
    for word, coord in zip(rule_words, final_coords):
        # Iterate over tokens of word to find the one that needs the fewest actions to reach goal
        min_seq_len = float('inf')
        outcomes = {}
        for token_idx in range(len(new_state[word])):
            new_actions_, new_state_ = push_to(new_state, word, token_idx, coord)
            outcomes[token_idx] = [new_actions_, new_state_]  # Store the actions and state for each token
            if len(new_actions_) < min_seq_len:
                min_seq_len = len(new_actions_)
                min_token_idx = token_idx
        new_actions, new_state = outcomes[min_token_idx]
        actions.extend(new_actions)

    if check_rule(new_state, rule_words):
        message = 'Success'
    else:
        message = 'Failure'
    logger.append({'operator': 'form_rule', 'message': message})
    return actions, new_state
