#!/usr/bin/env python3
"""
Save and manage custom worksheets.
This module provides functions to save worksheets and create PDFs.
"""
import os
import json
from datetime import datetime
from generate_pdf import create_pdf

def save_worksheet(problems, filename=None):
    """
    Save the worksheet to a JSON file in a dated folder.
    
    Args:
        problems: List of problem dictionaries to save
        filename: Optional filename (without extension)
    
    Returns:
        str: Path to the saved worksheet file
    """
    # Create a timestamp for the worksheet
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Create the worksheets directory if it doesn't exist
    os.makedirs('worksheets', exist_ok=True)
    
    # Create a date-based subdirectory (YYYY-MM-DD)
    date_dir = os.path.join('worksheets', date_str)
    os.makedirs(date_dir, exist_ok=True)
    
    # Create a subdirectory for this specific worksheet
    worksheet_dir = os.path.join(date_dir, f'worksheet_{timestamp}')
    os.makedirs(worksheet_dir, exist_ok=True)
    
    # Generate filename if not provided
    if not filename:
        filename = f'worksheet_{timestamp}'
    
    # Save the problems to a JSON file
    worksheet_file = os.path.join(worksheet_dir, f'{filename}.json')
    
    with open(worksheet_file, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'problems': problems
        }, f, indent=2)
    
    print(f"Worksheet saved to: {worksheet_file}")
    return worksheet_file

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
