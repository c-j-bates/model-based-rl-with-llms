from copy import deepcopy
from itertools import product
from utils import push, get_delta

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
        from utils import push, get_delta

        # Retrieve current coordinate of 'baba_obj'
        baba_obj_coord = state['baba_obj'][0]
        
        # Calculate new coordinate based on action
        delta = get_delta(action)
        new_coord = (baba_obj_coord[0] + delta[0], baba_obj_coord[1] + delta[1])

        # Check if new coordinate is within the borders
        if new_coord not in state['border']:
            # Move baba_obj to new coordinate if within borders
            state['baba_obj'] = [new_coord]
        
        # Return the updated state for 'baba_obj' and 'border'
        return {'border': state['border'], 'baba_obj': state['baba_obj']}

# Create an instance of the interaction rule and append it to the interaction_rules list
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
        from utils import push, get_delta

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
        from copy import deepcopy
        from utils import get_delta, is_unoccupied
        
        # Make deep copies of the relevant parts of the state        
        new_empty = deepcopy(state[self.entity_key1])
        new_baba_obj = deepcopy(state[self.entity_key2])
        delta = get_delta(action)
        
        # Process each 'baba' object
        for coord in state[self.entity_key2]:
            target_coord = (coord[0] + delta[0], coord[1] + delta[1])
            
            # Ensure the target position is unoccupied and valid (not outside the grid)
            if is_unoccupied(state, target_coord) and target_coord not in state['border']:
                new_baba_obj.remove(coord)
                new_baba_obj.append(target_coord)
                new_empty.remove(target_coord)
                new_empty.append(coord)

        print("HERE IS DEEPCOPY OF STATES")
        print(new_empty)
        print(new_baba_obj)
                
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
        from utils import push, get_delta


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
        from utils import push, get_delta

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
        from utils import push, get_delta

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
        from utils import push, get_delta

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
        from utils import push, get_delta

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
