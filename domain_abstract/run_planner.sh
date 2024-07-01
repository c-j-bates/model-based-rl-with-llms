#!/bin/bash

# Define the output file
output_file="plans_output.txt"

# Clear the output file
> "$output_file"

# Define the levels
levels=("level1.pddl" "level2.pddl" "level3.pddl" "level4.pddl" "level5.pddl" "level6.pddl")

# Loop through each level and run the command
for level in "${levels[@]}"; do
    echo "Running plan for $level..."
    # Run the command
    python bfws.py baba3.pddl "$level" k-BFWS
    
    # Check if execution.details file exists and is not empty
    if [[ -s execution.details ]]; then
        echo "-----------------------------------" >> "$output_file"
        echo "Plan for $level" >> "$output_file"
        echo "-----------------------------------" >> "$output_file"
        
        # Append the contents of execution.details to the output file
        cat execution.details >> "$output_file"
        echo "" >> "$output_file"
    else
        echo "No execution details found for $level" >> "$output_file"
    fi
done

echo "All plans have been saved to $output_file"
