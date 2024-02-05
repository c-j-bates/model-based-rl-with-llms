import importlib
from pathlib import Path
from copy import deepcopy
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import random
import re
from games import LavaGrid, BabaIsYou


main_prompt = \
"""You are a model-based, RL-style agent. At each step, you choose an action to take in order to maximize
cumulative reward. In order to do that with small number of samples, you need to also learn an explicit
model of the domain, which allows you to predict changes in state given your actions. By iteratively
improving your world model, you will be able to make better and better plans to maximize reward.

WORLD MODEL:
{world_model}

"""

create_world_model_prompt = main_prompt + \
"""Your job right now is to create a piece of code that serves as a world model.
This world model must be a Python function called 'model', which takes in an initial state
and an action, and returns the next state. E.g.,

```python
def model(state, action):
    new_state = some_transform(state, action)
    return new_state
```

The 'state' argument will be of the form:
{state_format}

The set of possible actions:
{actions_set}

Observations:
{observations}

You must put your code inside markup tags, as above, as this is the only place
I will look for it.
"""

generate_subgoals_prompt = main_prompt + \
"""
The 'state' argument will be of the form:
{state_format}

The set of possible actions:
{actions_set}

Current state:
{current_state}

Now that you have a world model, you can think about what you need to do to win.
First, think: What do you notice about the current state? What do you think you need to
do to win? Break your plan down into a sequence of intermediate steps or subgoals.
Then for each one, write a Python function that takes in a set of observations and
checks if the subgoal has been reached. For example,
```python
subgoals = [
    lambda state: state['baba_obj'][0] == state['flag_obj'][0],  # Baba is on same column as flag
    lambda state: state['flag_obj'][1] == state['other_obj'][1] and state['other_obj'][0] > 1,  # Flag is at same row as some other object, and other object is in column greater than 1
    ...
]
```
Note the above checkers are not a good example of how to solve the level.
They're just to give you a sense of what we're after.

You MUST name your subgoals as above! I will look for a list of lambda expressions named 'subgoals'!
If necessary, you can also define functions to call inside the lambda expressions.
"""

create_planner_prompt = main_prompt + \
"""
The 'state' argument will be of the form:
{state_format}

The set of possible actions:
{actions_set}

Current state:
{current_state}

Current goal:
Make this expression return True:
```python
{subgoal}
```

Your job right now is to create a piece of code that serves as an action policy to achieve
the above goal, starting from the current state.
Your function should be written in Python, e.g.:

```python
def planner(state):
    # Some code that produces a sequence of actions to achieve subgoal,
    # starting from state
    actions = func(state)
    return actions
```

You must put your code inside markup tags, as above, as this is the only place
I will look for it.
"""

reflect_prompt = main_prompt + \
"""
"""

debug_model_prompt = """
state = {state}
model(state, {action})
{error}
"""

debug_planner_prompt = """
state = {state}
planner(state)
{error}
"""


