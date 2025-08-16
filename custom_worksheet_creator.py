#!/usr/bin/env python3
"""
Custom Worksheet Creator

This script provides an interactive command-line interface to create custom math worksheets
with specific topics and number of questions for each topic.
"""

import json
import os
import random
import sys
import time
import asyncio
from datetime import datetime
from typing import Dict, List, Optional

# Import the worksheet utility functions
from create_custom_worksheet import save_worksheet, create_pdf

# Import the problem importer
from problem_importer import ProblemImporter
 
# Agents for validation
from agents.student_agent import StudentAgent
from agents.teacher_agent import TeacherAgent, ProblemVariation

# Default LLM config for agents
llm_config = {
    "llm_model": "mistral",
    "llm_temperature": 0.7,
}

async def _validate_one(teacher, problem_text, solution_text, problem_number=None):
    """Validate a single problem using the teacher agent."""
    try:
        if problem_number is not None:
            print(f"\n🔍 Validating problem {problem_number}...")
            print(f"   Problem: {problem_text}")
            print(f"   Solution: {solution_text}")
        
        # Create a ProblemVariation object as expected by _validate_problem
        problem_variation = ProblemVariation(
            original_question=problem_text,
            variation=problem_text,
            solution=solution_text
        )
        
        # Call the correct validation method
        validation = await teacher._validate_problem(problem_variation)
        
        if problem_number is not None:
            status = "✅ ACCEPTED" if validation.get('is_valid') else "❌ REJECTED"
            print(f"   {status}: {validation.get('feedback', 'No feedback provided')}")
            if not validation.get('is_valid') and 'validation_result' in validation:
                print(f"   Validation details: {validation['validation_result']}")
                
        return validation
    except Exception as e:
        error_msg = f'Validation error: {e}'
        if problem_number is not None:
            print(f"❌ ERROR validating problem {problem_number}: {error_msg}")
        return {'is_valid': False, 'feedback': error_msg}

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

