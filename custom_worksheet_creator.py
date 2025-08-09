#!/usr/bin/env python3
"""
Custom Worksheet Creator

This script provides an interactive command-line interface to create custom math worksheets
with specific topics and number of questions for each topic.
"""

import os
import sys
import json
import random
from typing import Dict, List, Optional
from datetime import datetime

# Import the worksheet generator functions
from create_custom_worksheet import (
    generate_integer_problems,
    generate_fraction_problems,
    generate_simple_equations_problems,
    save_worksheet,
    create_pdf
)

# Import the problem importer
from problem_importer import ProblemImporter

# Available difficulty levels
DIFFICULTY_LEVELS = {
    'easy': {
        'name': 'Easy',
        'description': 'Basic problems suitable for beginners',
        'default': False
    },
    'intermediate': {
        'name': 'Intermediate',
        'description': 'Standard problems with moderate complexity',
        'default': True
    },
    'hard': {
        'name': 'Hard',
        'description': 'Challenging problems for advanced students',
        'default': False
    }
}

# Available topics and their generator functions
TOPIC_GENERATORS = {
    'integer': {
        'name': 'Integer Problems',
        'generator': generate_integer_problems,
        'default_count': 5,
        'description': 'Problems involving integer operations and word problems',
        'default_difficulty': 'intermediate',
        'supports_difficulty': True
    },
    'fraction': {
        'name': 'Fraction Problems',
        'generator': generate_fraction_problems,
        'default_count': 5,
        'description': 'Problems involving fractions and mixed numbers',
        'default_difficulty': 'intermediate',
        'supports_difficulty': True
    },
    'simple_equations': {
        'name': 'Simple Equations',
        'generator': generate_simple_equations_problems,
        'default_count': 10,
        'description': 'Basic algebraic equations and word problems',
        'default_difficulty': 'intermediate',
        'supports_difficulty': True
    },
    # Add new topics here as they become available
}

def display_difficulty_menu():
    """Display the available difficulty levels and get user selection."""
    print("\n=== Difficulty Levels ===")
    difficulties = list(DIFFICULTY_LEVELS.items())
    
    # Display menu
    for i, (level_id, level_info) in enumerate(difficulties, 1):
        default_marker = " (default)" if level_info.get('default', False) else ""
        print(f"{i}. {level_id.title()}{default_marker}")
        print(f"   {level_info['description']}")
    
    # Get user input with validation
    while True:
        try:
            choice = input("\nEnter the number of your choice (1-3, default 2): ").strip()
            if not choice:  # User pressed Enter, use default
                default_choice = next((i+1 for i, (_, info) in enumerate(difficulties) 
                                    if info.get('default', False)), 1)
                return default_choice
                
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(difficulties):
                return choice_idx + 1  # Return 1-based index
                
            print(f"Please enter a number between 1 and {len(difficulties)}")
        except ValueError:
            print("Please enter a valid number.")

def display_topic_menu():
    """Display the available topics with their descriptions."""
    print("\n=== Available Topics ===")
    for i, (topic_id, topic_info) in enumerate(TOPIC_GENERATORS.items(), 1):
        print(f"{i}. {topic_info['name']} (default: {topic_info['default_count']} questions)")
        print(f"   {topic_info['description']}")
        if 'default_difficulty' in topic_info:
            print(f"   Default difficulty: {topic_info['default_difficulty'].title()}")
        print()
    print("Enter the number of your choice.")

def get_choice_input(prompt: str, options: list, default: str = None) -> str:
    """Get a valid choice from the given options."""
    while True:
        choice = input(prompt).strip().lower()
        if not choice and default is not None:
            return default
        if choice in options:
            return choice
        print(f"Please enter one of: {', '.join(options)}")

def get_integer_input(prompt: str, min_val: int = 1, max_val: int = 50, default: int = None) -> int:
    """Get a valid integer input from the user."""
    while True:
        try:
            value = input(prompt).strip()
            if not value:  # Use default if no input
                if default is not None:
                    return default
                return -1
            value = int(value)
            if min_val <= value <= max_val:
                return value
            print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Please enter a valid number.")

