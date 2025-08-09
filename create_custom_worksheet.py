#!/usr/bin/env python3
"""
Create a custom worksheet with word problems from different categories.
Uses dedicated word problem generators directly for better quality and consistency.
"""
import os
import json
import random
from datetime import datetime
from integer_word_problem_generators import IntegerWordProblemGenerator
from fractions_word_problem_generators import FractionWordProblemGenerator
from simple_equations_generators import SimpleEquationsGenerator
from generate_pdf import create_pdf

def is_placeholder(problem_text):
    """Check if a problem text is a placeholder."""
    if not problem_text or not isinstance(problem_text, str):
        return True
    
    # List of phrases that indicate a placeholder problem
    placeholder_phrases = [
        'not implemented',
        'coming soon',
        'TODO',
        'placeholder',
        'not available'
    ]
    
    return any(phrase in problem_text.lower() for phrase in placeholder_phrases)

def get_problem_pattern(problem_text, problem_type):
    """Extract a pattern from the problem text to identify similar problems."""
    if not problem_text or not problem_type:
        return None
        
    # For operation sequence problems (like the ones in the example)
    if 'divide' in problem_text.lower() and 'add' in problem_text.lower() and 'multiply' in problem_text.lower():
        # Extract the operation sequence pattern
        operations = []
        if 'divide' in problem_text.lower():
            operations.append('D')
        if 'add' in problem_text.lower():
            operations.append('A')
        if 'multiply' in problem_text.lower():
            operations.append('M')
        if 'subtract' in problem_text.lower():
            operations.append('S')
        return f"operation_sequence_{'_'.join(operations)}"
        
    # For baking/recipe problems
    if 'batch' in problem_text.lower() and 'cups' in problem_text.lower():
        return "baking_recipe_division"
        
    # Default to problem_type if no specific pattern matches
    return problem_type

def generate_integer_problems(count=10, max_attempts=5):
    """Generate integer word problems using the dedicated generator."""
    generator = IntegerWordProblemGenerator()
    problems = []
    attempts = 0
    
    # Get all problem generation methods
    problem_methods = [
        ('temperature', generator._generate_temperature_problem, 1.0),
        ('elevation', generator._generate_elevation_problem, 1.0),
        ('money', generator._generate_money_problem, 1.5),
        ('sequence', generator._generate_sequence_problem, 1.0),
        ('average', generator._generate_average_problem, 1.0),
        ('quiz_scoring', generator._generate_quiz_scoring_problem, 1.2),
        ('sports', generator._generate_sports_games_problem, 1.2),
        ('financial', generator._generate_financial_problem, 1.3),
        ('academic', generator._generate_academic_competition_problem, 1.2),
        ('real_world', generator._generate_real_world_problem, 1.1),
        ('advanced', generator._generate_advanced_challenge_problem, 0.8),
        ('classroom', generator._generate_classroom_problem, 1.0),
        ('puzzle', generator._generate_puzzle_problem, 0.9),
        ('multi_step', generator._generate_multi_step_problem, 1.1),
        ('assessment', generator._generate_assessment_problem, 0.9),
        ('real_life', generator._generate_real_life_scenario, 1.0),
        ('time_zone', generator._generate_time_zone_problem, 0.7),
        ('height_change', generator._generate_height_change_problem, 0.7),
        ('game_scoring', generator._generate_game_scoring_problem, 1.0)
    ]
    
    method_names, methods, weights = zip(*problem_methods)
    
    while len(problems) < count and attempts < max_attempts * count:
        try:
            # Set all integer problems to hard difficulty
            difficulty = 'hard'
            
            # Randomly select a problem type based on weights
            method_idx = random.choices(range(len(methods)), weights=weights, k=1)[0]
            method = methods[method_idx]
            method_name = method_names[method_idx]
            
            # Generate the problem
            problem, answer = method(difficulty)
            
            # Skip if problem is None, answer is None, or it's a placeholder
            if not problem or answer is None or is_placeholder(problem):
                attempts += 1
                continue
                
            # Skip if we've seen this problem before
            if any(p['problem'] == problem for p in problems):
                attempts += 1
                continue
                
            problems.append({
                'problem': problem,
                'answer': answer,
                'type': 'integer',
                'difficulty': difficulty,
                'subtype': method_name
            })
            
        except Exception as e:
            print(f"Warning: Error generating integer problem: {e}")
            attempts += 1
            continue
            
        attempts += 1
    
    if len(problems) < count:
        print(f"Warning: Only generated {len(problems)}/{count} unique integer problems after {attempts} attempts")
    
    return problems

