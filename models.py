from copy import deepcopy
import importlib
import _model_tmp
importlib.reload(_model_tmp)
from _model_tmp import interaction_rules


def transition_model(state0, action):
    state = deepcopy(state0)
    for rule in interaction_rules:
        preds = rule.forward(state, action)
        for key, val in preds.items():
            state[key] = val
    return state