def get_yes_no(prompt: str) -> bool:
    """Get a yes/no response from the user."""
    while True:
        response = input(f"{prompt} (y/n): ").strip().lower()
        if response in ('y', 'yes'):
            return True
        if response in ('n', 'no'):
            return False
        print("Please enter 'y' or 'n'.")

def generate_llm_problems(problem_type: str, count: int, difficulty: str = 'medium') -> list:
    """Generate problems using the LLM importer.
    
    Args:
        problem_type: Type of problem to generate
        count: Number of problems to generate
        difficulty: Difficulty level
        
    Returns:
        List of problem dictionaries
    """
    try:
        importer = ProblemImporter()
        problems = []
        
        # Map problem types to categories
        category_map = {
            'integer': 'Number System',
            'fraction': 'Number System',
            'decimal': 'Number System',
            'simple_equation': 'Algebra'
        }
        
        # Base problems for different types - expanded with clear, complete questions
        base_problems = {
            'integer': [
                "A train travels 300 km in 5 hours. What is its average speed in kilometers per hour?",
                "The sum of two consecutive numbers is 25. What are the two numbers? Show your work.",
                "A shopkeeper sold 45 books on Monday and 37 on Tuesday. How many more books were sold on Monday than on Tuesday?",
                "You have $100. You spend $37 on groceries and $28 on gas. How much money do you have left after these purchases?",
                "A football team gained 7 yards, then lost 12 yards, and finally gained 8 yards. What is their net yardage after these three plays?",
                "The temperature was -5°C at night. During the day, it rose by 12°C. What was the daytime temperature in degrees Celsius?",
                "A submarine is at 250 meters below sea level. If it rises 180 meters, what is its new depth below sea level?",
                "A pizza is cut into 8 equal slices. If 5 people share the pizza equally, how many slices does each person get, and how many slices remain?"
            ],
            'fraction': [
                "If 3/4 of a number is 15, what is the original number? Show your calculations.",
                "A recipe calls for 2/3 cup of sugar. If you want to make half the recipe, how much sugar should you use? Express your answer as a fraction.",
                "John has 5/6 of a pizza left. He eats 1/3 of the remaining pizza. What fraction of the whole pizza did he eat?",
                "In a class of 24 students, 5/8 are girls. How many girls are in the class? How many boys are there?",
                "A water tank is 3/4 full. After using 1/3 of the water in the tank, what fraction of the tank's capacity is now filled with water?",
                "If 2/5 of a number is 14, what is 3/4 of that number? Show your step-by-step solution.",
                "A recipe requires 3/4 cup of flour. If you want to make 2 1/2 times the recipe, how many cups of flour will you need?",
                "A rope is 12 meters long. How many pieces, each measuring 3/4 meter, can be cut from the rope? Will there be any rope left over?"
            ],
            'decimal': [
                "A rectangle has a length of 12.5 cm and a width of 8 cm. Calculate its area in square centimeters.",
                "A shirt is on sale for $45 after a 20% discount. What was the original price of the shirt before the discount?",
                "A car travels 245.6 km on 18.5 liters of petrol. Calculate the car's fuel efficiency in kilometers per liter (round to one decimal place).",
                "If 2.5 kg of apples cost $7.50, what is the cost per kilogram of apples?",
                "A student's scores on three tests are 85.5, 92.0, and 78.5. What is the student's average test score? Round your answer to one decimal place.",
                "A water tank contains 250.75 liters of water. If 37.5 liters are used, how many liters of water remain in the tank?",
                "A runner completes a 400-meter race in 45.8 seconds. Calculate the runner's average speed in meters per second (round to two decimal places).",
                "A recipe calls for 0.25 kg of flour, 0.15 kg of sugar, and 0.05 kg of cocoa powder. What is the total weight of these dry ingredients in kilograms?"
            ],
            'simple_equation': [
                "Solve for x: 2x + 5 = 15. Show each step of your solution.",
                "The sum of three consecutive even numbers is 54. Find all three numbers.",
                "A number increased by 7 equals 15. Set up and solve an equation to find the number.",
                "If 3 times a number minus 5 equals 16, what is the number? Show your work.",
                "The sum of two numbers is 45. If one number is twice the other, find both numbers.",
                "A rectangle's length is 5 meters more than its width. If the perimeter is 38 meters, find the length and width of the rectangle.",
                "The sum of three consecutive odd numbers is 57. Find all three numbers.",
                "A number divided by 4 plus 7 equals 15. Find the number by setting up and solving an equation."
            ]
        }
        
        base_problems_list = base_problems.get(problem_type, [
            f"If x = 5, what is 2x + 3?"  # Fallback problem
        ])
        
        # Track seen problems to avoid duplicates
        seen_problems = set()
        all_variations = []
        
        # First, try to generate variations from base problems
        max_attempts_per_problem = 2  # Maximum number of attempts per base problem
        max_total_attempts = count * 3  # Overall maximum attempts to prevent infinite loops
        total_attempts = 0
        
        # Shuffle the base problems to get more variety
        random.shuffle(base_problems_list)
        
        # Try to generate variations until we have enough or run out of attempts
        while len(all_variations) < count and total_attempts < max_total_attempts:
            # Cycle through base problems
            for base_problem in base_problems_list:
                if len(all_variations) >= count:
                    break
                    
                attempts = 0
                while attempts < max_attempts_per_problem and len(all_variations) < count:
                    try:
                        # Generate variations for this base problem
                        variations = importer.generate_variations(
                            problem_text=base_problem,
                            problem_type=problem_type.capitalize(),
                            num_variations=1  # Generate one at a time for better control
                        )
                        
                        if variations and isinstance(variations, list):
                            for variation in variations:
                                if 'text' in variation and variation['text'].strip():
                                    # Clean up the question
                                    question = variation['text'].strip()
                                    if not question.endswith('?'):
                                        question = f"{question}?"
                                    
                                    # Check for uniqueness
                                    if question not in seen_problems:
                                        seen_problems.add(question)
                                        
                                        # Add to all variations
                                        all_variations.append({
                                            'question': question,
                                            'answer': variation.get('explanation', 'No solution provided'),
                                            'type': problem_type.capitalize(),
                                            'difficulty': difficulty,
                                            'category': category_map.get(problem_type, 'General')
                                        })
                                        break  # Move to next base problem after one successful variation
                        
                    except Exception as e:
                        print(f"Error generating variation: {str(e)}")
                    
                    attempts += 1
                    total_attempts += 1
        
        # If we still don't have enough unique variations, use some base problems directly
        if len(all_variations) < count:
            for problem in base_problems_list:
                if len(all_variations) >= count:
                    break
                    
                if problem not in seen_problems:
                    seen_problems.add(problem)
                    all_variations.append({
                        'question': problem,
                        'answer': 'Solution not available',
                        'type': problem_type.capitalize(),
                        'difficulty': difficulty,
                        'category': category_map.get(problem_type, 'General')
                    })
        
        # Ensure we have exactly the requested number of problems
        return all_variations[:count]
        
    except Exception as e:
        print(f"Error in generate_llm_problems: {str(e)}")
        import traceback
        traceback.print_exc()
        # Return empty list to indicate failure
        return []
        
    except Exception as e:
        print(f"Critical error in generate_llm_problems: {str(e)}")
        # Return empty list to avoid crashing the calling function
        return []