def generate_fraction_problems(count=10, max_attempts=5):
    """Generate fraction word problems using the dedicated generator."""
    generator = FractionWordProblemGenerator()
    problems = []
    attempts = 0
    
    # Define problem types and their weights (for variety)
    problem_types = [
        ('_generate_recipe_problem', 2),
        ('_generate_sharing_problem', 2),
        ('_generate_addition_problem', 1.5),
        ('_generate_subtraction_problem', 1.5),
        ('_generate_multiplication_problem', 1.5),
        ('_generate_division_problem', 1.5),
        ('_generate_comparison_problem', 1),
        ('_generate_conversion_problem', 1),
        ('_generate_mixed_operations_problem', 1.5),
        ('_generate_measurement_problem', 1.5)
    ]
    
    while len(problems) < count and attempts < max_attempts * count:
        try:
            # Randomly select problem type based on weights
            problem_funcs, weights = zip(*problem_types)
            selected_func = random.choices(problem_funcs, weights=weights, k=1)[0]
            
            # Set all integer problems to hard difficulty
            difficulty = 'hard'
            
            # Generate the problem
            problem, answer = getattr(generator, selected_func)(difficulty)
            
            # Skip if we've seen this problem before
            if any(p['problem'] == problem for p in problems):
                attempts += 1
                continue
                
            if problem is not None and answer is not None:
                problems.append({
                    'problem': problem,
                    'answer': answer,
                    'type': 'fraction',
                    'difficulty': difficulty,
                    'subtype': selected_func.replace('_generate_', '').replace('_', ' ')
                })
                
        except Exception as e:
            print(f"Warning: Error generating fraction problem: {e}")
            
        attempts += 1
    
    if len(problems) < count:
        print(f"Warning: Only generated {len(problems)}/{count} unique fraction problems after {attempts} attempts")
    
    return problems

def generate_simple_equations_problems(count=10, max_attempts=5, exclude_types=None):
    """Generate simple equations word problems using the dedicated generator.
    
    Args:
        count: Number of problems to generate
        max_attempts: Maximum number of attempts to generate unique problems
        exclude_types: Set of problem types to exclude from generation
    """
    generator = SimpleEquationsGenerator()
    problems = []
    attempts = 0
    used_types = set()
    
    # List of available problem types (intermediate difficulty)
    problem_types = [
        'age_related_sum',
        'age_related_difference',
        'age_related_ratio',
        'number',
        'consecutive_integers',
        'money_basic',
        'money_discount',
        'rectangle_perimeter',
        'rectangle_area',
        'square_perimeter',
        'square_area',
        'triangle_perimeter',
        'triangle_area',
        'circle_circumference',
        'circle_area',
        'shopping',
        'drt_basic',
        'work_rate_basic'
    ]
    
    # Filter out excluded types
    if exclude_types:
        problem_types = [pt for pt in problem_types if pt not in exclude_types]
    
    # Make a copy to avoid modifying the original list
    available_types = problem_types.copy()
    
    while len(problems) < count and attempts < max_attempts * count and available_types:
        attempts += 1
        try:
            # Select a random problem type from remaining available types
            if not available_types:
                break
                
            problem_type = random.choice(available_types)
            
            # Generate problem with intermediate difficulty
            problem = generator.generate_problem(
                problem_type=problem_type,
                difficulty='intermediate'
            )
            
            # Debug print
            print(f"Generated problem type: {problem_type}")
            print(f"Problem statement: {problem.statement[:100]}..." if problem.statement else "No statement")
            
            # Convert problem to the expected format
            problem_dict = {
                'problem': problem.statement,  # Using statement to match the Problem class
                'answer': problem.answer,
                'solution': '\n'.join(problem.solution_steps) if problem.solution_steps else '',
                'type': 'simple_equations',
                'subtype': problem_type,  # Use the selected problem_type to ensure consistency
                'difficulty': problem.difficulty
            }
            
            # Check if this is a valid problem (not a placeholder, has all required fields, and type not used)
            if (not is_placeholder(problem_dict['problem']) and 
                problem_dict['problem'] and 
                problem_dict['answer'] is not None and
                problem_type not in used_types):
                
                # Add to used types and remove from available types
                used_types.add(problem_type)
                if problem_type in available_types:
                    available_types.remove(problem_type)
                
                problems.append(problem_dict)
                print(f"✓ Added problem type: {problem_type}")
                
                # If we've used all types, reset available types (but keep track of used types)
                if not available_types and len(problems) < count:
                    print("All problem types used, recycling types...")
                    available_types = [pt for pt in problem_types if pt not in used_types]
                
        except Exception as e:
            print(f"Error generating simple equations problem: {e}")
    
    if len(problems) < count:
        print(f"Warning: Only generated {len(problems)}/{count} unique simple equations problems after {attempts} attempts")
    
    return problems

