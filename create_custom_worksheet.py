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
from generate_pdf import create_pdf

def is_placeholder(problem_text):
    """Check if a problem text is a placeholder."""
    placeholder_indicators = [
        'placeholder',
        'problem statement',
        'problem text',
        'example problem',
        'sample problem'
    ]
    problem_lower = problem_text.lower()
    return any(indicator in problem_lower for indicator in placeholder_indicators)

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
            # Set all problems to medium difficulty
            difficulty = 'medium'
            
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
            
            # Set all problems to medium difficulty
            difficulty = 'medium'
            
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
        # Add new topics here as they become available
        # 'algebra': (generate_algebra_problems, 1.0),
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
    
    # Define available topics
    available_topics = ['integer', 'fraction']  # Add more as they become available
    
    # For now, use all available topics
    # In the future, you could add command-line arguments to select specific topics
    selected_topics = available_topics
    
    print(f"Selected topics: {', '.join(selected_topics)}")
    
    # Generate problems
    problems = generate_problems(topics=selected_topics, total_problems=20)
    
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
