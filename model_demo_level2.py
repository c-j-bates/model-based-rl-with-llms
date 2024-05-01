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
    from predicates import check_rule, is_adjacent, is_moveable, is_unoccupied
    new_e1 = state[entity1['name']]
    new_e2 = state[entity2['name']]
    preconds = check_rule(state, [entity1['name'].split('_')[0] + '_word', 'is_word', 'you_word']) \
        and is_adjacent(entity1['coord'], entity2['coord']) \
        and is_moveable(state, entity2['name'])

    # if entity1['name'] == 'baba_obj' and entity2['name'] == 'flag_word':

    if preconds:
        # If entity 1 is adjacent to entity 2 and it's moveable, then both will be displaced by action
        delta = get_delta(action)
        # Look to see if there are any obstacles behind entity 2 that would prevent it from moving
        next_e2_occupancy = (entity2['coord'][0] + delta[0], entity2['coord'][1] + delta[1])
        if is_unoccupied(state, next_e2_occupancy):
            next_e1_occupancy = (entity1['coord'][0] + delta[0], entity1['coord'][1] + delta[1])
            new_e2.remove(entity2['coord'])
            new_e2.append(next_e2_occupancy)
            new_e1.remove(entity1['coord'])
            new_e1.append(next_e1_occupancy)
            return {entity1['name']: new_e1, entity2['name']: new_e2}
    return {entity1['name']: state[entity1['name']], entity2['name']: state[entity2['name']]}


interaction_rules = []

class BaseInteractionRule:
    def __init__(self, entity_key1, entity_key2):
        self.entity_key1 = entity_key1  # Field that corresponds to entity class 1
        self.entity_key2 = entity_key2  # Field that corresponds to entity class 2

    def forward(self, state, action):
        """Method to be overridden. 

        Runs forward model to predict new states for entity1 and entity2, specifically.
        Note the overall state is provided because predictions could be mediated by
        other dimensions of the overall state.

        Args:
            state: full state, including all objects
            action: proposed action

        Returns:
            dict of predicted states of tokens of entity1 and entity2 after taking action
        """
        # No-op
        predictions = {{
            self.entity_key1: state[self.entity_key1],
            self.entity_key2: state[self.entity_key2]
        }}
        return predictions

class BorderBabaWordInteractionRule(BaseInteractionRule): 
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BorderBabaWordInteractionRule('border', 'baba_word'))

class BorderEmptyInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BorderEmptyInteractionRule('border', 'empty'))

class BorderIsWordInteractionRule(BaseInteractionRule): 
    def forward(self, state, action): 
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BorderIsWordInteractionRule('border', 'is_word'))

class BorderBabaObjInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BorderBabaObjInteractionRule('border', 'baba_obj'))

class BorderYouWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BorderYouWordInteractionRule('border', 'you_word'))

class BorderFlagWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BorderFlagWordInteractionRule('border', 'flag_word'))


class BorderFlagObjInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BorderFlagObjInteractionRule('border', 'flag_obj'))


class BorderWinWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BorderWinWordInteractionRule('border', 'win_word'))


class BorderWonInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BorderWonInteractionRule('border', 'won'))


class BorderLostInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BorderLostInteractionRule('border', 'lost'))


class BabaWordEmptyInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BabaWordEmptyInteractionRule('baba_word', 'empty'))


class BabaWordIsWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BabaWordIsWordInteractionRule('baba_word', 'is_word'))


class BabaWordBabaObjInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        from itertools import product
        from copy import deepcopy

        new_state = deepcopy(state)
        # For each token of entity1, predict its interaction with each token of entity2
        # (Assumes updates are independent of each other, which is not always the case in general)
        for coord1, coord2 in product(state[self.entity_key1], state[self.entity_key2]):
            updates = push(new_state, action, {'name': self.entity_key1, 'coord': coord1}, {'name': self.entity_key2, 'coord': coord2})
            for key, val in updates.items():
                new_state[key] = val
        return new_state

interaction_rules.append(BabaWordBabaObjInteractionRule('baba_word', 'baba_obj'))


class BabaWordYouWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BabaWordYouWordInteractionRule('baba_word', 'you_word'))


class BabaWordFlagWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BabaWordFlagWordInteractionRule('baba_word', 'flag_word'))


class BabaWordFlagObjInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BabaWordFlagObjInteractionRule('baba_word', 'flag_obj'))


class BabaWordWinWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BabaWordWinWordInteractionRule('baba_word', 'win_word'))


class BabaWordWonInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BabaWordWonInteractionRule('baba_word', 'won'))


class BabaWordLostInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BabaWordLostInteractionRule('baba_word', 'lost'))


class EmptyIsWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(EmptyIsWordInteractionRule('empty', 'is_word'))


class EmptyBabaObjInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        from itertools import product
        from copy import deepcopy
        from predicates import is_adjacent, is_unoccupied
        new_empty = deepcopy(state[self.entity_key1])
        new_baba_obj = deepcopy(state[self.entity_key2])
        delta = get_delta(action)
        for coord in state[self.entity_key2]:
            target_coord = (coord[0] + delta[0], coord[1] + delta[1])
            # Check if baba_obj is moving into an empty coordinate
            if is_unoccupied(state, target_coord):
                # Move baba_obj
                new_baba_obj.remove(coord)
                new_baba_obj.append(target_coord)
                # Remove this empty coordinate from current list of empties
                new_empty.remove(target_coord)
        return {self.entity_key1: new_empty, self.entity_key2: new_baba_obj}

interaction_rules.append(EmptyBabaObjInteractionRule('empty', 'baba_obj'))


class EmptyYouWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(EmptyYouWordInteractionRule('empty', 'you_word'))


class EmptyFlagWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(EmptyFlagWordInteractionRule('empty', 'flag_word'))


class EmptyFlagObjInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(EmptyFlagObjInteractionRule('empty', 'flag_obj'))


class EmptyWinWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(EmptyWinWordInteractionRule('empty', 'win_word'))


class EmptyWonInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(EmptyWonInteractionRule('empty', 'won'))


class EmptyLostInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(EmptyLostInteractionRule('empty', 'lost'))


class IsWordBabaObjInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        from itertools import product
        from copy import deepcopy

        new_state = deepcopy(state)
        # For each token of entity1, predict its interaction with each token of entity2
        # (Assumes updates are independent of each other, which is not always the case in general)
        for coord1, coord2 in product(state[self.entity_key1], state[self.entity_key2]):
            updates = push(new_state, action, {'name': self.entity_key1, 'coord': coord1}, {'name': self.entity_key2, 'coord': coord2})
            for key, val in updates.items():
                new_state[key] = val
        return new_state

interaction_rules.append(IsWordBabaObjInteractionRule('is_word', 'baba_obj'))


class IsWordYouWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(IsWordYouWordInteractionRule('is_word', 'you_word'))


class IsWordFlagWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(IsWordFlagWordInteractionRule('is_word', 'flag_word'))


class IsWordFlagObjInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(IsWordFlagObjInteractionRule('is_word', 'flag_obj'))


class IsWordWinWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(IsWordWinWordInteractionRule('is_word', 'win_word'))


class IsWordWonInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(IsWordWonInteractionRule('is_word', 'won'))


class IsWordLostInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(IsWordLostInteractionRule('is_word', 'lost'))


class BabaObjYouWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        from itertools import product
        from copy import deepcopy

        new_state = deepcopy(state)
        # For each token of entity1, predict its interaction with each token of entity2
        # (Assumes updates are independent of each other, which is not always the case in general)
        for coord1, coord2 in product(state[self.entity_key1], state[self.entity_key2]):
            updates = push(new_state, action, {'name': self.entity_key1, 'coord': coord1}, {'name': self.entity_key2, 'coord': coord2})
            for key, val in updates.items():
                new_state[key] = val
        return new_state

interaction_rules.append(BabaObjYouWordInteractionRule('baba_obj', 'you_word'))


class BabaObjFlagWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        from itertools import product
        from copy import deepcopy

        new_state = deepcopy(state)
        # For each token of entity1, predict its interaction with each token of entity2
        # (Assumes updates are independent of each other, which is not always the case in general)
        for coord1, coord2 in product(state[self.entity_key1], state[self.entity_key2]):
            updates = push(new_state, action, {'name': self.entity_key1, 'coord': coord1}, {'name': self.entity_key2, 'coord': coord2})
            for key, val in updates.items():
                new_state[key] = val
        return new_state

interaction_rules.append(BabaObjFlagWordInteractionRule('baba_obj', 'flag_word'))


class BabaObjFlagObjInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        from itertools import product
        from copy import deepcopy
        from predicates import check_rule, is_unoccupied

        new_state = deepcopy(state)
        flag_is_win = check_rule(state, ['flag_word', 'is_word', 'win_word'])
        # For each token of entity1, predict its interaction with each token of entity2
        # (Assumes updates are independent of each other, which is not always the case in general)
        for coord1, coord2 in product(state[self.entity_key1], state[self.entity_key2]):
            if flag_is_win:
                delta = get_delta(action)
                new_coord1 = (coord1[0] + delta[0], coord1[1] + delta[1])
                new_state['baba_obj'].remove(coord1)
                new_state['baba_obj'].append(new_coord1)
            else:
                updates = push(new_state, action, {'name': self.entity_key1, 'coord': coord1}, {'name': self.entity_key2, 'coord': coord2})
                for key, val in updates.items():
                    new_state[key] = val
        return new_state

interaction_rules.append(BabaObjFlagObjInteractionRule('baba_obj', 'flag_obj'))


class BabaObjWinWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        from itertools import product
        from copy import deepcopy

        new_state = deepcopy(state)
        # For each token of entity1, predict its interaction with each token of entity2
        # (Assumes updates are independent of each other, which is not always the case in general)
        for coord1, coord2 in product(state[self.entity_key1], state[self.entity_key2]):
            updates = push(new_state, action, {'name': self.entity_key1, 'coord': coord1}, {'name': self.entity_key2, 'coord': coord2})
            for key, val in updates.items():
                new_state[key] = val
        return new_state

interaction_rules.append(BabaObjWinWordInteractionRule('baba_obj', 'win_word'))


class BabaObjWonInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BabaObjWonInteractionRule('baba_obj', 'won'))


class BabaObjLostInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(BabaObjLostInteractionRule('baba_obj', 'lost'))


class YouWordFlagWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(YouWordFlagWordInteractionRule('you_word', 'flag_word'))


class YouWordFlagObjInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(YouWordFlagObjInteractionRule('you_word', 'flag_obj'))


class YouWordWinWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(YouWordWinWordInteractionRule('you_word', 'win_word'))


class YouWordWonInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(YouWordWonInteractionRule('you_word', 'won'))


class YouWordLostInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(YouWordLostInteractionRule('you_word', 'lost'))


class FlagWordFlagObjInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(FlagWordFlagObjInteractionRule('flag_word', 'flag_obj'))


class FlagWordWinWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(FlagWordWinWordInteractionRule('flag_word', 'win_word'))


class FlagWordWonInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(FlagWordWonInteractionRule('flag_word', 'won'))


class FlagWordLostInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(FlagWordLostInteractionRule('flag_word', 'lost'))


class FlagObjWinWordInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(FlagObjWinWordInteractionRule('flag_obj', 'win_word'))


class FlagObjWonInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(FlagObjWonInteractionRule('flag_obj', 'won'))


class FlagObjLostInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(FlagObjLostInteractionRule('flag_obj', 'lost'))


class WinWordWonInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(WinWordWonInteractionRule('win_word', 'won'))


class WinWordLostInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(WinWordLostInteractionRule('win_word', 'lost'))


class WonLostInteractionRule(BaseInteractionRule):
    def forward(self, state, action):
        return {self.entity_key1: state[self.entity_key1], self.entity_key2: state[self.entity_key2]}

interaction_rules.append(WonLostInteractionRule('won', 'lost'))