def generate_problems(topics=None, total_problems=20):
    """Generate problems from specified topics with even distribution.
    
    Args:
        topics: List of topic names to include. If None, uses all available.
        total_problems: Total number of problems to generate.
    
    Returns:
        List of problem dictionaries.
    """
    # Define available topic generators and their weights
    topic_generators = {
        'integer': (generate_integer_problems, 1.0),
        'fraction': (generate_fraction_problems, 1.0),
        'simple_equations': (generate_simple_equations_problems, 1.0),
        # Add new topics here as they become available
        # 'geometry': (generate_geometry_problems, 1.0),
    }
    
    # Use all available topics if none specified
    if topics is None:
        topics = list(topic_generators.keys())
    else:
        # Filter to only include available topics
        topics = [t for t in topics if t in topic_generators]
        if not topics:
            raise ValueError("No valid topics specified")
    
    # Calculate problems per topic
    problems_per_topic = total_problems // len(topics)
    remainder = total_problems % len(topics)
    
    all_problems = []
    
    # Generate problems for each topic
    for i, topic in enumerate(topics):
        # Distribute remainder problems among topics
        count = problems_per_topic + (1 if i < remainder else 0)
        if count == 0:
            continue
            
        generator_func, _ = topic_generators[topic]
        try:
            problems = generator_func(count)
            all_problems.extend(problems)
            print(f"Generated {len(problems)} {topic} problems")
        except Exception as e:
            print(f"Error generating {topic} problems: {e}")
    
    # Fill any shortfall with problems from other topics
    if len(all_problems) < total_problems:
        shortfall = total_problems - len(all_problems)
        print(f"Warning: Only generated {len(all_problems)}/{total_problems} problems. Attempting to fill shortfall...")
        
        # Try to get more problems from available topics
        for topic in topics:
            if shortfall <= 0:
                break
                
            try:
                generator_func, _ = topic_generators[topic]
                extra = generator_func(shortfall)
                all_problems.extend(extra)
                shortfall -= len(extra)
                print(f"Added {len(extra)} more {topic} problems")
            except Exception as e:
                print(f"Error generating extra {topic} problems: {e}")
    
    # Shuffle the problems
    random.shuffle(all_problems)
    
    return all_problems