def import_problem():
    """Import a problem from a textbook."""
    try:
        from problem_importer import get_user_input, ProblemImporter
        
        # Get user input for the problem
        problem_data = get_user_input()
        
        if problem_data.get('problem_text') and problem_data.get('problem_type') and problem_data.get('difficulty'):
            importer = ProblemImporter()
            try:
                # Use the new import_problem method
                result = importer.import_problem(
                    problem_text=problem_data['problem_text'],
                    problem_type=problem_data['problem_type'],
                    category=problem_data.get('category', 'Real-Life Scenarios'),
                    difficulty=problem_data['difficulty'],
                    grade=problem_data.get('grade', 'Grade 7')
                )
                
                print("\n✅ Problem imported successfully!")
                print(f"Type: {result['type']}")
                print(f"Difficulty: {result['difficulty']}")
                print(f"Saved to: data/{result['id']}.json")
                
                # Generate variations
                print("\nGenerating variations...")
                variations = importer.generate_variations(
                    problem_text=problem_data['problem_text'],
                    problem_type=problem_data['problem_type'],
                    num_variations=3
                )
                
                if variations:
                    # Update the problem with variations
                    result['variations'] = variations
                    result['metadata']['has_variations'] = True
                    result['metadata']['variation_count'] = len(variations)
                    
                    # Save the updated problem with variations
                    importer._save_problem(result)
                    print(f"✅ Generated {len(variations)} variations for the problem.")
                
            except Exception as e:
                print(f"\n❌ Error importing problem: {str(e)}")
                import traceback
                traceback.print_exc()
    except ImportError as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please ensure all required modules are available.")
    
    input("\nPress Enter to continue...")

