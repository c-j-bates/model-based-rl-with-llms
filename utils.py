# utils.py
from predicates import check_rule, is_adjacent, is_moveable, is_unoccupied

def get_delta(action):
    if action == 'up':
        delta = (0, 1)
    elif action == 'down':
        delta = (0, -1)
    elif action == 'left':
        delta = (-1, 0)
    elif action == 'right':
        delta = (1, 0)
    return delta

def push(state, action, entity1, entity2):
    from copy import deepcopy
    new_e1 = deepcopy(state[entity1['name']])
    new_e2 = deepcopy(state[entity2['name']])
    
    # Checking individual preconditions
    rule_check = check_rule(state, [entity1['name'].split('_')[0] + '_word', 'is_word', 'you_word'])
    adjacency_check = is_adjacent(entity1['coord'], entity2['coord'])
    moveable_check = is_moveable(state, entity2['name'])

    ############

    if not adjacency_check:
        # Define goal as a predicate
        goal_cond = lambda state_, name, init_coord, goal_coord: goal_coord in state_[name] and init_coord not in state_[name]

        # Use world model to search exhaustively over action sequences to reach goal

        init_coord = entity1['coord']
        goal_coord = entity2['coord']   # figure out way to represent adjacency

        # breakpoint() return nothing?
        low_level_planner(state, goal_cond, entity1, init_coord, goal_coord)


        
    #################
    preconds = rule_check and adjacency_check and moveable_check

    print(f"Attempting to push {entity1['name']} from {entity1['coord']} to {entity2['coord']}")
    print(f"Preconditions: check_rule={rule_check}, is_adjacent={adjacency_check}, is_moveable={moveable_check}")
    print(f"Preconditions met: {preconds}")

    if preconds:
        delta = get_delta(action)
        next_e2_occupancy = [entity2['coord'][0] + delta[0], entity2['coord'][1] + delta[1]]
        print(f"Next e2 occupancy: {next_e2_occupancy}")

        if is_unoccupied(state, next_e2_occupancy):
            next_e1_occupancy = [entity1['coord'][0] + delta[0], entity1['coord'][1] + delta[1]]
            print(f"Next e1 occupancy: {next_e1_occupancy}")

            new_e2.remove(entity2['coord'])
            new_e2.append(next_e2_occupancy)
            new_e1.remove(entity1['coord'])
            new_e1.append(next_e1_occupancy)

            print(f"Push successful: {entity1['name']} to {next_e1_occupancy}, {entity2['name']} to {next_e2_occupancy}")
            print(f"New coordinates for {entity1['name']}: {new_e1}")
            print(f"New coordinates for {entity2['name']}: {new_e2}")
            
            new_state = deepcopy(state)
            new_state[entity1['name']] = new_e1
            new_state[entity2['name']] = new_e2
            return new_state

    print("Push failed. Returning original state.")
    return deepcopy(state)



