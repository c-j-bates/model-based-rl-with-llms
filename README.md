# Playing Baba is You with LLM agents and theory-based RL

[Project under development.]

## Usage

Run agents using:
```bash
python tbrl.py [args]
```

Agent can be warm-started with models by pointing to files using args. E.g., to load interaction rules stored in model_demo_level2.py, operators in operators.py, predicates in predicates.py, and to play KekeCompetition's demo level 2, run:

```bash
python tbrl.py --world-model-file-name model_demo_level2 --operators-file-name operators --predicates-file-name predicates --game baba --levels [('demo_LEVELS', 1)]
```

Note these are also the current default args. By default, world model learning is turned off, so the agent only generates plans. It can be turned on by supplying the '--learn-model' flag.

Note that this implementation is incomplete, including the model learning part of the algorithm. Logic for learning predicates and operators still needs implementing.