def create_custom_worksheet():
    """Interactive function to create a custom worksheet."""
    print("\n=== Math Worksheet Generator (AI-Powered) ===")
    print("1. Generate New Worksheet with AI")
    print("2. Import Problem from Textbook")
    print("3. Exit")
    
    choice = input("\nSelect an option (1-3): ").strip()
    
    if choice == '1':
        # AI-generated worksheet
        create_ai_worksheet()
    elif choice == '2':
        import_problem()
    elif choice == '3':
        print("\nExiting. Goodbye!")
        return
    else:
        print("\nInvalid option. Please try again.")
        create_custom_worksheet()

def get_topic_settings(topic_id):
    """Get settings (number of problems and difficulty) for a specific topic."""
    print(f"\n=== {TOPIC_GENERATORS[topic_id]['name']} Settings ===")
    
    # Get number of problems
    while True:
        try:
            num_str = input(f"Number of {TOPIC_GENERATORS[topic_id]['name'].lower()} problems (1-10, default 5): ").strip()
            if not num_str:  # If user just presses Enter
                num_problems = 5
                break
            num_problems = int(num_str)
            if 1 <= num_problems <= 10:
                break
            print("Please enter a number between 1 and 10")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get difficulty level
    print("\nSelect difficulty level:")
    difficulty_choice = display_difficulty_menu()
    difficulties = list(DIFFICULTY_LEVELS.keys())
    difficulty = difficulties[difficulty_choice - 1] if 1 <= difficulty_choice <= len(difficulties) else 'medium'
    
    return {
        'id': topic_id,
        'name': TOPIC_GENERATORS[topic_id]['name'],
        'num_problems': num_problems,
        'difficulty': difficulty
    }