class Agent:
    def __init__(
        self,
        language_model='gpt-4',
        # language_model='gpt-4-turbo-preview',
        temperature=1.0,
        episode_length=20,
        observation_memory_size=1,
    ):
        self.model = None
        self.model_str = ''
        self.planner = None
        self.planner_str = ''
        self.observation_memory_size = observation_memory_size
        self.obs_summaries = []
        self.subgoals = []
        self.subgoals_index = 0
        self.search_algorithm = 'dfs'

        # Prompts
        self.create_world_model_prompt = create_world_model_prompt
        self.generate_subgoals_prompt = generate_subgoals_prompt
        self.create_planner_prompt = create_planner_prompt
        self.debug_planner_prompt = debug_planner_prompt
        self.debug_model_prompt = debug_model_prompt
        self.reflect_prompt = reflect_prompt

        # Save names
        self.world_model_save_name = '_model_tmp'
        self.planner_save_name = '_planner_tmp'
        self.subgoals_save_name = '_subgoals_tmp'

        # Set up chat model
        self.language_model = language_model
        self.temperature = temperature
        chat = ChatOpenAI(
            model_name=self.language_model,
            temperature=temperature,
        )
        self.query_lm = lambda prompt: chat(prompt.to_messages()).content
        self.episode_length = episode_length

        # Record episodes
        self.tape = []

    def enumerative_search(self, max_depth=5):
        """
        Search for win state according to specified algorithm cutting off at
        max_depth
        """
        won = False
        if self.search_algorithm == 'bfs':
            # Breadth-first search
            raise NotImplementedError()
        elif self.search_algorithm == 'dfs':
            # Depth-first search
            start = ()
            states = {start: deepcopy(self.observations[-1])}
            stack = [start]
            while stack:
                node = stack.pop()

                if states[node].get('won'):  # Model predicts win
                    won = True
                    break

                if len(node) > max_depth:
                    # print('MAX DEPTH REACHED')
                    continue

                # Build adjacency graph dynamically to only include actions
                # that change the state of the game in some way (e.g. don't
                # keep running into a wall), and are valid
                for a in self.actions_set:
                    state = self._call_model_debug(deepcopy(states[node]), a)
                    if state is not None and state != states[node] and not state.get('lost'):
                        new_node = node + (a,)
                        states[new_node] = deepcopy(state)
                        stack.append(new_node)
            actions = list(node)
            return actions, won
        else:
            NotImplementedError()

    def _do_revise_model(self, eps=1.0):
        """
        Revise world model with probability epsilon if it makes incorrect
        prediction.
        """
        if not self.model:
            return True
        if self._get_pred_errors():
            if random.choices([0, 1], weights=[1 - eps, eps]):
                return True
            else:
                return False
        return False

    def _get_obs_summary(self):
        if self.observation_memory_size is None:
            summary = '\n\n'.join(self.obs_summaries)
        else:
            # Take last k steps in history, as a simple heuristic
            summary = '\n\n'.join(self.obs_summaries[-self.observation_memory_size:])
        return summary

    def _get_obs_deltas_str(self):
        """
        Highlight the changes in state resulting from last action
        """
        def _stringify(x, k=2):
            if hasattr(x, '__len__'):
                # Add ellipsis for entries of x beyond length k
                if len(x) > k:
                    return str(sorted(x[:k]))[:-1] + '...'
                else:
                    return str(sorted(x))
            else:
                return str(x)

        if len(self.observations) < 2:
            return ''

        string = ''
        # Get set of unique keys between from last two steps
        all_keys = set(self.observations[-1].keys()).union(
            set(self.observations[-2].keys())
        )
        for key in all_keys:
            val0 = self.observations[-2].get(key)
            val = self.observations[-1].get(key)
            if not self._eq(val, val0):
                cond1 = (hasattr(val, '__len__') and len(val) > 2)
                cond2 = (hasattr(val0, '__len__') and len(val0) > 2)
                if cond1 or cond2:
                    # For long lists of coordinates, summarize by stating what
                    # was added or removed
                    added = []
                    removed = []
                    if not hasattr(val, '__len__'):
                        added.append(val)
                    else:
                        for x in val:
                            if x not in val0:
                                added.append(x)
                    if not hasattr(val0, '__len__'):
                        removed.append(val0)
                    else:
                        for x in val0:
                            if x not in val:
                                removed.append(x)
                    string += f'"{key}": Added: {added}\n'
                    string += f'"{key}": Removed: {removed}\n'
                else:
                    string += f'"{key}": {_stringify(val0)} --> {_stringify(val)}\n'
        return string

    def _eq(self, x, y):
        if (
            hasattr(x, '__len__') and
            hasattr(y, '__len__') and
            set(x) == set(y)
        ):
            # Ignore ordering and possible repetitions on coordinates
            return True
        else:
            return x == y

    def _get_pred_errors(self):

        def _stringify(x, k=2):
            if hasattr(x, '__len__'):
                # Add ellipsis for entries of x beyond length k
                if len(x) > k:
                    return str(sorted(x[:k]))[:-1] + '...'
                else:
                    return str(sorted(x))
            else:
                return str(x)

        if not self.predictions or not self.predictions[-1]:
            return 'None'

        all_keys = set(self.observations[-1].keys()).union(
            set(self.predictions[-1].keys())
        )
        string = ""
        for key in all_keys:
            val = self.observations[-1].get(key)
            pred = self.predictions[-1].get(key)
            if not self._eq(val, pred):
                cond1 = hasattr(val, '__len__') and len(val) > 2
                cond2 = hasattr(pred, '__len__') and len(pred) > 2
                if cond1 or cond2:
                    # If lists are long, only state what was missing or extraneous
                    missing = []
                    extra = []
                    if not hasattr(val, '__len__'):
                        missing.append(val)
                    else:
                        for x in val:
                            if x not in pred:
                                missing.append(x)
                    if not hasattr(pred, '__len__'):
                        extra.append(pred)
                    else:
                        for x in pred:
                            if x not in val:
                                extra.append(x)
                    string += f'"{key}": Missing: {missing}\n'
                    string += f'"{key}": extraneous: {extra}\n'
                else:
                    # If list of coords is short, just print both in full
                    string += f'"{key}": predicted: {_stringify(pred)}\n'
                    string += f'"{key}": actual: {_stringify(val)}\n'
        return string

    def _get_abbreviated_observations(self, obs, cutoff=3):
        init_state_abbreviated = {}
        string = '{'
        for j, (key, val) in enumerate(obs.items()):
            string += f'{key}: '
            if not hasattr(val, '__len__'):
                string += f'{val}'
            else:
                string += '['
                for i, v in enumerate(val[:cutoff]):
                    string += f'{v}'
                    if i < cutoff - 1 and len(val) > i + 1:
                        string += ', '
                if len(val) > cutoff:
                    string += ', ...'
                string += ']'
            if j < len(obs) - 1:
                string += ', '
        string += '}'
        return string

    def _check_subgoal(self, idx):
        """
        Check if most recent observation satisfies the current subgoal
        """
        if not self.subgoals:
            return False

        if idx > len(self.subgoals):
            # Attempted all subgoals and still didn't win
            return False

        try:
            result = self.subgoals[idx - 1](self.observations[-1])
        except Exception as e:
            print('SUBGOALS ERROR:', e)
            self.tape[-1]['subgoals_err'] = e
            result = None
        if not type(result) is bool:
            return False
        return result

    def _update_subgoals(self, text):
        import ast
        def find_functions(node):
            functions = []
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.Lambda):
                    # Convert the lambda expression back into a string
                    lambda_str = ast.unparse(child)
                    functions.append(lambda_str)
                elif isinstance(child, ast.FunctionDef):
                    # Convert the function definition back into a string
                    func_str = ast.unparse(child)
                    functions.append(func_str)
                else:
                    functions.extend(find_functions(child))
            return functions


        x = re.findall(r'```python([\s\S]*?)```', text)
        if not len(x):
            return 'Exception: No code found'
        x = x[0].strip()
        if x:
            try:
                exec(x)
            except Exception as e:
                return e
            else:
                if 'subgoals' in locals():
                    # Update to new subgoals
                    self.subgoals = locals()['subgoals']
                    self.subgoals_str = x
                    self.subgoals_str_list = find_functions(ast.parse(x))
                    if len(self.subgoals_str_list) != len(self.subgoals):
                        return (
                            'Exception: String extraction of subgoals returned'
                            ' different number of subgoals than exec'
                        )
                    with Path(self.subgoals_save_name + '.py').open('w') as fid:
                        fid.write(x)
                    return None
                else:
                    return 'Exception: Could not find function named "subgoals"'
        else:
            return 'Exception: No code found inside Python tags.'

    def _update_planner(self, text):
        x = re.findall(r'```python([\s\S]*?)```', text)
        if not len(x):
            return 'Exception: No code found'
        x = x[0].strip()
        if x:
            try:
                exec(x)
            except Exception as e:
                return e
            else:
                if 'planner' in locals():
                    # Update to new planner
                    self.planner = locals()['planner']
                    self.planner_str = x
                    with Path(self.planner_save_name + '.py').open('w') as fid:
                        fid.write(x)
                    return None
                else:
                    return 'Exception: Could not find function named "planner"'
        else:
            return 'Exception: No code found inside Python tags.'

    def _call_model_debug(self, state, action, max_retries=5):
        for i in range(max_retries):
            try:
                import _model_tmp
                importlib.reload(_model_tmp)  # Get newest version
                from _model_tmp import model
                pred = model(state, action)
                return pred
            except Exception as e:
                prompt = self._make_langchain_prompt(
                    self.create_world_model_prompt + self.debug_model_prompt,
                    **{
                        'world_model': self.model_str,
                        'observations': self._get_obs_summary(),
                        'state_format': self.engine.state_format,
                        'actions_set': self.engine.actions_set,
                        'state': state,
                        'action': action,
                        'error': e,
                    }
                )
                print(f'DEBUG ITER {i}')
                print(f'ERROR: {e}')
                resp = self.query_lm(prompt)
                print(resp)
                error_msg = self._update_world_model(resp)
        return

    def _update_world_model(self, text):
        x = re.findall(r'```python([\s\S]*?)```', text)
        if not len(x):
            return 'Exception: No code found'
        x = '\n'.join([xi.strip() for xi in x])
        if x:
            try:
                exec(x)
            except Exception as e:
                return e
            else:
                if 'model' in locals():
                    # Update to new world model
                    self.model = locals()['model']
                    self.model_str = x
                    with Path(self.world_model_save_name + '.py').open('w') as fid:
                        fid.write(x)
                    return None
                else:
                    return 'Exception: Could not find function named "model"'
        else:
            return 'Exception: No code found inside Python tags.'

    def _call_planner_debug(self, state, max_retries=5):
        # locals()['model'] = self.model  # Make world model callable inside planner with 'model(...'
        for i in range(max_retries):
            try:
                import _planner_tmp
                importlib.reload(_planner_tmp)  # Get newest version
                from _planner_tmp import planner
                import _model_tmp  # Planner might use model, so import
                importlib.reload(_model_tmp)
                from _model_tmp import model
                action = planner(state)
                if not hasattr(action, '__len__'):
                    action = [action]
                return action
            except Exception as e:
                prompt = self._make_langchain_prompt(
                    self.create_planner_prompt + self.debug_planner_prompt,
                    **{  # TODO: Fix: State is used twice
                        'world_model': self.model_str,
                        'state_format': self.engine.state_format,
                        'actions_set': self.engine.actions_set,
                        'subgoal': self.subgoals_str_list[self.subgoals_index - 1],
                        'current_state': state,
                        'state': state,
                        'error': e,
                    }
                )
                print(f'DEBUG ITER {i}')
                print(f'ERROR: {e}')
                resp = self.query_lm(prompt)
                print(resp)
                error_msg = self._update_planner(resp)
        return

    def _revise_world_model(self):
        obs_abbr0 = self._get_abbreviated_observations(
            self.observations[-2]
        )
        obs_abbr1 = self._get_abbreviated_observations(
            self.observations[-1]
        )
        self.obs_summaries.append(
            (
                f"Initial state: {obs_abbr0}\n"
                f"Action: {self.actions[-1]}\n"
                f"Next state: {obs_abbr1}\n"
                f"Summary of changes:\n{self._get_obs_deltas_str()}"
                f"Your prediction errors:\n{self._get_pred_errors()}\n"
            )
        )
        if self.model is None:
            prompt = self._make_langchain_prompt(
                self.create_world_model_prompt,
                **{
                    'world_model': 'None yet',
                    'observations': self._get_obs_summary(),
                    'state_format': self.engine.state_format,
                    'actions_set': self.engine.actions_set,
                }
            )
        else:
            prompt = self._make_langchain_prompt(
                self.create_world_model_prompt,
                **{
                    'world_model': self.model_str,
                    'observations': self._get_obs_summary(),
                    'state_format': self.engine.state_format,
                    'actions_set': self.engine.actions_set,
                }
            )
        resp = self.query_lm(prompt)
        self.error_msg = self._update_world_model(resp)
        self.tape[-1]['revision_prompt'] = prompt.to_messages()[0].content
        self.tape[-1]['revision_response'] = resp
        print(prompt.to_messages()[0].content)
        print(resp)

    def _reflect(self):
        # TODO
        # prompt = self._make_langchain_prompt(
        #     self.reflect_prompt,
        #     **{
        #         'world_model': self.model_str,
        #         'observations': self._get_obs_summary(),
        #         'state_format': self.engine.state_format,
        #         'actions_set': self.engine.actions_set,
        #     }
        # )
        # resp = self.query_lm(prompt)
        # self.error_msg = self._update_world_model(resp)
        # self.tape[-1]['reflect_prompt'] = prompt.to_messages()[0].content
        # self.tape[-1]['reflect_response'] = resp
        # print(prompt.to_messages()[0].content)
        # print(resp)
        pass

    def _random_explore(self):
        return [random.choice(self.actions_set)]    

    def _directed_explore(self):
        if self.model is None:
            return self._random_explore()

        # Check if current subgoal was achieved (and skip subsequent ones that
        # have also already been achieved in current state, e.g. you might also
        # achieve the next subgoal "for free" by accident).
        # If not, regenerate subgoals.
        if self._check_subgoal(self.subgoals_index):
            idx = self.subgoals_index
            while self._check_subgoal(idx):
                idx += 1
            self.subgoals_index = idx
        else:
            self.subgoals_index = 0
            # Reflect on why the plan didn't work (TODO)
            self._reflect()

        if not self.subgoals_index:
            # Generate subgoals (hierarchical plan)
            prompt = self._make_langchain_prompt(
                self.generate_subgoals_prompt,
                **{
                    'world_model': self.model_str,
                    'state_format': self.engine.state_format,
                    'actions_set': self.engine.actions_set,
                    'current_state': self.observations[-1],
                }
            )
            resp = self.query_lm(prompt)
            error_msg = self._update_subgoals(resp)
            if error_msg is None:
                self.subgoals_index = 1
                # Record data to tape
                self.tape[-1]['subgoals_prompt'] = prompt.to_messages()[0].content
                self.tape[-1]['subgoals_response'] = resp
                print(prompt.to_messages()[0].content)
                print(resp)
            else:
                print('PLANNING ERROR:', error_msg)
                self.tape[-1]['planner_err'] = error_msg
                return self._random_explore()

        # Make planner for current subgoal
        prompt = self._make_langchain_prompt(
            self.create_planner_prompt,
            **{
                'world_model': self.model_str,
                'state_format': self.engine.state_format,
                'actions_set': self.engine.actions_set,
                'current_state': self.observations[-1],
                'subgoal': self.subgoals_str_list[self.subgoals_index - 1],
            }
        )
        resp = self.query_lm(prompt)
        error_msg = self._update_planner(resp)
        self.tape[-1]['planner_prompt'] = prompt.to_messages()[0].content
        self.tape[-1]['planner_response'] = resp
        print(prompt.to_messages()[0].content)
        print(resp)

        actions = self._call_planner_debug(self.observations[-1])
        if not actions:
            return self._random_explore()
        return actions

    def _make_langchain_prompt(self, text, **kwargs):
        x = HumanMessagePromptTemplate.from_template(text)
        chat_prompt = ChatPromptTemplate.from_messages([x])
        prompt = chat_prompt.format_prompt(**kwargs)
        return prompt

    def step_env(self, action):

        # Get agent's prediction
        if self.model is None:
            self.predictions.append(None)
        else:
            # Assume markov environments with no latent states
            # TODO: Accommodate non-Markov world models
            self.predictions.append(
                self._call_model_debug(self.observations[-1], action)
            )
        # Step the game engine and append to history
        self.engine.step(action)
        self.observations.append(deepcopy(self.engine.get_obs()))
        self.actions.append(action)

        self.tape.append({})
        self.tape[-1]['action'] = action
        self.tape[-1]['observation'] = deepcopy(self.observations[-1])
        self.tape[-1]['predictions'] = deepcopy(self.predictions[-1])
        self.tape[-1]['world_model'] = self.model_str
        self.tape[-1]['planner'] = self.planner_str

    def reset(self, keep_model=True):
        self.engine.reset()
        self.actions_set = engine.actions_set
        self.observations = [self.engine.get_obs().copy()]
        self.actions = []
        self.predictions = []
        self.full_action_history = []  # For detecting perseveration
        self.outcomes = []
        if not keep_model:
            self.model = None  # Hypothesized transition model
            self.model_str = ''  # String repr of model code

    def run(self, engine, keep_model=True):
        """
        Roll out an episode
        """
        self.engine = engine
        self.reset(keep_model=keep_model)

        for i in range(self.episode_length):
            if self.model is None:
                # No world model yet on first step
                actions = self._random_explore()
            elif not len(actions):
                # First try simple enumerative search, and if win state not
                # found, then try directed exploration
                actions, win_predicted = self.enumerative_search()
                if not actions or not win_predicted:
                    actions = self._directed_explore()

            # Take the sampled action and update engine
            self.step_env(actions.pop(0))

            # Exit if agent won
            if self.engine.won:
                print('WON THE GAME!!!')
                self.tape[-1]['exit_condition'] = 'won'
                break

            if self._do_revise_model():
                self._revise_world_model()

            # Reset things if agent lost
            if self.engine.lost:
                print('LOST THE GAME :(((')
                self.reset(keep_model=True)
                self.tape[-1]['exit_condition'] = 'lost'


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--game', type=str, default='baba')
    parser.add_argument('--levels', type=str, default="[('demo_LEVELS', 1)]")
    parser.add_argument('--episode-length', type=int, default=20)
    args = parser.parse_args()

    levels = eval(args.levels)

    for level_set, level_id in levels:
        if args.game == 'baba':
            engine = BabaIsYou(level_set=level_set, level_id=level_id)
        elif args.game == 'lava':
            engine = LavaGrid()
        agent = Agent(episode_length=args.episode_length)
        agent.run(engine)

    # Save tape to json
    import time
    import json
    tape_path = f'tapes/{args.game}_{level_set}_{level_id}_{time.time()}.json'
    Path(tape_path).parent.mkdir(parents=True, exist_ok=True)
    with open(tape_path, 'w') as f:
        json.dump(agent.tape, f, indent=4)
