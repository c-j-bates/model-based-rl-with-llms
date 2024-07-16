import os

def generate_adjacent_rules(rows, cols):
    rules = ""
    for row in range(rows):
        rules += f"        ;row {row + 1}\n"
        for col in range(cols - 1):
            rules += f"         (adjacent loc-{col}-{row} loc-{col+1}-{row} horizontal)\n"
    return rules

# Function to check for formed rules
def check_rule_formation(entity_locations):
    abstract_rules = set()
    granular_rules = []
    loc_to_word = {}
    for word, (x, y) in entity_locations.items():
        if '_word' in word or '_obj' in word:
            loc_to_word[(x, y)] = word

    for x in range(10):
        for y in range(10):
            # Check horizontal alignment
            if (x, y) in loc_to_word and (x + 1, y) in loc_to_word and (x + 2, y) in loc_to_word:
                granular_rule = (loc_to_word[(x, y)], loc_to_word[(x + 1, y)], loc_to_word[(x + 2, y)])
                granular_rules.append(granular_rule)
                abstract_rules.add((granular_rule[0].split('_')[0], granular_rule[1].split('_')[0], granular_rule[2].split('_')[0]))
            # Check vertical alignment
            if (x, y) in loc_to_word and (x, y + 1) in loc_to_word and (x, y + 2) in loc_to_word:
                granular_rule = (loc_to_word[(x, y)], loc_to_word[(x, y + 1)], loc_to_word[(x, y + 2)])
                granular_rules.append(granular_rule)
                abstract_rules.add((granular_rule[0].split('_')[0], granular_rule[1].split('_')[0], granular_rule[2].split('_')[0]))
    return abstract_rules, granular_rules

def generate_pddl_problem(state_dict, level_name="level"):
    # Define the locations and orientations
    locations = [f"loc-{i}-{j}" for i in range(10) for j in range(10)]
    orientations = ["horizontal", "vertical"]

    # Initialize objects and words from the state dictionary
    objects = {}
    words = {}
    for key, value in state_dict.items():
        if key.endswith("_obj"):
            objects[key] = value
        elif key.endswith("_word"):
            words[key] = value

    # Generate object names with enumeration for multiple instances
    obj_names = []
    word_names = []
    for key, value in objects.items():
        for i in range(len(value)):
            obj_names.append(f"{key}_{i+1}")

    for key, value in words.items():
        for i in range(len(value)):
            word_names.append(f"{key}_{i+1}")

    # Create sets for unique superclass objects
    unique_words = {key.split('_')[0] for key in objects.keys()}.union({key.split('_')[0] for key in words.keys()})

    # Create the PDDL problem file content
    pddl = f"(define (problem {level_name})\n"
    pddl += "    (:domain baba)\n\n"
    pddl += "    (:objects\n"
    for loc in locations:
        pddl += f"        {loc} - location\n"
    for word in word_names:
        pddl += f"        {word} - word_instance\n"
    for obj in obj_names:
        pddl += f"        {obj} - object_instance\n"
    for word in unique_words:
        pddl += f"        {word} - word\n"
    for ori in orientations:
        pddl += f"        {ori} - orientation\n"
    pddl += "    )\n\n"
    
    # Initialize locations for entities
    pddl += "    (:init\n\n"
    pddl += "         ;; Initial locations for entities\n"
    entity_locations = {}
    for key, value in words.items():
        for i, (x, y) in enumerate(value):
            entity_name = f"{key}_{i+1}"
            entity_locations[entity_name] = (x, y)
            pddl += f"        (at {entity_name} loc-{x}-{y})\n"
    for key, value in objects.items():
        for i, (x, y) in enumerate(value):
            entity_name = f"{key}_{i+1}"
            entity_locations[entity_name] = (x, y)
            pddl += f"        (at {entity_name} loc-{x}-{y})\n"

    # Formed rules section
    abstract_rules, granular_rules = check_rule_formation(entity_locations)
    if abstract_rules:
        pddl += "\n         ; formed rules\n\n"
        for rule in abstract_rules:
            pddl += f"        (rule_formed {rule[0]} {rule[1]} {rule[2]})\n"

    # Control rules section
    if granular_rules:
        pddl += "\n         ; control rules\n\n"
        for abstract_rule in abstract_rules:
            if abstract_rule[1] == 'is' and abstract_rule[2] == 'you':
                object_prefix = abstract_rule[0]
                for obj in obj_names:
                    if obj.startswith(object_prefix):
                        pddl += f"        (control_rule {obj} is you)\n"

    # Commented granular rules
    if granular_rules:
        pddl += "\n         ; fully granular rules (commented)\n\n"
        for granular_rule in granular_rules:
            pddl += f"        ; (rule_formed {granular_rule[0]} {granular_rule[1]} {granular_rule[2]})\n"

    pddl += "\n    )\n\n"
    pddl += "    (:goal (and\n"
    pddl += "        ; Specify your goal here\n"
    pddl += "     "
    pddl += "    ))\n"
    pddl += ")"

    return pddl

if __name__ == "__main__": 

    # Example usage:
    state_dict =  {"border": [[0, 9], [0, 8], [0, 7], [0, 6], [0, 5], [0, 4], [0, 3], [0, 2], [0, 1], [0, 0], [1, 9], [1, 0], [2, 9], [2, 0], [3, 9], [3, 0], [4, 9], [4, 0], [5, 9], [5, 0], [6, 9], [6, 0], [7, 9], [7, 0], [8, 9], [8, 0], [9, 9], [9, 8], [9, 7], [9, 6], [9, 5], [9, 4], [9, 3], [9, 2], [9, 1], [9, 0]], "baba_word": [[1, 8]], "empty": [[1, 7], [1, 6], [1, 5], [1, 4], [1, 3], [1, 2], [1, 1], [2, 7], [2, 6], [2, 4], [2, 3], [2, 2], [2, 1], [3, 7], [3, 6], [3, 5], [3, 4], [3, 3], [3, 2], [3, 1], [4, 8], [4, 7], [4, 6], [4, 5], [4, 4], [4, 2], [4, 1], [5, 8], [5, 7], [5, 6], [5, 5], [5, 4], [5, 3], [5, 2], [5, 1], [6, 7], [6, 6], [6, 5], [6, 4], [6, 3], [6, 2], [6, 1], [7, 7], [7, 6], [7, 4], [7, 3], [7, 2], [8, 7], [8, 6], [8, 5], [8, 4], [8, 3], [8, 2]], "is_word": [[2, 8], [7, 8], [7, 1]], "baba_obj": [[2, 5]], "you_word": [[3, 8]], "rock_word": [[4, 3]], "flag_word": [[6, 8], [8, 1]], "rock_obj": [[7, 5]], "win_word": [[8, 8]], "won": False, "lost": False}
    
    pddl_content = generate_pddl_problem(state_dict, "lvtest")
    print(pddl_content)

    def save_pddl_to_file(pddl_content, filename):
        with open(filename, 'w') as file:
            file.write(pddl_content)
        print(f"PDDL problem file saved as {filename}")

    save_pddl_to_file(pddl_content, "lvtest.pddl")