def create_ai_worksheet():
    """Create a worksheet using AI-generated problems with multiple topics."""
    print("\n=== AI-Powered Worksheet Generation ===")
    print("This will generate a worksheet using AI based on your preferences.\n")
    
    # Display available topics with numbers
    print("=== Available Topics ===")
    topics = list(TOPIC_GENERATORS.keys())
    selected_topics = []
    
    # Allow selecting multiple topics with individual settings
    while True:
        print("\nCurrent selection:")
        if not selected_topics:
            print("  None")
        else:
            for i, topic in enumerate(selected_topics, 1):
                print(f"  {i}. {topic['name']} - {topic['num_problems']} problems ({topic['difficulty']})")
        
        print("\nAvailable topics to add:")
        for i, topic in enumerate(topics, 1):
            print(f"{i}. {TOPIC_GENERATORS[topic]['name']} - {TOPIC_GENERATORS[topic]['description']}")
        print("0. Done adding topics")
        
        try:
            choice = input("\nSelect a topic to add (1-{}) or 0 when done: ".format(len(topics)))
            if choice == '0':
                if not selected_topics:
                    print("Please select at least one topic.")
                    continue
                break
                
            topic_idx = int(choice) - 1
            if 0 <= topic_idx < len(topics):
                topic_id = topics[topic_idx]
                # Get settings for this topic
                topic_settings = get_topic_settings(topic_id)
                selected_topics.append(topic_settings)
                topics.pop(topic_idx)  # Remove selected topic from available options
            else:
                print("Please enter a number between 1 and {}".format(len(topics)))
        except ValueError:
            print("Please enter a valid number.")
        
    # Generate problems for each selected topic with their individual settings
    all_problems = []
    worksheet_topics = []
    
    for topic_settings in selected_topics:
        print(f"\nGenerating {topic_settings['num_problems']} {topic_settings['difficulty']} {topic_settings['name'].lower()}...")
        
        # Generate problems for this topic
        problems = generate_llm_problems(
            problem_type=topic_settings['id'],
            count=topic_settings['num_problems'],
            difficulty=topic_settings['difficulty']
        )
        
        if problems:
            worksheet_topics.append({
                'id': topic_settings['id'],
                'name': topic_settings['name'],
                'difficulty': topic_settings['difficulty'],
                'problems': problems
            })
            all_problems.extend(problems)
    
    if not all_problems:
        print("Failed to generate any problems. Please try again.")
        return
    
    # Create worksheet data
    worksheet = {
        'metadata': {
            'title': f"AI-Generated Mixed Topics Worksheet",
            'created_at': datetime.now().isoformat(),
            'source': 'ai_generated',
            'difficulty': worksheet_topics[0]['difficulty'] if worksheet_topics else 'mixed',
            'topics': [t['id'] for t in worksheet_topics]
        },
        'topics': worksheet_topics,
        'problems': all_problems
    }
    
    # Save the worksheet
    topic_ids = '_'.join(t['id'] for t in worksheet_topics)
    save_worksheet(worksheet, f"multi_{topic_ids}")
    
    print("\n✅ Worksheet generated successfully!")
    print(f"Total problems: {len(all_problems)}")
    for topic in worksheet_topics:
        print(f"- {len(topic['problems'])} {topic['name']} problems")
    
    # Ask if user wants to create another worksheet
    if not get_yes_no("\nWould you like to create another worksheet"):
        print("\nThank you for using the Math Worksheet Generator!")
        sys.exit(0)

        # Get difficulty selection
        while True:
            try:
                choice = input("\nSelect difficulty (1-{}, default 2): ".format(len(difficulties)))
                if not choice:  # Default to intermediate
                    difficulty = 'intermediate'
                    break
                diff_idx = int(choice) - 1
                if 0 <= diff_idx < len(difficulties):
                    difficulty = difficulties[diff_idx]
                    break
                print("Please enter a number between 1 and {}".format(len(difficulties)))
            except ValueError:
                print("Please enter a valid number.")

        print("\nGenerating your AI-powered worksheet...")

        # Generate problems using LLM
        problems = generate_llm_problems(
            problem_type=topic_id,
            count=num_problems,
            difficulty=difficulty
        )

        if not problems:
            print("Failed to generate problems. Please try again.")
            return

        # Create worksheet
        worksheet = {
            'metadata': {
                'title': f"AI-Generated {TOPIC_GENERATORS[topic_id]['name']}",
                'created_at': datetime.now().isoformat(),
                'source': 'ai_generated',
                'difficulty': difficulty,
                'topic': topic_id
            },
            'problems': problems
        }

        # Save worksheet with proper directory structure
        date_str = datetime.now().strftime("%Y-%m-%d")
        folder_path = os.path.join('worksheets', date_str)
        os.makedirs(folder_path, exist_ok=True)

        # Save the worksheet
        save_worksheet(worksheet, topic_id)

def generate_solution(problem: dict) -> str:
    """Generate a solution for a given problem."""
    try:
        # If problem already has an answer, use it
        if problem.get('answer'):
            return problem['answer']
            
        # Generate solution based on problem type
        if problem.get('type') == 'integer':
            return "[Sample solution for integer problem]"
        elif problem.get('type') == 'fraction':
            return "[Sample solution for fraction problem]"
        elif problem.get('type') == 'decimal':
            return "[Sample solution for decimal problem]"
        else:  # simple_equation or other
            return "[Sample solution]"
    except Exception as e:
        print(f"Warning: Could not generate solution: {e}")
        return "[Solution not available]"

