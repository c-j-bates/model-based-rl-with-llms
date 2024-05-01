def check_rule(state, words):
    # Check that a rule is formed
    same_row = state[words[0]][0][1] == state[words[1]][0][1] == state[words[2]][0][1]
    same_col = state[words[0]][0][0] == state[words[1]][0][0] == state[words[2]][0][0]
    if same_row or same_col:
        return True
    return False


def is_adjacent(x, y):
    # Check if two coordinates are adjacent
    if (abs(x[0] - y[0]) == 1 and abs(x[1] - y[1]) == 0) or (abs(x[0] - y[0]) == 0 and abs(x[1] - y[1]) == 1):
        return True
    return False


def overlapping(entity1_coord, entity2_coord):
    if entity1_coord == entity2_coord:
        return True
    return False


def is_moveable(state, entity_name):
    # TODO: How to implement this? Maybe write a lookup function that considers all active rules?
    return True


def is_unoccupied(state, coord):
    if coord in state['empty']:
        return True
    return False


def level_cleared(state):
    # Check that baba_obj is on top of flag_obj and flag is win
    if overlapping(state['baba_obj'][0], state['flag_obj'][0]) and check_rule(state, ['flag_word', 'is_word', 'win_word']):
        return True
    return False
