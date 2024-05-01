from models import transition_model
from copy import deepcopy
from pathlib import Path

with Path('_actions_set_tmp.py').open('r') as fid:
    exec(fid.read())
if 'actions_set' not in globals():
    raise ValueError('actions_set not loaded')


def enumerative_search(state0, goal_cond, *args, strategy='bfs', max_iters=2000):
    """
    Search for a goal state
    """
    from collections import deque

    # Depth-first search
    start = ()
    states = {start: deepcopy(state0)}
    queue = deque([start])

    search_iters = 0

    while queue:
        search_iters += 1
        if strategy == 'bfs':
            node = queue.popleft()
        else:
            # Depth-first search
            node = queue.pop()

        if goal_cond(states[node], *args):
            # Goal reached
            break

        if search_iters > max_iters:
            # print('MAX DEPTH REACHED')
            break

        # Build adjacency graph dynamically to only include actions
        # that change the state of the game in some way (e.g. don't
        # keep running into a wall), and are valid
        for a in actions_set:
            state = transition_model(deepcopy(states[node]), a)
            # print(state['baba_obj'], state['flag_word'])
            if state is not None and state != states[node] and not state.get('lost'):
                new_node = node + (a,)
                states[new_node] = deepcopy(state)
                queue.append(new_node)
                if goal_cond(states[new_node], *args):
                    # Goal reached
                    print('Goal reached')
                    break
    actions = list(node)
    return actions, states[node]


def low_level_planner(state, goal_cond, *args):
        actions, new_state = enumerative_search(state, goal_cond, *args)
        return actions, new_state