def save_worksheet(worksheet_data: dict, topic_id: str) -> tuple:
    """Save the worksheet and its solutions to files.
    
    Args:
        worksheet_data: Dictionary containing worksheet data
        topic_id: Identifier for the worksheet topic
        
    Returns:
        tuple: (saved_worksheet_data, output_folder_path)
    """
    try:
        # Create dated directory if it doesn't exist
        date_str = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_path = os.path.join('worksheets', date_str)
        os.makedirs(folder_path, exist_ok=True)
        
        # Ensure problems is a list
        problems = worksheet_data.get('problems', [])
        if not isinstance(problems, list):
            problems = [problems]
        
        # Generate solutions for each problem
        for problem in problems:
            if 'solution' not in problem:
                problem['solution'] = generate_solution(problem)
        
        # Update the worksheet data with solutions
        worksheet_data['problems'] = problems
        
        # Save the worksheet as JSON
        worksheet_file = f"worksheet_{topic_id}_{timestamp}.json"
        worksheet_path = os.path.join(folder_path, worksheet_file)
        
        with open(worksheet_path, 'w') as f:
            json.dump(worksheet_data, f, indent=2)
        
        # Generate a solutions file
        solutions = {
            'worksheet_id': worksheet_file,
            'topic': worksheet_data.get('metadata', {}).get('title', 'Custom Worksheet'),
            'date': date_str,
            'difficulty': worksheet_data.get('metadata', {}).get('difficulty', 'medium'),
            'solutions': [
                {
                    'problem': p.get('question', 'No question provided'),
                    'solution': p.get('solution', 'No solution available'),
                    'explanation': p.get('explanation', '')
                } for p in problems
            ]
        }
        
        solutions_file = f"solutions_{topic_id}_{timestamp}.json"
        solutions_path = os.path.join(folder_path, solutions_file)
        
        with open(solutions_path, 'w') as f:
            json.dump(solutions, f, indent=2)
        
        print(f"\n✅ Worksheet saved to: {worksheet_path}")
        print(f"✅ Solutions saved to: {solutions_path}")
        
        # Generate PDF versions if needed
        try:
            from generate_pdf import create_pdf
            
            # Prepare worksheet data for PDF generation
            pdf_worksheet_data = {
                'topic': worksheet_data.get('metadata', {}).get('title', 'Math Worksheet'),
                'difficulty': worksheet_data.get('metadata', {}).get('difficulty', 'medium'),
                'date': datetime.now().strftime("%Y-%m-%d"),
                'problems': [
                    {
                        'problem': p.get('question', p.get('problem', 'No problem text')),
                        'answer': p.get('solution', p.get('answer', 'No solution available')),
                        'explanation': p.get('explanation', '')
                    }
                    for p in worksheet_data.get('problems', [])
                ]
            }
            
            # Create worksheet PDF
            pdf_worksheet = os.path.join(folder_path, f"worksheet_{topic_id}_{timestamp}.pdf")
            create_pdf(pdf_worksheet_data, include_answers=False, output_path=pdf_worksheet)
            
            # Create solutions PDF
            pdf_solutions = os.path.join(folder_path, f"solutions_{topic_id}_{timestamp}.pdf")
            create_pdf(pdf_worksheet_data, include_answers=True, output_path=pdf_solutions)
            
            print(f"✅ Worksheet PDF: {pdf_worksheet}")
            print(f"✅ Solutions PDF: {pdf_solutions}")
            
        except ImportError as e:
            print(f"PDF generation module not available: {e}")
            print("Only JSON files were created. Please ensure ReportLab is installed.")
        except Exception as e:
            print(f"Warning: Could not generate PDFs: {e}")
            print("Only JSON files were created. Please check the error above.")
        
        return worksheet_data, folder_path
        
    except Exception as e:
        print(f"\n❌ Error saving worksheet: {e}")
        raise  # Re-raise to allow calling function to handle the error

