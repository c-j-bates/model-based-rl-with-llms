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