# Available topics and their configurations
TOPIC_GENERATORS = {
    'integer': {
        'name': 'Integer Problems',
        'default_count': 5,
        'description': 'Problems involving integer operations and word problems',
        'default_difficulty': 'intermediate',
        'supports_difficulty': True
    },
    'fraction': {
        'name': 'Fraction Problems',
        'default_count': 5,
        'description': 'Problems involving fractions and mixed numbers',
        'default_difficulty': 'intermediate',
        'supports_difficulty': True
    },
    'simple_equations': {
        'name': 'Simple Equations',
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

import re

def generate_llm_problems(problem_type: str, count: int, difficulty: str = 'medium') -> list:
    """Generate fresh math problems aligned with CBSE curriculum for Indian students.
    
    Problems are designed to match the NCERT syllabus and style for Grade 7 students.
    Uses problem templates from data/problems as seeds for generating similar problems.
    
    Args:
        problem_type: Type of problem to generate (e.g., 'integer')
        count: Number of problems to generate
        difficulty: Difficulty level ('easy', 'medium', 'hard')
        
    Returns:
        List of problem dictionaries with 'problem' and 'solution' keys
    """
    try:
        from local_llm_integration import LocalLLMGenerator
        from problem_template_manager import ProblemTemplateManager
        import json
        
        # Initialize the LLM generator and template manager
        llm = LocalLLMGenerator()
        template_manager = ProblemTemplateManager()
        
        # Ensure the server is running
        if not llm.ensure_server():
            print("❌ Could not connect to LLM server. Please make sure Ollama is running.")
            return []
        
        problems = []
        used_problem_texts = set()  # To avoid duplicates
        
        # Map problem types to categories
        category_map = {
            'integer': 'Number System',
            'fraction': 'Number System',
            'decimal': 'Number System',
            'simple_equations': 'Algebra'
        }
        
        # Get the appropriate category for the problem type
        category = category_map.get(problem_type, 'General')
        
        for _ in range(count):
            try:
                # Try to get a template matching the requested type and difficulty
                template = template_manager.get_random_template(
                    problem_type=problem_type,
                    difficulty=difficulty,
                    avoid_used=True
                )
                
                if template:
                    # Use the template to generate a similar problem
                    # Special handling for simple equations to ensure they require solving an equation
                    if problem_type.lower() in ['simple_equations', 'equation', 'equations', 'sim']:
                        prompt = f"""You are an expert math teacher creating equation-solving problems for 7th grade Indian students following the CBSE curriculum.
                        
                        === ORIGINAL PROBLEM ===
                        {template['original_question']}
                        
                        === MATHEMATICAL STRUCTURE ===
                        Analyze and maintain the exact same mathematical structure in your variation.
                        For example, if the original is "1 subtracted from one-third of a number gives 1", 
                        the structure is: (x/3) - 1 = 1
                        
                        === TASK ===
                        Create a new variation that:
                        1. Has the EXACT SAME mathematical structure as the original
                        2. The variation looks similar to the original problem
                        3. May change the numbers and context (e.g., different objects, measurements)
                        4. Results in a whole number or simple fraction answer
                        5. Is culturally appropriate for Indian students
                        6. Uses Indian currency (₹) and metric units
                        
                        === REQUIREMENTS ===
                        - The problem MUST have the SAME mathematical structure as the original
                        - The variation should look similar to the original problem
                        - You MUST first analyze and show the mathematical structure of the original
                        - Only change the numbers and context, keeping the equation structure identical
                        - The solution should require the SAME number of steps as the original
                        - The answer should be a whole number or simple fraction
                        - The problem must end with a question mark (?)
                        
                        === EXAMPLE 1 ===
                        Original: "1 subtracted from one-third of a number gives 1, find the number."
                        Structure: (x/3) - 1 = 1
                        Good Variation: "2 subtracted from one-fourth of a number gives 3, find the number."
                        Structure: (x/4) - 2 = 3
                        
                        === EXAMPLE 2 ===
                        Original: "The sum of three consecutive numbers is 36. Find the numbers."
                        Structure: x + (x+1) + (x+2) = 36
                        Good Variation: "The sum of three consecutive even numbers is 48. Find the numbers."
                        Structure: x + (x+2) + (x+4) = 48
                        
                        === EXAMPLE 3 ===
                        Original: "If 5 is added to three times a number, the result is 20."
                        === REQUIRED JSON FORMAT ===
                        {{
                          "original_structure": "The mathematical structure of the original problem (e.g., (x/3) - 1 = 1)",
                          "variation_structure": "The mathematical structure of your variation (should match the original)",
                          "variation": "Your new problem text here?",
                          "solution_steps": [
                            "Step 1: Write down the equation",
                            "Step 2: Solve for x",
                            "Step 3: Verify the solution"
                          ],
                          "final_answer": "The final numerical answer (e.g., x = 12)",
                          "explanation": "Brief explanation of the solution approach"
                        }}
                        
                        Your response (ONLY the JSON object, no other text):
                        """
                    else:
                        # Original prompt for other problem types
                        prompt = f"""You are an expert math teacher creating variations of problems for 7th grade Indian students following the CBSE curriculum.
                        
                        === ORIGINAL PROBLEM ===
                        {template['original_question']}
                        
                        === TASK ===
                        Create a new variation of this problem that:
                        - Has the same core mathematical concept and structure
                        - The variation should look similar to the original problem
                        - Uses different numbers and context
                        - Is appropriate for {difficulty} difficulty
                        - Is clear, complete, and ends with a question mark
                        - Is culturally appropriate for Indian students
                        - Uses Indian currency (₹) and metric units
                        
                        === REQUIRED JSON FORMAT ===
                        You MUST respond with a valid JSON object containing these fields:
                        - "variation": The new problem text (ending with a question mark)
                        - "solution_steps": ["Step 1", "Step 2", ...] (detailed solution steps)
                        - "final_answer": "The final numerical/computational answer"
                        - "explanation": A brief explanation of the solution approach
                        
                        Example:
                        {{
                          "variation": "If a train travels 300 km in 5 hours, what is its speed in km/h?",
                          "solution_steps": [
                            "Step 1: Calculate the speed using the formula speed = distance/time",
                            "Step 2: Plug in the values and solve for speed"
                          ],
                          "final_answer": "60 km/h",
                          "explanation": "This problem involves calculating speed using the formula speed = distance/time."
                        }}
                        
                        RULES:
                        1. The response MUST be valid JSON
                        2. The variation MUST end with a question mark (?)
                        3. The variation MUST be a complete, self-contained question
                        4. The explanation should be brief and focus on the mathematical changes
                        
                        Your response (ONLY the JSON object, no other text):
                        """
                else:
                    # Fallback to generic prompt if no template found
                    prompt = f"""
                    You are an expert math teacher creating problems for 7th grade Indian students following the CBSE curriculum.
                    
                    === TASK ===
                    Generate EXACTLY ONE complete math problem with a clear question and solution.
                    
                    === REQUIREMENTS ===
                    - Problem type: {problem_type}
                    - Difficulty: {difficulty}
                    - Must be a complete, self-contained question
                    - Must end with a clear, specific question mark (?)
                    - Must include all necessary information to solve
                    - Must be culturally appropriate for Indian students
                    - Must use Indian currency (₹) and metric units
                    
                    === REQUIRED JSON FORMAT ===
                    You MUST respond with a valid JSON object containing exactly these two fields:
                    - "variation": The new problem text (ending with a question mark)
                    - "solution_steps": ["Step 1", "Step 2", ...] (detailed solution steps)
                    - "final_answer": "The final numerical/computational answer"
                    - "explanation": A brief explanation of the solution approach
                    
                    Example:
                    {{
                      "variation": "If a train travels 300 km in 5 hours, what is its speed in km/h?",
                      "solution_steps": [
                        "Step 1: Calculate the speed using the formula speed = distance/time",
                        "Step 2: Plug in the values and solve for speed"
                      ],
                      "final_answer": "60 km/h",
                      "explanation": "This problem involves calculating speed using the formula speed = distance/time."
                    }}
                    
                    RULES:
                    1. The response MUST be valid JSON
                    2. The variation MUST end with a question mark (?)
                    3. The variation MUST be a complete, self-contained question
                    4. The explanation should briefly describe the mathematical concept
                    
                    Your response (ONLY the JSON object, no other text):
                    """
                
                # Generate the problem using the LLM
                response = llm._generate_with_llm(prompt, temperature=0.7)
                
                try:
                    # Clean up the response
                    response = response.strip()
                    
                    # Debug: Print the raw response for troubleshooting
                    debug_file = os.path.join('debug', f'llm_response_{int(time.time())}.txt')
                    os.makedirs('debug', exist_ok=True)
                    with open(debug_file, 'w') as f:
                        f.write(response)
                    
                    try:
                        # Debug: Log the raw response for inspection
                        with open(debug_file + '.raw', 'wb') as f:
                            f.write(response.encode('utf-8', 'replace'))
                        
                        # Try to parse as JSON with strict encoding handling
                        import json
                        response_data = json.loads(response)
                        
                        if not isinstance(response_data, dict):
                            raise ValueError(f"Expected a JSON object, got {type(response_data).__name__}")
                            
                        if 'variation' not in response_data or 'solution_steps' not in response_data or 'final_answer' not in response_data or 'explanation' not in response_data:
                            # If we still can't parse, try to extract just a question
                            questions = re.findall(r'([^.!?]+\?)', response)
                            if questions:
                                problem_text = questions[0].strip()
                                solution_text = "Solution: " + response.replace(problem_text, '').strip()
                            else:
                                raise ValueError(f"Could not parse LLM response. Response: {response[:200]}...")
                        else:
                            problem_text = response_data['variation'].strip()
                            # Format the solution with steps and final answer
                            solution_steps = '\n'.join(f"• {step}" for step in response_data.get('solution_steps', []))
                            final_answer = response_data.get('final_answer', 'No final answer provided')
                            explanation = response_data.get('explanation', 'No explanation provided')
                            
                            solution_text = f"{solution_steps}\n\nFinal Answer: {final_answer}\n\nExplanation: {explanation}"
                        
                        # Create the problem dictionary
                        problem = {
                            'problem': problem_text,
                            'solution': solution_text,
                            'type': problem_type,
                            'difficulty': difficulty,
                            'category': category,
                            'source': 'ai_generated',
                            'template_used': template['id'] if template else None
                        }
                        
                        # Check for duplicates
                        if problem_text not in used_problem_texts:
                            problems.append(problem)
                            used_problem_texts.add(problem_text)
                            print(f"✅ Generated problem {len(problems)}/{count}")
                        else:
                            print("⚠️  Duplicate problem detected, generating another...")
                            continue
                    except json.JSONDecodeError as e:
                        # Fallback to simple parsing if JSON parsing fails
                        print("⚠️  Could not parse LLM response as JSON, using fallback parsing")
                        problem_text = response.split('\n')[0].strip()
                        if not problem_text.endswith('?'):
                            problem_text = problem_text.rstrip('.') + '?'
                            
                        problem = {
                            'problem': problem_text,
                            'solution': 'Solution steps not provided by AI.',
                            'type': problem_type,
                            'difficulty': difficulty,
                            'category': category,
                            'source': 'ai_generated_fallback',
                            'template_used': template['id'] if template else None
                        }
                        
                        if problem_text not in used_problem_texts:
                            problems.append(problem)
                            used_problem_texts.add(problem_text)
                
                except (json.JSONDecodeError, KeyError, IndexError) as e:
                    print(f"⚠️  Error parsing LLM response: {e}")
                    print("Response:", response)
                    continue
                    
            except Exception as e:
                print(f"⚠️  Error generating problem: {e}")
                continue
        
        # If we couldn't generate enough problems, try with a simpler prompt
        remaining = count - len(problems)
        if remaining > 0 and remaining < count:  # Only try if we made some progress
            print(f"⚠️  Could only generate {len(problems)}/{count} problems. Trying with simpler prompts...")
            try:
                # Try with simpler prompts for remaining problems
                simple_prompt = f"""
                Create a {difficulty} level math problem about {problem_type} for 7th grade students.
                Make it clear and end with a question mark.
                
                Problem: """
                
                for _ in range(remaining):
                    try:
                        response = llm._generate_with_llm(simple_prompt, temperature=0.8)
                        problem_text = response.strip()
                        
                        if not problem_text.endswith('?'):
                            problem_text = problem_text.rstrip('.') + '?'
                            
                        if problem_text not in used_problem_texts:
                            problem = {
                                'problem': problem_text,
                                'solution': 'Solution steps not provided by AI.',
                                'type': problem_type,
                                'difficulty': difficulty,
                                'category': category,
                                'source': 'ai_generated_fallback_simple'
                            }
                            problems.append(problem)
                            used_problem_texts.add(problem_text)
                            print(f"✅ Generated fallback problem {len(problems)}/{count}")
                            
                    except Exception as e:
                        print(f"⚠️  Error with fallback generation: {e}")
                        continue
                        
            except Exception as e:
                print(f"⚠️  Error in fallback generation: {e}")
        
        # Final check if we still don't have enough problems
        if len(problems) < count:
            print(f"⚠️  Warning: Only generated {len(problems)} out of requested {count} problems.")
        
        return problems
        
    except Exception as e:
        print(f"❌ Error in problem generation: {e}")
        import traceback
        traceback.print_exc()
        # Extract problem text
        problem_text = ''
        if 'PROBLEM' in problem_data:
            problem_text = problem_data.get('PROBLEM', '').strip()
        elif 'problem' in problem_data:
            problem_text = problem_data.get('problem', '').strip()
        
        # Extract question if separate
        question = problem_data.get('QUESTION', problem_data.get('question', '')).strip()
        if question and question not in problem_text:
            problem_text = f"{problem_text} {question}"
        
        # Extract solution
        solution = ''
        if 'SOLUTION' in problem_data:
            solution = problem_data.get('SOLUTION', '')
        elif 'solution' in problem_data:
            solution = problem_data.get('solution', '')
        
        # Normalize solution format
        if isinstance(solution, (list, tuple)):
            solution = '\n'.join(str(s).strip() for s in solution if str(s).strip())
        elif isinstance(solution, dict):
            solution = '\n'.join(f"{k}: {v}" for k, v in solution.items() if str(v).strip())
        else:
            solution = str(solution).strip()
            
        # If we couldn't extract a valid problem and solution, use fallback
        if not problem_text or not solution:
            problem_text = "Please provide a complete question."
            solution = "No solution provided."
        
        # Clean up the problem text
        if problem_text:
            # Remove any JSON-like formatting and extra whitespace
            problem_text = re.sub(r'^["\']|["\']$', '', problem_text.strip())
            problem_text = ' '.join(line.strip() for line in problem_text.split('\n') if line.strip())
            
            # Ensure the problem is a complete question
            if problem_text:
                # Remove any leading numbers or bullets
                problem_text = re.sub(r'^[\d\s\-\.\)\(]*', '', problem_text).strip()
                
                # Capitalize first letter
                problem_text = problem_text[0].upper() + problem_text[1:]
                
                # Ensure it ends with a question mark
                if not problem_text.endswith('?'):
                    problem_text = problem_text.rstrip('.') + '?'
        
        # Clean up the solution
        if solution:
            if isinstance(solution, str):
                # Remove any JSON-like formatting and extra whitespace
                solution = re.sub(r'^["\']|["\']$', '', solution.strip())
                solution = '\n'.join(line.strip() for line in solution.split('\n') if line.strip())
            
            # Ensure solution has a final answer if it's multi-line
            if '\n' in solution and not re.search(r'(?i)final(?:\s+answer)?\s*[:\-]?\s*', solution):
                solution = f"{solution}\n\nFinal answer: See steps above."
        
        if problem_text and solution:
            problems.append({
                'problem': problem_text,
                'solution': solution,
                'type': problem_type.capitalize(),
                'difficulty': difficulty,
                'category': category_map.get(problem_type, 'General')
            })
            print(f"✓ Generated problem {len(problems)}/{count}")
        else:
            print("❌ Empty problem or solution")
            print("Problem:", problem_text)
            print("Solution:", solution)
            print("Raw response:", response)
    
    except Exception as e:
        print(f"❌ Error in problem generation: {e}")
        print("Raw response:", response)
        import traceback
        traceback.print_exc()
        return problems
        

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
    while True:
        print("\n=== Math Worksheet Generator (AI-Powered) ===")
        print("1. Generate New Worksheet with AI")
        print("2. Import Problem from Textbook")
        print("3. Generate Problems using Teacher-Student Agents")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == '1':
            # AI-generated worksheet
            create_ai_worksheet()
        elif choice == '2':
            import_textbook_problem()
        elif choice == '3':
            asyncio.run(create_ai_worksheet_with_agents())
        elif choice == '4':
            print("\nThank you for using the Math Worksheet Generator!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

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
    
async def create_ai_worksheet_with_agents():
    """Create a worksheet using AI-generated problems validated by Teacher-Student agents."""
    print("\n=== Agent-Validated Worksheet Generation ===")
    print("This will generate problems and validate them using Teacher-Student agents.\n")
    
    # Instantiate agents once
    try:
        student = StudentAgent(grade_level=7, config=llm_config)
        teacher = TeacherAgent(student_agent=student, config=llm_config)
    except Exception as e:
        print(f"❌ Failed to initialize agents: {e}")
        return
    
    # Topic selection flow (reuse from create_ai_worksheet)
    print("=== Available Topics ===")
    topics = list(TOPIC_GENERATORS.keys())
    selected_topics = []
    
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
                topic_settings = get_topic_settings(topic_id)
                selected_topics.append(topic_settings)
                topics.pop(topic_idx)
            else:
                print("Please enter a number between 1 and {}".format(len(topics)))
        except ValueError:
            print("Please enter a valid number.")
    
    all_problems = []
    worksheet_topics = []
    rejected_log = []
    
    for topic_settings in selected_topics:
        desired = topic_settings['num_problems']
        print(f"\n📝 Generating {desired} {topic_settings['difficulty']} {topic_settings['name'].lower()}...")
        print(f"   Will make up to {desired * 3} attempts to get {desired} valid problems")
        
        attempts = 0
        max_attempts = desired * 3
        validated: list = []
        
        # Track progress
        def get_progress():
            return f"[{'✅' * len(validated)}{'⬜' * (desired - len(validated))}] {len(validated)}/{desired} problems"
        
        while len(validated) < desired and attempts < max_attempts:
            # Calculate batch size (smaller as we get closer to desired count)
            remaining = desired - len(validated)
            batch_size = min(3, remaining)
            attempts += 1
            
            print(f"\n🔄 Attempt {attempts}/{max_attempts} {get_progress()}")
            print(f"   Generating {batch_size} problem{'s' if batch_size > 1 else ''}...")
            
            try:
                # Generate a batch of problems
                problems = generate_llm_problems(
                    problem_type=topic_settings['id'],
                    count=batch_size,
                    difficulty=topic_settings['difficulty']
                )
                
                if not problems:
                    print("   ❌ No problems generated in this attempt")
                    continue
                    
                print(f"   Validating {len(problems)} generated problem{'s' if len(problems) > 1 else ''}...")
                
                # Process each problem in the batch
                for i, p in enumerate(problems, 1):
                    try:
                        problem_text = p.get('problem') or p.get('question', '')
                        solution_text = p.get('solution', '')
                        
                        res = await _validate_one(teacher, problem_text, solution_text, problem_number=len(validated) + 1)
                        
                        if res.get('is_valid'):
                            validated.append(p)
                            print(f"   🎉 Added to worksheet! {get_progress()}")
                            if len(validated) >= desired:
                                break
                        else:
                            reason = res.get('feedback', 'No specific reason provided')
                            print(f"   ❌ Rejected: {reason}")
                            if 'validation_result' in res:
                                print(f"      Details: {res['validation_result']}")
                                
                            rejected_log.append({
                                'problem': problem_text,
                                'reason': reason,
                                'validation_result': res.get('validation_result')
                            })
                            
                    except Exception as e:
                        error_msg = f'Processing error: {e}'
                        print(f"   ❌ {error_msg}")
                        rejected_log.append({
                            'problem': p.get('problem') or p.get('question', ''), 
                            'reason': error_msg
                        })
                        continue
                        
            except Exception as e:
                print(f"   ❌ Error generating problems: {e}")
                continue
        if len(validated) < desired:
            print(f"⚠️  Only {len(validated)} of {desired} problems passed validation for {topic_settings['name']} after {attempts} attempts.")
        if validated:
            worksheet_topics.append({
                'id': topic_settings['id'],
                'name': topic_settings['name'],
                'difficulty': topic_settings['difficulty'],
                'problems': validated[:desired]
            })
            all_problems.extend(validated[:desired])
    
    if not all_problems:
        print("Failed to produce any validated problems. Please try again.")
        return
    
    # Build PDF-friendly worksheet (map 'solution'->'answer')
    date_str = datetime.now().strftime("%Y-%m-%d")
    pdf_worksheet = {
        'topic': 'Mixed Topics' if len(worksheet_topics) > 1 else (worksheet_topics[0]['name'] if worksheet_topics else 'Math'),
        'difficulty': 'mixed' if len(worksheet_topics) > 1 else (worksheet_topics[0]['difficulty'] if worksheet_topics else 'intermediate'),
        'date': date_str,
        'problems': [
            {
                'problem': p.get('problem') or p.get('question', ''),
                'answer': p.get('answer', p.get('solution', ''))
            }
            for p in all_problems
        ]
    }
    
    # Save JSON using standard saver (returns JSON file path); derive folder for PDFs
    topic_ids = '_'.join(t['id'] for t in worksheet_topics)
    
    # Save just the problems list to JSON
    saved_json_path = save_worksheet(pdf_worksheet['problems'], f"agents_multi_{topic_ids}")
    folder_path = os.path.dirname(saved_json_path)
    
    # Generate PDFs in same folder
    questions_pdf = os.path.join(folder_path, 'worksheet_questions.pdf')
    answers_pdf = os.path.join(folder_path, 'worksheet_answers.pdf')
    create_pdf(pdf_worksheet, include_answers=False, output_path=questions_pdf)
    create_pdf(pdf_worksheet, include_answers=True, output_path=answers_pdf)

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
