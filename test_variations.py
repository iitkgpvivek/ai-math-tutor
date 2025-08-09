#!/usr/bin/env python3
"""
Test script to generate variations for a random problem from the problems directory.
"""
import os
import json
import random
from problem_importer import ProblemImporter

def load_random_problem():
    """Load a random problem from the problems directory."""
    problems_dir = os.path.join('data', 'problems')
    problem_files = [f for f in os.listdir(problems_dir) if f.endswith('.json')]
    
    if not problem_files:
        print("No problem files found in the problems directory.")
        return None
    
    # Select a random problem file
    selected_file = random.choice(problem_files)
    file_path = os.path.join(problems_dir, selected_file)
    
    with open(file_path, 'r') as f:
        problem_data = json.load(f)
    
    return problem_data, selected_file

def test_variations():
    """Test generating variations for a random problem."""
    # Load a random problem
    problem_data, filename = load_random_problem()
    if not problem_data:
        return
    
    problem_text = problem_data.get('original_question', '')
    problem_type = problem_data.get('type', 'Integers')
    
    print("=" * 80)
    print(f"Testing variations for problem from: {filename}")
    print("-" * 40)
    print("ORIGINAL PROBLEM:")
    print(problem_text)
    print("\n" + "=" * 80 + "\n")
    
    # Initialize the problem importer
    importer = ProblemImporter()
    
    # Generate 3 variations
    print("GENERATING 3 VARIATIONS...\n")
    variations = importer.generate_variations(
        problem_text=problem_text,
        problem_type=problem_type,
        num_variations=3
    )
    
    # Print the variations
    for i, variation in enumerate(variations, 1):
        print(f"VARIATION {i}:")
        print(variation['text'])
        print(f"\nExplanation: {variation['explanation']}")
        print("\n" + "-" * 40 + "\n")

if __name__ == "__main__":
    test_variations()
