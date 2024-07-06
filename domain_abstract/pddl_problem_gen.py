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

    # Create the PDDL problem file content
    pddl = f"(define (problem {level_name})\n"
    pddl += "    (:domain babadomain_abstract_v5)\n\n"
    pddl += "    (:objects\n"
    for loc in locations:
        pddl += f"        {loc} - location\n"
    for word in word_names:
        pddl += f"        {word} - word\n"
    for obj in obj_names:
        pddl += f"        {obj} - object\n"
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

    # Function to check for formed rules
    def check_rule_formation(entity_locations):
        rules = []
        loc_to_word = {}
        for word, (x, y) in entity_locations.items():
            if '_word' in word:
                loc_to_word[(x, y)] = word
        
        for x in range(10):
            for y in range(10):
                # Check horizontal alignment
                if (x, y) in loc_to_word and (x + 1, y) in loc_to_word and (x + 2, y) in loc_to_word:
                    rules.append((loc_to_word[(x, y)], loc_to_word[(x + 1, y)], loc_to_word[(x + 2, y)]))
                # Check vertical alignment from top to bottom
                if (x, y) in loc_to_word and (x, y + 1) in loc_to_word and (x, y + 2) in loc_to_word:
                    rules.append((loc_to_word[(x, y)], loc_to_word[(x, y + 1)], loc_to_word[(x, y + 2)]))
        return rules

    # Formed rules section
    rules = check_rule_formation(entity_locations)
    if rules:
        pddl += "\n         ; formed rules\n\n"
        for rule in rules:
            if entity_locations[rule[0]][0] == entity_locations[rule[1]][0] == entity_locations[rule[2]][0]:  # Vertical alignment
                pddl += f"        (rule_formed {rule[2]} {rule[1]} {rule[0]})\n"
            else:
                pddl += f"        (rule_formed {rule[0]} {rule[1]} {rule[2]})\n"

    # Unoccupied locations section
    pddl += "\n       ; occupancies section\n\n"
    for i in range(10):
        for j in range(10):
            loc = f"loc-{i}-{j}"
            occupied = False
            for key, value in words.items():
                if [i, j] in value:
                    occupied = True
            for key, value in objects.items():
                if [i, j] in value:
                    occupied = True
            if occupied:
                pddl += f"        ; (unoccupied {loc})\n"
            else:
                pddl += f"        (unoccupied {loc})\n"

    # Adjacency definition section (this never changes)
    pddl += "\n         ; define adjacencies section\n\n"
    for i in range(9):
        pddl += f"        (adjacent loc-0-{i} loc-0-{i+1} vertical)\n"
        pddl += f"        (adjacent loc-0-{i} loc-1-{i} horizontal)\n"
        pddl += f"        (adjacent loc-0-{i+1} loc-0-{i} vertical)\n"
    pddl += f"        (adjacent loc-0-9 loc-0-8 vertical)\n"
    pddl += f"        (adjacent loc-0-9 loc-1-9 horizontal)\n"

    for row in range(1, 10):
        for col in range(10):
            if col > 0:
                pddl += f"        (adjacent loc-{row}-{col} loc-{row}-{col-1} vertical)\n"
            if col < 9:
                pddl += f"        (adjacent loc-{row}-{col} loc-{row}-{col+1} vertical)\n"
            if row < 9:
                pddl += f"        (adjacent loc-{row}-{col} loc-{row+1}-{col} horizontal)\n"
            if row > 0:
                pddl += f"        (adjacent loc-{row}-{col} loc-{row-1}-{col} horizontal)\n"

    pddl += "\n    )\n\n"
    pddl += "    (:goal (and\n"
    pddl += "        ; Specify your goal here\n"
    pddl += "    ))\n"
    pddl += ")"

    return pddl

# Example usage:
state_dict = {"border": [[0, 9], [0, 8], [0, 7], [0, 6], [0, 5], [0, 4], [0, 3], [0, 2], [0, 1], [0, 0], [1, 9], [1, 0], [2, 9], [2, 0], [3, 9], [3, 0], [4, 9], [4, 0], [5, 9], [5, 0], [6, 9], [6, 0], [7, 9], [7, 0], [8, 9], [8, 0], [9, 9], [9, 8], [9, 7], [9, 6], [9, 5], [9, 4], [9, 3], [9, 2], [9, 1], [9, 0]], "empty": [[1, 8], [1, 7], [1, 5], [1, 4], [1, 3], [1, 1], [2, 8], [2, 7], [2, 5], [2, 4], [2, 3], [2, 1], [3, 8], [3, 5], [3, 3], [3, 1], [4, 8], [4, 7], [4, 5], [4, 4], [4, 3], [4, 2], [4, 1], [5, 8], [5, 7], [5, 5], [5, 4], [5, 3], [5, 2], [5, 1], [6, 8], [6, 5], [6, 3], [6, 2], [7, 8], [7, 7], [7, 5], [7, 4], [7, 3], [7, 2], [8, 8], [8, 7], [8, 2]], "wall_obj": [[1, 6], [2, 6], [3, 6], [4, 6], [5, 6], [6, 6], [7, 6], [8, 6]], "baba_word": [[1, 2]], "is_word": [[2, 2], [7, 1], [8, 4]], "keke_obj": [[3, 7]], "keke_word": [[3, 4]], "you_word": [[3, 2]], "flag_obj": [[6, 7]], "baba_obj": [[6, 4]], "flag_word": [[6, 1]], "wall_word": [[8, 5]], "stop_word": [[8, 3]], "win_word": [[8, 1]], "won": False, "lost": False}

pddl_content = generate_pddl_problem(state_dict, "level14")
print(pddl_content)

def save_pddl_to_file(pddl_content, filename):
    with open(filename, 'w') as file:
        file.write(pddl_content)
    print(f"PDDL problem file saved as {filename}")

save_pddl_to_file(pddl_content, "level14.pddl")
