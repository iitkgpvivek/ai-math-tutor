#!/usr/bin/env python3
"""
Create a custom worksheet with problems from different categories.
"""
import os
import json
from datetime import datetime
from grade7_problems import Grade7ProblemGenerator
from generate_pdf import create_pdf

def generate_problems():
    """Generate 10 integer and 10 fraction/decimal problems."""
    generator = Grade7ProblemGenerator()
    problems = []
    
    # Generate 10 integer problems
    for _ in range(10):
        problem, answer = generator.generate_integer_problem('hard')
        problems.append({
            'problem': problem,
            'answer': answer,
            'type': 'integer',
            'difficulty': 'hard'
        })
    
    # Generate 10 fraction/decimal problems (alternating between the two)
    for i in range(10):
        if i % 2 == 0:
            problem, answer = generator.generate_fraction_decimal_problem('hard')
            prob_type = 'fraction'
        else:
            problem, answer = generator.generate_rational_number_problem('hard')
            prob_type = 'decimal'
            
        problems.append({
            'problem': problem,
            'answer': answer,
            'type': prob_type,
            'difficulty': 'hard'
        })
    
    return problems

def save_worksheet(problems):
    """Save the worksheet to a JSON file in a dated folder."""
    # Create dated folder
    date_str = datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join('worksheets', date_str)
    os.makedirs(folder_path, exist_ok=True)
    
    # Prepare worksheet data
    worksheet = {
        'topic': 'Mixed Problems - Integers, Fractions & Decimals',
        'difficulty': 'hard',
        'date': date_str,
        'problems': problems
    }
    
    # Save to JSON
    json_path = os.path.join(folder_path, 'worksheet.json')
    with open(json_path, 'w') as f:
        json.dump(worksheet, f, indent=2)
    
    return worksheet, folder_path

def main():
    print("Generating custom worksheet...")
    
    # Generate problems
    problems = generate_problems()
    
    # Save to dated folder
    worksheet, folder_path = save_worksheet(problems)
    
    # Generate PDFs
    print("Creating PDFs...")
    
    # Questions only
    questions_pdf = os.path.join(folder_path, 'worksheet_questions.pdf')
    create_pdf(worksheet, include_answers=False, output_path=questions_pdf)
    
    # Questions with answers
    answers_pdf = os.path.join(folder_path, 'worksheet_answers.pdf')
    create_pdf(worksheet, include_answers=True, output_path=answers_pdf)
    
    print(f"\nWorksheet generation complete!")
    print(f"- Questions: {questions_pdf}")
    print(f"- Answers: {answers_pdf}")

if __name__ == "__main__":
    main()
