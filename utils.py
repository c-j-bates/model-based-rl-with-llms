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
    new_e1 = state[entity1['name']]
    new_e2 = state[entity2['name']]
    preconds = check_rule(state, [entity1['name'].split('_')[0] + '_word', 'is_word', 'you_word']) \
        and is_adjacent(entity1['coord'], entity2['coord']) \
        and is_moveable(state, entity2['name'])

    if preconds:
        delta = get_delta(action)
        next_e2_occupancy = (entity2['coord'][0] + delta[0], entity2['coord'][1] + delta[1])
        if is_unoccupied(state, next_e2_occupancy):
            next_e1_occupancy = (entity1['coord'][0] + delta[0], entity1['coord'][1] + delta[1])
            new_e2.remove(entity2['coord'])
            new_e2.append(next_e2_occupancy)
            new_e1.remove(entity1['coord'])
            new_e1.append(next_e1_occupancy)
            return {entity1['name']: new_e1, entity2['name']: new_e2}
    return {entity1['name']: state[entity1['name']], entity2['name']: state[entity2['name']]}
