"""
"""
import importlib
from pathlib import Path
from copy import deepcopy
import json
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
import ast


main_prompt = \
"""You are a model-based, RL-style agent. At each step, you choose an action to take in order to maximize
cumulative reward. In order to do that with a small number of samples, you need to also learn an explicit
model of the domain, which allows you to predict changes in state given your actions. By iteratively
improving your world model, you will be able to make better and better plans to maximize reward.

The 'state' argument will be of the form:
{state_format}

The set of possible actions:
{actions_set}

WORLD MODEL:
```python
{interaction_rules}

# PREDICATES
{predicates}

# OPERATORS
# (High-level operators for constructing plans)
{operators}
```
"""

evaluate_plan_prompt = main_prompt + \
"""
PLAN:
{plan}

LOG:
{log}

Examine the LOG for your PLAN above. The LOG was produced by simulating the PLAN
with your world model, and provides a guess about what will happen if you implement it.
E.g., the LOG might predict success or failure of an operator to achieve its desired effects.
Your job right now is to decide whether to reject or keep the plan. You should reject if
you think it is unlikely to work. Give a single-word response, Reject or Keep.
"""

get_relevant_rules_prompt = main_prompt + \
"""
GOAL:
{goal}

PLAN:
{plan}

CURRENT STATE:
{observation}

ACTION:
{action}

INSTRUCTIONS:
Of the interaction rules above, choose a subset that are essential for predicting the next
state transition, given the current state. Omit rules that you think
will predict no change or a change that is irrelevant for the goal and plan.

You MUST:
--List your selected rules like:
('entity_key1', 'entity_key2')
('entity_key1', 'entity_key3')
...
etc.
--List rules as tuples, i.e. with () not []
(I will use regular expressions to look for tuples of strings.)
"""

infer_interaction_rule_prompt = main_prompt + \
"""
INTERACTION RULE:
{interaction_rule}

OBSERVATIONS:
{observations}

INSTRUCTIONS:
Your job right now is to create a piece of code that serves as part of your world model.
You should rewrite the INTERACTION RULE so that its forward function is consistent with
the OBSERVATIONS.

You MUST:
--Put your code inside markup tags, as above, as this is the only place
I will look for it.
--Include a line of code that creates an instance of the class and appends it to the list `interaction_rules`, like:
interaction_rules.append(MyInteractionRule(entity1, entity2, state_keys_entity1, state_keys_entity2))
(but be sure to insert the correct name of the interaction rule from above). Assume `interaction_rules` already exists.
--Return a dict from the `forward` function, as in BaseInteractionRule, where keys are the entity keys.
"""

planner_prompt = main_prompt + \
"""
CURRENT STATE:
{current_state}

GOAL: {goal}

INSTRUCTIONS:
First, express the GOAL as a FOL formula composed of PREDICATES.
Then, form a high-level plan consisting of a sequence of intermediate steps,
expressed in terms of OPERATORS, in order to reach the GOAL. It should look like,

```python
# Goal
goal_state_str = "predicate(args)"  # Callable with exec
# Plan
actions = []
new_actions, new_state = operator1(args1)
actions.extend(new_actions)
new_actions, new_state = operator2(args2)
actions.extend(new_actions)
# etc...
```

IMPORTANT NOTES:
--Use the *absolute minimum* number of operators that you possibly can!! If your plan only needs one or two operators total, that's fine!
"""

"""
--You can propose new predicates and operators as needed!! The lists above may be incomplete.
If you propose a new one, define it below.
"""

debug_model_prompt = """
DEBUG:
state = {state}
model(state, {action})
{error}
"""


def extract_function_or_class_str(x, fname):
    """Extract code for function or class named 'fname' from string x, using AST parse and unparse"""
    tree = ast.parse(x)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == fname:
            return ast.unparse(node)
        elif isinstance(node, ast.ClassDef) and node.name == fname:
            return ast.unparse(node)
    return None

def extract_function_names(file_content):
    function_pattern = r'def\s+([^\(]+)\('
    matches = re.finditer(function_pattern, file_content)
    function_names = set(match.group(1).strip() for match in matches)
    return function_names


