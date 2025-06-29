from grade7_problems import Grade7ProblemGenerator
import random
import json
from datetime import datetime
import os

def generate_integer_worksheet(count=10, difficulty='hard'):
    """Generate a worksheet focused on integer problems."""
    generator = Grade7ProblemGenerator()
    problems = []
    
    print(f"Generating {count} integer problems at {difficulty} difficulty...")
    
    # Define weights for different types of integer problems
    problem_weights = {
        'operation': 4,         # Basic operations
        'word': 3,              # Word problems
        'property': 2,          # Integer properties
        'ordering': 1,          # Ordering integers
        'absolute_value': 1,    # Absolute value problems
        'temperature': 1,       # Temperature change problems
        'elevation': 1,         # Elevation problems
        'money': 1,             # Money-related problems
        'sequence': 1,          # Number sequence problems
        'average': 1            # Average problems
    }
    
    # Generate problems
    for _ in range(count):
        # Choose problem type based on weights
        problem_type = random.choices(
            list(problem_weights.keys()),
            weights=list(problem_weights.values()),
            k=1
        )[0]
        
        try:
            if problem_type == 'operation':
                problem, answer = generator._generate_integer_operation(difficulty)
            elif problem_type == 'property':
                problem, answer = generator._generate_integer_property(difficulty)
            elif problem_type == 'word':
                problem, answer = generator._generate_integer_word_problem(difficulty)
            elif problem_type == 'temperature':
                problem, answer = generator._generate_temperature_problem(difficulty)
            elif problem_type == 'elevation':
                problem, answer = generator._generate_elevation_problem(difficulty)
            elif problem_type == 'money':
                problem, answer = generator._generate_money_problem(difficulty)
            elif problem_type == 'sequence':
                problem, answer = generator._generate_sequence_problem(difficulty)
            elif problem_type == 'average':
                problem, answer = generator._generate_average_problem(difficulty)
            elif problem_type == 'ordering':
                problem, answer = generator._generate_integer_ordering(difficulty)
            elif problem_type == 'absolute_value':
                problem, answer = generator._generate_absolute_value_problem(difficulty)
            
            problems.append({
                'problem': problem,
                'answer': answer,
                'type': f'integer_{problem_type}'
            })
            
        except Exception as e:
            print(f"Error generating {problem_type} problem: {e}")
            continue
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"integer_worksheet_{timestamp}.json"
    filepath = os.path.join('data', filename)
    
    with open(filepath, 'w') as f:
        json.dump({
            'topic': 'Integers',
            'difficulty': difficulty,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'problems': problems
        }, f, indent=2)
    
    print(f"Integer worksheet saved to: {filepath}")
    return filepath

def main():
    # Generate a worksheet with 15 integer problems at hard difficulty
    generate_integer_worksheet(count=15, difficulty='hard')

if __name__ == "__main__":
    main()