def create_manual_worksheet():
    """This function is deprecated. Manual worksheet creation has been replaced by AI-powered generation."""
    print("\n⚠️  Manual worksheet creation is no longer supported.")
    print("Please use the AI-powered worksheet generator instead (Option 1).")
    print("This provides better quality problems and supports automatic solution generation.")
    
    # Display available topics
    display_topic_menu()
    
    # Get topic selection
    selected_topics = {}
    for topic_id, topic_info in TOPIC_GENERATORS.items():
        count = get_integer_input(
            f"Number of {topic_info['name']} questions (0 to skip, Enter for default {topic_info['default_count']}): ",
            min_val=0,
            max_val=50,
            default=topic_info['default_count']
        )
        if count <= 0:
            continue
            
        # Get difficulty level if supported
        difficulty = None
        if topic_info['supports_difficulty']:
            display_difficulty_menu()
            difficulty_options = list(DIFFICULTY_LEVELS.keys())
            default_difficulty = topic_info['default_difficulty']
            
            print(f"\nSelect difficulty for {topic_info['name']}:")
            for i, level_id in enumerate(difficulty_options, 1):
                is_default = " (default)" if level_id == default_difficulty else ""
                print(f"{i}. {level_id.title()}{is_default}")
                
            difficulty_choice = input(f"Choose difficulty [1-{len(difficulty_options)}] (Enter for {default_difficulty}): ").strip()
            
            if difficulty_choice.isdigit() and 1 <= int(difficulty_choice) <= len(difficulty_options):
                difficulty = difficulty_options[int(difficulty_choice) - 1]
            else:
                difficulty = default_difficulty
                print(f"Using default difficulty: {difficulty}")
        
        selected_topics[topic_id] = {
            'count': count,
            'difficulty': difficulty
        }
    
    if not selected_topics:
        print("\nError: You must select at least one topic.")
        return
    
    # Generate worksheet
    print("\nGenerating your custom worksheet...")
    
    # Track used problem patterns and types across all categories
    used_problem_patterns = set()
    all_problems = []
    
    # Generate problems for each selected topic
    for topic_id, topic_config in selected_topics.items():
        count = topic_config['count']
        difficulty = topic_config.get('difficulty')
        
        try:
            problems = []
            attempts = 0
            max_attempts_per_topic = count * 2  # Allow some retries for unique problems
            
            while len(problems) < count and attempts < max_attempts_per_topic:
                attempts += 1
                batch_problems = []
                
                # Generate a batch of problems
                # Note: The difficulty parameter is not supported in the current generator functions
                # We'll add the difficulty to the problem after generation
                batch_problems = TOPIC_GENERATORS[topic_id]['generator'](count=1)
                
                # Process each generated problem
                for problem in batch_problems:
                    if not problem or 'problem' not in problem:
                        continue
                        
                    # Set difficulty if not already set
                    if difficulty and 'difficulty' not in problem:
                        problem['difficulty'] = difficulty
                        
                    # Skip if we've already used this pattern
                    pattern = problem.get('pattern', problem.get('subtype', 'unknown'))
                    if pattern in used_problem_patterns:
                        continue
                        
                    # Add pattern to used patterns
                    used_problem_patterns.add(pattern)
                    problem['pattern'] = pattern  # Ensure pattern is set
                    problems.append(problem)
                    
                    # Show difficulty in the progress message if available
                    diff_info = f" ({problem.get('difficulty', 'default')} difficulty)" if 'difficulty' in problem else ""
                    print(f"✓ Added {len(problems)}/{count} {TOPIC_GENERATORS[topic_id]['name']}{diff_info}")
                    
                    # Stop if we have enough problems
                    if len(problems) >= count:
                        break
            
            print(f"Generated {len(problems)} {TOPIC_GENERATORS[topic_id]['name']} problems")
            all_problems.extend(problems)
            
        except Exception as e:
            print(f"Error generating {TOPIC_GENERATORS[topic_id]['name'].lower()} problems: {e}")
            import traceback
            traceback.print_exc()
    
    if not all_problems:
        print("\nError: No problems were generated.")
        return
    
    # Shuffle the problems
    import random
    random.shuffle(all_problems)
    
    # Save to dated folder
    worksheet, folder_path = save_worksheet(all_problems)
    
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
    print(f"Total problems: {len(all_problems)}")
    for typ, count in worksheet['problem_counts'].items():
        print(f"- {typ.capitalize()}: {count}")
    print("\nGenerated files:")
    print(f"- Questions: {questions_pdf}")
    print(f"- Answers: {answers_pdf}")
    print("="*50)

if __name__ == "__main__":
    try:
        while True:
            create_custom_worksheet()
            if not get_yes_no("\nCreate another worksheet"):
                print("\nThank you for using the Math Worksheet Generator!")
                sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()