class TBRLAgent:
    """
    Theory-based RL agent.

    Factorizes world model into discrete set of interaction rules between
    object types and synthesizes code to predict next state given current state
    and action for interacting entities in each rule.

    Assumes Markov world.
    """
    def __init__(
        self,
        world_model_load_name=None,
        operators_load_name=None,
        predicates_load_name=None,
        # language_model='gpt-4',
        language_model='gpt-3.5-turbo',

        # language_model='gpt-4-turbo-preview',
        temperature=1.0,
        episode_length=20,
        do_revise_model=False,
        sparse_interactions=True,  # Only run subset of world model
        observation_memory_size=1,
        planner_explore_prob=0,
        max_replans=1,
    ):
        # Load BaseInteractionRule class from file
        with Path('base_interaction_rule.py').open('r') as fid:
            self.interaction_rule_base_class = fid.read()

        self.runtime_vars = {
            'interaction_rules': {},
            'interaction_rules_str': {},
            'error_msg_model': '',
            'observations': [],
            'revise_plan': False,
            'plan_str': '',
            'plan_log': '',
            'goal': 'Win',
            'goal_state_str': '',
            'operators': '',
            'predicates': '',
        }

        # Ablations
        self.do_revise_model = do_revise_model

        # Free model parameters
        self.sparse_interactions = sparse_interactions
        self.observation_memory_size = observation_memory_size
        self.planner_explore_prob = planner_explore_prob
        self.max_replans = max_replans

        # Prompts
        self.infer_interaction_rule_prompt = infer_interaction_rule_prompt
        self.get_relevant_rules_prompt = get_relevant_rules_prompt
        self.planner_prompt = planner_prompt
        self.evaluate_plan_prompt = evaluate_plan_prompt
        self.debug_model_prompt = debug_model_prompt

        # I/O
        self.world_model_save_name = '_model_tmp'
        self.world_model_load_name = world_model_load_name  # Possibly load existing model
        self.operators_save_name = '_operators_tmp'
        self.operators_load_name = operators_load_name
        self.predicates_save_name = '_predicates_tmp'
        self.predicates_load_name = predicates_load_name
        self.plan_save_name = '_plan_tmp'
        self.actions_set_save_name = '_actions_set_tmp'

        # Set up chat model
        self.language_model = language_model
        self.temperature = temperature
        chat = ChatOpenAI(
            model_name=self.language_model,
            temperature=temperature
        )
        self.query_lm = lambda prompt: chat(prompt.to_messages()).content
        self.episode_length = episode_length

        # Record episodes
        self.tape = [{}]

    def _make_langchain_prompt(self, text, **kwargs):
        x = HumanMessagePromptTemplate.from_template(text)
        chat_prompt = ChatPromptTemplate.from_messages([x])
        prompt = chat_prompt.format_prompt(**kwargs)
        return prompt

    def _get_state_deltas_str(self, state0, state1):
        """
        Highlight the changes in state resulting from last action
        """
        def _stringify(x, k=100):
            if hasattr(x, '__len__'):
                # Add ellipsis for entries of x beyond length k
                if len(x) > k:
                    return str(sorted(x[:k]))[:-1] + '...'
                else:
                    return str(sorted(x))
            else:
                return str(x)

        string = ''
        # Get set of unique keys between state0 and state1
        all_keys = set(state1.keys()).union(set(state0.keys()))
        for key in all_keys:
            val0 = state0.get(key)
            val1 = state1.get(key)
            if not self._eq(val1, val0):
                cond1 = (hasattr(val1, '__len__') and len(val1) > 2)
                cond2 = (hasattr(val0, '__len__') and len(val0) > 2)
                if cond1 or cond2:
                    # For long lists of coordinates, summarize by stating what
                    # was added or removed
                    added = []
                    removed = []
                    if not hasattr(val1, '__len__'):
                        added.append(val1)
                    else:
                        for x in val1:
                            if x not in val0:
                                added.append(x)
                    if not hasattr(val0, '__len__'):
                        removed.append(val0)
                    else:
                        for x in val0:
                            if x not in val1:
                                removed.append(x)
                    string += f'"{key}": Added: {added}\n'
                    string += f'"{key}": Removed: {removed}\n'
                else:
                    string += f'"{key}": {_stringify(val0)} --> {_stringify(val1)}\n'
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

    def _stringify(self, x, k=2):
        if hasattr(x, '__len__'):
            # Add ellipsis for entries of x beyond length k
            if len(x) > k:
                return str(sorted(x[:k]))[:-1] + '...'
            else:
                return str(sorted(x))
        else:
            return str(x)

    def _make_diff_string(self, pred, val, key):
        string = ""
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
                string += f'"{key}": predicted: {self._stringify(pred)}\n'
                string += f'"{key}": actual: {self._stringify(val)}\n'
        return string

    def _get_pred_errors(self, rule_key, state, predictions):
        vals = [state.get(e) for e in rule_key]
        preds = [predictions.get(e) for e in rule_key]
        diff_strs = [self._make_diff_string(pred, val, e) for pred, val, e in zip(preds, vals, rule_key)]
        diff_string = '\n'.join(diff_strs)
        return diff_string.strip()

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

    def _update_plan(self, text):
        x = re.findall(r'```python([\s\S]*?)```', text)
        if not len(x):
            return None, 'Exception: No code found'
        x = '\n'.join(x)
        self.runtime_vars['plan_str'] = x
        if x:
            state = self.runtime_vars['observations'][-1]
            with Path('_plan_vars_tmp_state.json').open('w') as fid:
                json.dump(state, fid)

            actions_path = '_plan_vars_tmp_actions'
            logger_path = '_plan_vars_tmp_logger'
            goal_state_str_path = '_plan_vars_tmp_goal_state_str'

            imports_str = f"import json\n"
            imports_str += f"from {self.predicates_save_name} import *\n"
            imports_str += f"from {self.operators_save_name} import *\n\n"
            imports_str += f"with open('_plan_vars_tmp_state.json', 'r') as fid:\n"
            imports_str += f"    state = json.load(fid)\n"
            save_str = f"\nactions_path = '{actions_path}'\n"
            save_str += f"logger_path = '{logger_path}'\n"
            save_str += f"goal_state_str_path = '{goal_state_str_path}'\n"
            save_str += "with open(actions_path, 'w') as fid:\n"
            save_str += "    fid.write(str(actions))\n"
            save_str += "with open(logger_path, 'w') as fid:\n"
            save_str += "    fid.write(str(logger))\n"
            save_str += "with open(goal_state_str_path, 'w') as fid:\n"
            save_str += "    fid.write(goal_state_str)\n"
            x1 = imports_str + x + save_str

            with Path(self.plan_save_name + '.py').open('w') as fid:
                fid.write(x1)

            import subprocess

            try:
                result = subprocess.run(['python', self.plan_save_name + '.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # exec(x)
            except Exception as e:
                return None, e
            else:
                # Detect runtime errors
                stderr = result.stderr.decode('utf-8')
                if result.returncode != 0:
                    return None, stderr

                with Path(actions_path).open('r') as fid:
                    actions = fid.read()
                try:
                    actions = eval(actions)
                except:
                    actions = []
                with Path(logger_path).open('r') as fid:
                    logger = fid.read()
                with Path(goal_state_str_path).open('r') as fid:
                    goal_state_str = fid.read()
                self.runtime_vars['goal_state_str'] = locals()['goal_state_str']
                self.runtime_vars['plan_log'] = logger

                return actions, None
        else:
            return None, 'Exception: No code found inside Python tags.'

    def _call_model_debug(self, rule_key, state, action, max_retries=5):
        for i in range(max_retries):
            try:
                preds = self.runtime_vars['interaction_rules'][rule_key].forward(state, action)
                return preds
            except Exception as e:
                from ipdb import set_trace; set_trace()
                prompt = self._make_langchain_prompt(
                    self.infer_interaction_rule_prompt + self.debug_model_prompt,
                    **{
                        'state_format': self.engine.state_format,
                        'actions_set': self.engine.actions_set,
                        'operators': self.runtime_vars['operators'].replace('{', '{{').replace('}', '}}'),
                        'predicates': self.runtime_vars['predicates'].replace('{', '{{').replace('}', '}}'),
                        'interaction_rules': '',  # TODO: Insert other rules into context?
                        'interaction_rule': self.runtime_vars['interaction_rules_str'][rule_key],
                        'observations': 'IGNORE',
                        'state': state,
                        'action': action,
                        'error': e,
                    }
                )
                print(f'DEBUG ITER {i}')
                print(f'ERROR: {e}')
                resp = self.query_lm(prompt)
                self.tape[-1]['debug_model_prompt'] = prompt.to_messages()[0].content
                self.tape[-1]['debug_model_response'] = resp
                print(resp)
                self.runtime_vars['error_msg_model'] = self._update_world_model(resp, list(self.runtime_vars['interaction_rules'].keys()))
        return

    def _generate_rule_stubs(self):
        """
        For each pair of object classes in observations, create a stub, if
        missing.
        The forward function is not overridden, and thus predicts no
        change in state.
        """
        from itertools import combinations

        def snake_to_camel(s):
            parts = s.split('_')
            camel_case_parts = [part.capitalize() for part in parts]
            return ''.join(camel_case_parts)

        exec(self.interaction_rule_base_class)
        interaction_rules = []
        classes = list(self.runtime_vars['observations'][-1].keys())
        for c1, c2 in combinations(classes, r=2):
            if (c1, c2) not in self.runtime_vars['interaction_rules_str'].keys():
                rule_name = f'{snake_to_camel(c1)}{snake_to_camel(c2)}'
                self.runtime_vars['interaction_rules_str'][(c1, c2)] = (
                    f"class {rule_name}InteractionRule(BaseInteractionRule):\n"
                    "    pass\n\n"
                    f"interaction_rules.append({rule_name}InteractionRule('{c1}', '{c2}'))\n"
                )
                exec(self.runtime_vars['interaction_rules_str'][(c1, c2)])
                self.runtime_vars['interaction_rules'][(c1, c2)] = interaction_rules.pop()

            if (c1, c2) not in self.replay_buffers.keys():
                self.replay_buffers[(c1, c2)] = []

    def _update_world_model(self, text, rule_keys, save_to_file=True):
        x = re.findall(r'```python([\s\S]*?)```', text)
        if not len(x):
            return 'Exception: No code found'
        x = '\n'.join([xi.strip() for xi in x])
        if x:
            interaction_rules = []  # Gets appended to in LLM-generated code
            try:
                exec(x, globals(), my_locals := {})
            except Exception as e:
                return e
            else:
                if not 'interaction_rules' in my_locals:
                    return 'Exception: Could not find interaction_rules'
                interaction_rules = my_locals['interaction_rules']
                if len(interaction_rules):
                    err_msg = ''
                    for rule in interaction_rules:
                        key = (rule.entity_key1, rule.entity_key2)
                        if key in rule_keys:
                            self.runtime_vars['interaction_rules'][key] = rule
                            s = extract_function_or_class_str(x, rule.__class__.__name__)
                            s += f"\n\ninteraction_rules.append({rule.__class__.__name__}('{key[0]}', '{key[1]}'))"
                            self.runtime_vars['interaction_rules_str'][key] = s
                        else:
                            err_msg += f'Exception: Could not find {key} in rule_keys.\n'
                    self._save_interaction_rules_to_file()
                    return None if not err_msg else err_msg
                else:
                    return 'Exception: Could not find any interaction rules'
        else:
            return 'Exception: No code found inside Python tags.'

    def _do_revise_model(self, error_count):
        # TODO: Consider fancier rule here
        if error_count > 0:
            return True
        return False

    def _do_revise_plan(self, error_count):
        if error_count > 0:
            return True
        return False

    def _extract_sparse_rules(self, resp):
        """
        Assume rules are given like:

        ('entity1', 'entity2')
        ('entity2', 'entity3')
        ...

        Return list of tuples of strings
        """
        rules = re.findall(r"\([\'\"]([\w\s]+)[\'\"], [\'\"]([\w\s]+)[\'\"]\)", resp)
        return rules

    def _get_relevant_rules(self, obs):
        """
        Get the set of interaction rules that are relevant to the current
        observation, if sparse_interactions == True, else return all rules.
        """
        if self.sparse_interactions:
            prompt = self._make_langchain_prompt(
                self.get_relevant_rules_prompt,
                **{
                    'state_format': self.engine.state_format,
                    'actions_set': self.engine.actions_set,
                    'operators': self.runtime_vars['operators'].replace('{', '{{').replace('}', '}}'),
                    'predicates': self.runtime_vars['predicates'].replace('{', '{{').replace('}', '}}'),
                    'interaction_rules': '\n\n'.join([
                        self.interaction_rule_base_class,
                        '\n\n'.join(self.runtime_vars['interaction_rules_str'].values())
                    ]),
                    'goal': self.runtime_vars['goal'],
                    'plan': self.runtime_vars['plan_str'],
                    'observation': obs[0],
                    'action': obs[1],
                }
            )
            resp = self.query_lm(prompt) 
            relevant_rules = self._extract_sparse_rules(resp)
            print(resp)
            self.tape[-1]['relevant_rules_prompt'] = prompt.to_messages()[0].content
            self.tape[-1]['relevant_rules_response'] = resp
        else:
            relevant_rules = self.runtime_vars['interaction_rules'].keys()
        return relevant_rules

    def _update_replay_buffers(self, obs):
        """
        Update replay buffers for each rule.

        This matters most in the case of sparse_interactions == True, since
        every observed transition will not be relevant to every rule.
        """

        if self.sparse_interactions:
            # Prompt for subset of interaction rules
            relevant_rules = self._get_relevant_rules(obs)
            for key in self.replay_buffers.keys():
                if key in relevant_rules:
                    self.replay_buffers[key].append(obs)
        else:
            for key in self.replay_buffers.keys():
                self.replay_buffers[key].append(obs)

    def _make_observation_summaries(self, rule_key, obs, errors):
        s0, a, s1 = obs
        s0_rule = {key: val for key, val in s0.items() if key in rule_key}
        s1_rule = {key: val for key, val in s1.items() if key in rule_key}
        return (
            f"Initial state: {s0}\n"
            f"Action: {a}\n"
            f"Next state: {s1}\n"
            f"Summary of changes:\n{self._get_state_deltas_str(s0_rule, s1_rule)}"
            f"Your prediction errors:\n{errors}\n"
        )

    def _choose_synthesis_examples(self, rule_key):
        """
        Choose (s0, a) --> s1 transitions from replay buffer as program
        synthesis examples.

        TODO: Make this fancier (e.g. choose most important examples somehow)
        """
        # Simple solution: Just take last k from buffer
        obs = self.replay_buffers[rule_key][::-1][:self.observation_memory_size]
        preds = [self._call_model_debug(rule_key, s0, a) for (s0, a, s1) in obs]
        errors = [self._get_pred_errors(rule_key, s1, pred) for (s0, a, s1), pred in zip(obs, preds)]
        examples = [self._make_observation_summaries(rule_key, x, e) for x, e in zip(obs, errors)]
        error_count = sum([1 if e else 0 for e in errors])
        return examples, error_count

    def _revise_world_model(self):
        """
        (Re-)synthesize world model given examples, including an observed
        transition and any prediction errors under current world model
        """
        if not self.do_revise_model:
            return

        self.tape[-1]['revision_prompts'] = {}
        self.tape[-1]['revision_responses'] = {}
        for key, rule in self.runtime_vars['interaction_rules'].items():
            examples, error_count = self._choose_synthesis_examples(key)
            if self._do_revise_model(error_count):
                # Prompt to update model for this rule
                prompt = self._make_langchain_prompt(
                    self.infer_interaction_rule_prompt,
                    **{
                        'state_format': self.engine.state_format,
                        'actions_set': self.engine.actions_set,
                        'interaction_rules': '',  # Consider inserting other rules into context as well
                        'interaction_rule': self.runtime_vars['interaction_rules_str'][key],
                        'observations': '\n\n'.join(examples),
                        'operators': self.runtime_vars['operators'].replace('{', '{{').replace('}', '}}'),
                        'predicates': self.runtime_vars['predicates'].replace('{', '{{').replace('}', '}}'),
                    }
                )
                resp = self.query_lm(prompt)
                self.runtime_vars['error_msg_model'] = self._update_world_model(resp, [key])
                self.tape[-1]['revision_prompts'][key] = prompt.to_messages()[0].content
                self.tape[-1]['revision_responses'][key] = resp
                print(prompt.to_messages()[0].content)
                print(resp)
                if self._do_revise_plan(error_count):
                    self.runtime_vars['revise_plan'] = True

    def _revise_operators(self):
        # TODO
        pass
        return

    def _revise_predicates(self):
        # TODO
        pass
        return

    # def _get_tested_rules(self):
    #     return '\n'.join([self.runtime_vars['interaction_rules_str'][key] for key in self.tested_interaction_rules])

    def _random_explore(self):
        return [random.choice(self.actions_set)]    

    def _sample_exploratory_goal(self, state, model):
        raise NotImplementedError()
        # prompt = self._make_langchain_prompt(
        #     self.exploratory_goal_prompt,  # TODO
        #     **{
        #         'interaction_rules': '\n'.join(self.runtime_vars['interaction_rules_str'].values()),
        #         'state_format': self.engine.state_format,
        #         'actions_set': self.engine.actions_set,
        #         'current_state': self.runtime_vars['observations'][-1],
        #     }
        # )
        # resp = self.query_lm(prompt)
        # return resp

    def _sample_plan(self, state, goal):
        """
        Generate plan as series of operators
        """
        prompt = self._make_langchain_prompt(
            self.planner_prompt,
            **{
                'state_format': self.engine.state_format,
                'actions_set': self.engine.actions_set,
                'operators': self.runtime_vars['operators'].replace('{', '{{').replace('}', '}}'),
                'predicates': self.runtime_vars['predicates'].replace('{', '{{').replace('}', '}}'),
                'interaction_rules': '\n'.join(self.runtime_vars['interaction_rules_str'].values()),
                'current_state': state,
                'goal': goal,
            }
        )

        resp = self.query_lm(prompt)
        actions, error_msg = self._update_plan(resp)
        if error_msg is None:
            # Record data to tape
            self.tape[-1]['planner_prompt'] = prompt.to_messages()[0].content
            self.tape[-1]['planner_response'] = resp
            print(prompt.to_messages()[0].content)
            print(resp)
        else:
            print('PLANNER ERROR:', error_msg)
            self.tape[-1]['planner_err'] = error_msg
        if not actions:
            actions = self._random_explore()
        return actions

    def _keep_plan(self):
        """Prompt LLM to keep or reject plan it generated."""
        return True  # DEBUG
        # prompt = self._make_langchain_prompt(
        #     self.evaluate_plan_prompt,
        #     **{
        #         'state_format': self.engine.state_format,
        #         'actions_set': self.engine.actions_set,
        #         'interaction_rules': '\n'.join(self.runtime_vars['interaction_rules_str'].values()),
        #         'operators': self.runtime_vars['operators'].replace('{', '{{').replace('}', '}}'),
        #         'predicates': self.runtime_vars['predicates'].replace('{', '{{').replace('}', '}}'),
        #         'plan': self.runtime_vars['plan_str'],
        #         'log': str(self.runtime_vars['plan_log']),
        #     }
        # )
        # resp = self.query_lm(prompt)
        # if resp.startswith('Reject'):
        #     return False
        # else:
        #     return True

    def _get_plan_feedback(self):
        state = self.runtime_vars['observations'][-1]
        try:
            goal_reached = eval(self.runtime_vars['goal_state_str'])
        except Exception as e:
            self.runtime_vars['plan_feedback'] = e
        else:
            if goal_reached:
                self.runtime_vars['plan_feedback'] = 'Goal reached!'
            else:
                self.runtime_vars['plan_feedback'] = 'Goal was not reached.'

    def _hierarchical_planner(self, mode):
        if mode == 'exploit':
            goal = 'Win the level'
        else:
            goal = self._sample_exploratory_goal(self.runtime_vars['observations'][-1])

        for i in range(self.max_replans):
            actions = self._sample_plan(self.runtime_vars['observations'][-1], goal)
            if self._keep_plan():
                break

        for action in actions:
            yield action

    def _sample_planner_mode(self):
        if random.choices(
            [0, 1],
            weights=[1 - self.planner_explore_prob, self.planner_explore_prob]
        )[0]:
            mode = 'explore'
        else:
            mode = 'exploit'
        return mode

    def step_env(self, action):

        # Step the game engine and append to history
        self.engine.step(action)
        self.runtime_vars['observations'].append(deepcopy(self.engine.get_obs()))
        self.actions.append(action)
        # self._make_observation_summaries()  # Formatted for LLM prompts

        # Create new stubs if new entities observed
        self._generate_rule_stubs()

        # Update replay buffers
        self._update_replay_buffers((
            self.runtime_vars['observations'][-2],
            self.actions[-1],
            self.runtime_vars['observations'][-1]
        ))

        self.tape[-1]['action'] = action
        self.tape[-1]['observation'] = deepcopy(self.runtime_vars['observations'][-1])
        self.tape[-1]['world_model'] = self.runtime_vars['interaction_rules_str']

    def _load_world_model(self, world_model_load_name=None, operators_load_name=None, predicates_load_name=None):
        if world_model_load_name:
            with Path(world_model_load_name + '.py').open('r') as fid:
                text = fid.read()
            
            # Note: this will omit any interaction rules that aren't auto-
            # generated when creating stubs. Consider generating separate file
            # to list them (TODO).
            keys = list(self.runtime_vars['interaction_rules_str'].keys())
            err_msg = self._update_world_model("```python\n" + text + "\n```", keys)

            # FIXME: Grab any auxiliary functions defined inside model file and make sure they're saved to tmp file as well


        if operators_load_name:
            with Path(operators_load_name + '.py').open('r') as fid:
                self.runtime_vars['operators'] = fid.read()

        if predicates_load_name:
            with Path(predicates_load_name + '.py').open('r') as fid:
                self.runtime_vars['predicates'] = fid.read()
        
        # Save model-related info to tmp files, to be loaded when model is called
        self._save_interaction_rules_to_file()
        self._save_operators_to_file()
        self._save_predicates_to_file()
        self._save_actions_set_to_file()

    def _save_actions_set_to_file(self):
        with Path(self.actions_set_save_name + '.py').open('w') as fid:
            fid.write(f"actions_set = {self.actions_set}")

    def _save_operators_to_file(self):
        with Path(self.operators_save_name + '.py').open('w') as fid:
            fid.write(self.runtime_vars['operators'].replace('{{', '{').replace('}}', '}'))

    def _save_predicates_to_file(self):
        with Path(self.predicates_save_name + '.py').open('w') as fid:
            fid.write(self.runtime_vars['predicates'].replace('{{', '{').replace('}}', '}'))

    def _save_interaction_rules_to_file(self):
            # Save initialized model to file
            rules = self.interaction_rule_base_class
            rules += '\n\n'.join(self.runtime_vars['interaction_rules_str'].values())

            # Extract auxilary funciton names from the world model file to the model tmp file 
            function_names = set()
            if self.world_model_load_name:
                with Path(self.world_model_load_name + '.py').open('r') as fid:
                    file_content = fid.read()
                    function_names = extract_function_names(file_content)
                    # print(function_names)

            # Filter out methods you don't want to import
            function_names = [func for func in function_names if not (func.startswith('__') or func == 'forward')]

            # Write import statements for the extracted function names into model tmp file
            import_statements = '\n'.join(f"from {self.world_model_load_name} import {func}" for func in function_names)

            # print(import_statements)
            rules = import_statements + '\n\n' + rules

            with Path(self.world_model_save_name + '.py').open('w') as fid:
                fid.write(rules)

    def reset(self, keep_model=True):
        self.engine.reset()
        self.runtime_vars['revise_plan'] = False
        self.actions_set = engine.actions_set
        self.runtime_vars['observations'] = [self.engine.get_obs().copy()]
        self.actions = []
        self.replay_buffers = {}
        self._generate_rule_stubs()

        if not keep_model:
            self._load_world_model(
                self.world_model_load_name,
                self.operators_load_name,
                self.predicates_load_name
            )

    def run(self, engine, max_iters=10):
        self.engine = engine
        self.reset(keep_model=False)

        for i in range(max_iters):
            # Initialize
            self.reset(keep_model=True)

            mode = self._sample_planner_mode()
            plan = self._hierarchical_planner(mode)
            for action in plan:
                self.step_env(action)

                # Exit if agent won
                if self.engine.won:
                    self.tape[-1]['exit_condition'] = 'won'
                    return True

                # Reset things if agent lost
                if self.engine.lost:
                    self.reset(keep_model=True)
                    self.tape[-1]['exit_condition'] = 'lost'
                    break

                self._revise_world_model()
                if self.runtime_vars['revise_plan']:
                    # Revise plan when model is wrong (with probability eps)
                    self.runtime_vars['revise_plan'] = False  # Reset flag
                    break

            self._get_plan_feedback()  # TODO (Insert info about failures into main prompt next iteration)
            self._revise_predicates()  # TODO
            self._revise_operators()  # TODO
        return False


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--game', type=str, default='baba')
    parser.add_argument('--levels', type=str, default="[('demo_LEVELS', 1)]")
    parser.add_argument('--episode-length', type=int, default=20)
    parser.add_argument('--world-model-file-name', type=str, default='model_demo_level2')
    parser.add_argument('--operators-file-name', type=str, default='operators')
    parser.add_argument('--predicates-file-name', type=str, default='predicates')
    parser.add_argument('--learn-model', action='store_true')
    args = parser.parse_args()

    levels = eval(args.levels)

    for level_set, level_id in levels:
        if args.game == 'baba':
            engine = BabaIsYou(level_set=level_set, level_id=level_id)
        elif args.game == 'lava':
            engine = LavaGrid()
        agent = TBRLAgent(
            episode_length=args.episode_length,
            world_model_load_name=args.world_model_file_name,
            operators_load_name=args.operators_file_name,
            predicates_load_name=args.predicates_file_name,
            do_revise_model=args.learn_model,
        )
        agent.run(engine)

    # Save tape to json
    import time
    import json
    tape_path = f'tapes/{args.game}_{level_set}_{level_id}_{time.time()}.json'
    Path(tape_path).parent.mkdir(parents=True, exist_ok=True)
    # tapekeys = ['planner_err', 'relevant_rules_prompt', 'relevant_rules_response', 'action', 'observation', 'world_model']
    # for key in tapekeys:
    #     print(type(agent.tape[0][key]))
    # agent.tape[0]['observation'] = str(agent.tape[0]['observation'])
    # agent.tape[0]['world_model'] = str(agent.tape[0]['world_model'])

    # agent.tape[0]['observation'] = json.loads(agent.tape[0]['observation'])
    # agent.tape[0]['world_model'] = json.loads(agent.tape[0]['world_model'])

    # print(agent.tape[0]['observation'])
    # print(agent.tape[0]['world_model'])

    # print(agent.tape[0].keys())
    # print(agent.tape[0].get('observation'))
    # print(agent.tape[0]['observation'].valuees)
    # print(agent.tape[0]['world_model'])

    # world_model_tuple2string = agent[0].tape[0]['world_model']
    agent.tape[0]['world_model'] =  {str(k): v for k, v in agent.tape[0]['world_model'].items()}

    with open(tape_path, 'w') as f:
        json.dump(agent.tape, f, indent=4)