def save_worksheet(problems):
    """Save the worksheet to a JSON file in a dated folder."""
    # Create dated folder
    date_str = datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join('worksheets', date_str)
    os.makedirs(folder_path, exist_ok=True)
    
    # Count problems by type
    problem_counts = {}
    for p in problems:
        problem_type = p['type']
        problem_counts[problem_type] = problem_counts.get(problem_type, 0) + 1
    
    # Create topic description
    topic_parts = [f"{count} {typ.capitalize()}" for typ, count in problem_counts.items()]
    topic_str = " & ".join(topic_parts) + " Problems"
    
    # Prepare worksheet data
    worksheet = {
        'topic': f'Word Problems - {topic_str}',
        'date': date_str,
        'problem_counts': problem_counts,
        'problems': problems
    }
    
    # Save to JSON
    json_path = os.path.join(folder_path, 'worksheet.json')
    with open(json_path, 'w') as f:
        json.dump(worksheet, f, indent=2)
    
    return worksheet, folder_path

def main():
    print("Generating custom worksheet...")
    
    # Define problem distribution
    problem_distribution = {
        'integer': 5,         # 5 hard integer problems
        'fraction': 5,        # 5 hard fraction problems
        'simple_equations': 10  # 10 intermediate simple equations problems
    }
    
    # Track used problem patterns and types across all categories
    used_problem_patterns = set()
    all_problems = []
    
    # Generate problems for each topic
    for topic, count in problem_distribution.items():
        try:
            problems = []
            attempts = 0
            max_attempts_per_topic = count * 2  # Allow some retries for unique problems
            
            while len(problems) < count and attempts < max_attempts_per_topic:
                attempts += 1
                batch_problems = []
                
                # Generate a batch of problems
                if topic == 'integer':
                    batch_problems = generate_integer_problems(count=1)
                elif topic == 'fraction':
                    batch_problems = generate_fraction_problems(count=1)
                elif topic == 'simple_equations':
                    batch_problems = generate_simple_equations_problems(count=1)
                
                # Process each generated problem
                for problem in batch_problems:
                    if not problem or 'problem' not in problem:
                        continue
                        
                    # Get problem pattern for duplicate detection
                    problem_pattern = get_problem_pattern(
                        problem['problem'],
                        problem.get('subtype', '')
                    )
                    
                    # Skip if we've already used this pattern
                    if problem_pattern in used_problem_patterns:
                        print(f"Skipping duplicate pattern: {problem_pattern}")
                        continue
                        
                    # Add pattern to used patterns
                    used_problem_patterns.add(problem_pattern)
                    problem['pattern'] = problem_pattern  # Store pattern for reference
                    problems.append(problem)
                    
                    print(f"✓ Added {topic} problem - Pattern: {problem_pattern}")
                    
                    # Stop if we have enough problems
                    if len(problems) >= count:
                        break
            
            print(f"Generated {len(problems)} unique {topic} problems")
            all_problems.extend(problems)
            
        except Exception as e:
            print(f"Error generating {topic} problems: {e}")
            import traceback
            traceback.print_exc()
    
    # Shuffle the problems
    random.shuffle(all_problems)
    problems = all_problems
    
    if not problems:
        print("Error: No problems were generated.")
        return
    
    # Save to dated folder
    worksheet, folder_path = save_worksheet(problems)
    
    # Generate PDFs
    print("\nCreating PDFs...")
    
    # Questions only
    questions_pdf = os.path.join(folder_path, 'worksheet_questions.pdf')
    create_pdf(worksheet, include_answers=False, output_path=questions_pdf)
    
    # Questions with answers
    answers_pdf = os.path.join(folder_path, 'worksheet_answers.pdf')
    create_pdf(worksheet, include_answers=True, output_path=answers_pdf)
    
    # Print summary
    print("\n" + "="*50)
    print("WORKSHEET GENERATION COMPLETE")
    print("-"*50)
    print(f"Total problems: {len(problems)}")
    for typ, count in worksheet['problem_counts'].items():
        print(f"- {typ.capitalize()}: {count}")
    print("\nGenerated files:")
    print(f"- Questions: {questions_pdf}")
    print(f"- Answers: {answers_pdf}")
    print("="*50)

if __name__ == "__main__":
    main()
