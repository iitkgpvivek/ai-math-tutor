"""
Problem Importer for Math Worksheets

This module allows importing custom problems from textbooks and integrating them
with the existing problem generation system using local LLM for variation generation.
"""
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Union

class ProblemImporter:
    """Handles importing custom problems and generating variations using LLM."""
    
    def __init__(self, data_dir: str = "data", auto_start_llm: bool = True):
        """Initialize the importer with optional data directory for problem storage.
        
        Args:
            data_dir: Directory to store problem data
            auto_start_llm: Whether to automatically start the LLM server if needed
        """
        self.data_dir = Path(data_dir)
        self.ensure_data_dir()
        
        # Problem categories and types
        self.categories = {
            'Number System': ['Integers', 'Fractions', 'Decimals', 'Rational Numbers'],
            'Algebra': ['Simple Equations', 'Linear Equations', 'Expressions'],
            'Real-Life Scenarios': ['Shopping', 'Time', 'Measurement', 'Sports', 'Travel']
        }
        
        # Initialize LLM generator
        self.llm = None
        self.use_llm = False
        self._llm_server_started = False
        
        try:
            from local_llm_integration import LocalLLMGenerator, ensure_ollama_server, stop_ollama_server
            
            # Store these for later use
            self._ensure_ollama_server = ensure_ollama_server
            self._stop_ollama_server = stop_ollama_server
            
            # Initialize LLM with auto-start disabled (we'll handle it manually)
            # and use a dedicated cache directory
            self.llm = LocalLLMGenerator(
                auto_start_server=False,
                cache_dir=str(Path(data_dir) / "llm_cache")
            )
            
            # Check if we can connect to the server
            if auto_start_llm:
                self._ensure_llm_ready()
                
        except ImportError as e:
            print(f"⚠️ Local LLM generator not available: {e}")
        except Exception as e:
            print(f"⚠️ Error initializing LLM: {e}")
    
    def _ensure_llm_ready(self) -> bool:
        """Ensure LLM is ready to use, starting server if needed."""
        if not self.llm:
            return False
            
        try:
            # First try direct connection
            if self.llm._check_server():
                self.use_llm = True
                return True
                
            # If not connected, try to start the server
            print("Starting LLM server...")
            is_running, did_start = self._ensure_ollama_server()
            self._llm_server_started = did_start
            
            if is_running and self.llm._check_server():
                self.use_llm = True
                return True
                
            print("⚠️ Could not connect to LLM server. Some features may be limited.")
            return False
            
        except Exception as e:
            print(f"⚠️ Error connecting to LLM server: {e}")
            return False
    
    def __del__(self):
        """Cleanup when the importer is destroyed."""
        if self._llm_server_started and hasattr(self, '_stop_ollama_server'):
            try:
                self._stop_ollama_server()
                self._llm_server_started = False
            except Exception as e:
                print(f"⚠️ Error stopping LLM server: {e}")
        
        # Integer problem types for classification
        self.integer_problem_types = [
            'temperature', 'elevation', 'money', 'sequence', 'average',
            'quiz_scoring', 'sports', 'financial', 'academic_competition',
            'real_world', 'advanced_challenge', 'classroom', 'puzzle',
            'multi_step', 'assessment', 'real_life_scenario'
        ]
    
    def ensure_data_dir(self):
        """Ensure the data directory exists."""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def _extract_numbers(self, text: str) -> List[Dict]:
        """Extract numbers with their context from the problem text.
        
        Returns a list of dictionaries with:
        - 'value': The numeric value
        - 'unit': Unit if present (e.g., '°C', 'Rs')
        - 'context': Surrounding text for context
        """
        import re
        
        # Pattern to match numbers with optional units and context
        pattern = r'\b(\d+)(?:\.\d+)?\s*([a-zA-Z°%$€£¥]+\b)?'
        numbers = []
        
        for match in re.finditer(pattern, text):
            value = match.group(1)
            unit = match.group(2) or ''
            
            # Get surrounding context (3 words before and after)
            start = max(0, match.start() - 30)
            end = min(len(text), match.end() + 30)
            context = text[start:end]
            
            numbers.append({
                'value': value,
                'unit': unit.strip(),
                'context': context
            })
            
        return numbers
    
    def _generate_number_variation(self, value: str, unit: str = '') -> str:
        """Generate a variation of a number based on its magnitude and unit."""
        try:
            num = int(value)
            if unit in ['°C', '°F', '°']:
                # For temperatures, vary by ±30%
                variation = random.randint(
                    max(1, int(num * 0.7)),
                    int(num * 1.3) + 1
                )
            elif unit in ['Rs', '$', '€', '£', '¥']:
                # For money, vary by ±50% with whole numbers
                variation = random.randint(
                    max(1, int(num * 0.5)),
                    int(num * 1.5) + 1
                )
            else:
                # For unitless numbers, vary by ±50% with whole numbers
                variation = random.randint(
                    max(1, int(num * 0.5)),
                    int(num * 1.5) + 1
                )
            return f"{variation}{' ' + unit if unit else ''}"
        except (ValueError, TypeError):
            return f"{value}{' ' + unit if unit else ''}"
    
    def generate_variations(self, problem_text: str, problem_type: str, num_variations: int = 3) -> List[Dict[str, Any]]:
        """Generate variations of a problem using LLM.
        
        Args:
            problem_text: The original problem text
            problem_type: Type of the problem (e.g., 'Integers', 'Shopping')
            num_variations: Number of variations to generate
            
        Returns:
            List of dictionaries containing variation text and metadata
        """
        if not self.use_llm:
            return [{
                'text': problem_text,
                'explanation': 'LLM not available',
                'type': problem_type,
                'generated_at': datetime.now().isoformat()
            }]
            
        variations = []
        for i in range(num_variations):
            try:
                # Pass the variation index to ensure unique variations
                result = self.llm.generate_math_variation(problem_text, variation_index=i)
                if result and result.get('variation'):
                    # Check if this variation is different from previous ones
                    variation_text = result['variation'].strip()
                    if any(v['text'].strip() == variation_text for v in variations):
                        print(f"Skipping duplicate variation #{i+1}")
                        continue
                        
                    variations.append({
                        'text': variation_text,
                        'explanation': result.get('explanation', 'No explanation provided'),
                        'type': problem_type,
                        'generated_at': datetime.now().isoformat()
                    })
            except Exception as e:
                print(f"Error generating variation #{i+1}: {str(e)}")
                continue
                
        return variations or [{
            'text': problem_text,
            'explanation': 'No variations generated',
            'type': problem_type,
            'generated_at': datetime.now().isoformat()
        }]
    
    def import_problem(
        self, 
        problem_text: str, 
        problem_type: str,
        category: str = 'Real-Life Scenarios',
        difficulty: str = 'medium',
        source: str = 'user_import',
        grade: str = 'Grade 7'
    ) -> Dict[str, Any]:
        """Import a math problem and prepare it for worksheet generation.
        
        Args:
            problem_text: The original problem text
            problem_type: Type of problem (e.g., 'Shopping', 'Time')
            category: Problem category (e.g., 'Real-Life Scenarios', 'Number System')
            difficulty: Problem difficulty level
            source: Source of the problem
            grade: Target grade level
            
        Returns:
            Dictionary containing problem metadata (no variations included)
        """
        problem_id = f"{int(datetime.now().timestamp())}_{problem_type[:3].lower()}"
        
        problem_data = {
            'id': problem_id,
            'type': problem_type,
            'category': category,
            'difficulty': difficulty,
            'original_question': problem_text,
            'variations': [],
            'metadata': {
                'source': source,
                'date_added': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'grade': grade,
                'chapter': '',
                'subtopic': '',
                'variation_count': 0,
                'has_variations': False
            },
            'relationships': {
                'parent': None,  # This is the original problem
                'children': [],
                'related_problems': []  # For future cross-type variations
            }
        }
        
        # Save the initial problem
        problem_data = self._save_problem(problem_data)
        
        # Generate variations if LLM is available
        if self.use_llm:
            try:
                print("\nGenerating variations...")
                variations = self.generate_variations(
                    problem_text=problem_text,
                    problem_type=problem_type,
                    num_variations=3  # Generate 3 variations by default
                )
                
                if variations:
                    problem_data['variations'] = variations
                    problem_data['metadata']['variation_count'] = len(variations)
                    problem_data['metadata']['has_variations'] = True
                    problem_data['metadata']['last_updated'] = datetime.now().isoformat()
                    
                    # Save the problem with variations
                    problem_data = self._save_problem(problem_data)
                    print(f"✅ Generated {len(variations)} variations for the problem")
                
            except Exception as e:
                print(f"⚠️ Error generating variations: {str(e)}")
                import traceback
                traceback.print_exc()
        
        return problem_data
    
    def _save_problem(self, problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save a problem to the database."""
        # Ensure the problems directory exists
        problems_dir = os.path.join(self.data_dir, 'problems')
        os.makedirs(problems_dir, exist_ok=True)
        
        # Use the problem ID for the filename
        filename = f"{problem_data['id']}.json"
        filepath = os.path.join(problems_dir, filename)
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(problem_data, f, indent=2)
            
        return problem_data

    def get_available_problem_types(self) -> List[str]:
        """Get a list of available problem types for integer word problems."""
        return self.integer_problem_types


def get_user_input() -> Dict[str, str]:
    """Get user input for importing a problem."""
    importer = ProblemImporter()
    
    print("\n=== Problem Categories ===")
    for i, category in enumerate(importer.categories.keys(), 1):
        print(f"{i}. {category}")
    
    while True:
        try:
            cat_choice = int(input("\nSelect a category (number): ")) - 1
            if 0 <= cat_choice < len(importer.categories):
                category = list(importer.categories.keys())[cat_choice]
                break
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    print(f"\n=== {category} Problem Types ===")
    problem_types = importer.categories[category]
    for i, ptype in enumerate(problem_types, 1):
        print(f"{i}. {ptype}")
    
    while True:
        try:
            type_choice = int(input("\nSelect problem type (number): ")) - 1
            if 0 <= type_choice < len(problem_types):
                problem_type = problem_types[type_choice]
                break
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    print("\n=== Problem Details ===")
    print("Enter the problem text (press Enter twice when done):")
    problem_lines = []
    while True:
        line = input()
        if not line and problem_lines:
            break
        if line:
            problem_lines.append(line)
    problem_text = '\n'.join(problem_lines)
    
    difficulties = ['easy', 'medium', 'hard']
    print("\nSelect difficulty level:")
    for i, diff in enumerate(difficulties, 1):
        print(f"{i}. {diff.capitalize()}")
    
    while True:
        try:
            diff_choice = int(input("Choice (1-3): ")) - 1
            if 0 <= diff_choice < len(difficulties):
                difficulty = difficulties[diff_choice]
                break
            print("Invalid choice. Please enter a number between 1 and 3.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Include grade in the return dictionary
    return {
        'problem_text': problem_text,
        'problem_type': problem_type,
        'category': category,
        'difficulty': difficulty,
        'grade': 'Grade 7'  # Default to Grade 7 for now
    }
    
    while True:
        try:
            choice = int(input(f"\nEnter grade (1-{len(grades)}): ")) - 1
            if 0 <= choice < len(grades):
                selected_grade = grades[choice]
                break
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Problem text input
    print("\n=== Problem Text ===")
    print("Paste the problem text (press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == '':
            if lines and lines[-1] == '':
                lines.pop()
                break
        lines.append(line)
    problem_text = '\n'.join(lines).strip()
    
    if not problem_text:
        print("No problem text provided. Aborting import.")
        return None, None, None, None
    
    # Get problem type
    problem_types = importer.get_available_problem_types()
    
    print("\n=== Problem Type ===")
    print("Select the problem type:")
    for i, ptype in enumerate(problem_types, 1):
        print(f"{i}. {ptype.replace('_', ' ').title()}")
    
    while True:
        try:
            choice = int(input("\nEnter the number of the problem type: ")) - 1
            if 0 <= choice < len(problem_types):
                problem_type = problem_types[choice]
                break
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get difficulty
    difficulties = ['easy', 'medium', 'hard']
    print("\n=== Difficulty Level ===")
    print("Select the difficulty level:")
    for i, diff in enumerate(difficulties, 1):
        print(f"{i}. {diff.title()}")
    
    while True:
        try:
            choice = int(input("\nEnter the number of the difficulty level: ")) - 1
            if 0 <= choice < len(difficulties):
                difficulty = difficulties[choice]
                break
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    return problem_text, problem_type, difficulty, selected_grade


def get_problem_type() -> str:
    """Get problem type from user."""
    importer = ProblemImporter()
    print("\n=== Select Problem Type ===")
    for i, ptype in enumerate(importer.integer_problem_types, 1):
        print(f"{i}. {ptype.replace('_', ' ').title()}")
    
    while True:
        try:
            choice = int(input("\nEnter problem type number: "))
            if 1 <= choice <= len(importer.integer_problem_types):
                return importer.integer_problem_types[choice - 1]
            print(f"Please enter a number between 1 and {len(importer.integer_problem_types)}")
        except ValueError:
            print("Please enter a valid number.")

def get_difficulty() -> str:
    """Get difficulty level from user."""
    difficulties = ['easy', 'medium', 'hard']
    print("\n=== Select Difficulty ===")
    for i, diff in enumerate(difficulties, 1):
        print(f"{i}. {diff.title()}")
    
    while True:
        try:
            choice = int(input("\nEnter difficulty (1-3): "))
            if 1 <= choice <= 3:
                return difficulties[choice - 1]
            print("Please enter a number between 1 and 3")
        except ValueError:
            print("Please enter a valid number.")

def get_grade() -> str:
    """Get grade level from user."""
    print("\n=== Select Grade ===")
    grades = ['Grade 7', 'Grade 8']  # Can be expanded
    for i, grade in enumerate(grades, 1):
        print(f"{i}. {grade}")
    
    while True:
        try:
            choice = int(input("\nEnter grade (1-2): "))
            if 1 <= choice <= len(grades):
                return grades[choice - 1]
            print(f"Please enter a number between 1 and {len(grades)}")
        except ValueError:
            print("Please enter a valid number.")

def get_problem_text() -> str:
    """Get problem text from user."""
    print("\n=== Enter Problem Text ===")
    print("Paste the problem text (press Enter twice when done):\n")
    
    lines = []
    empty_lines = 0
    
    while True:
        try:
            line = input()
            if not line.strip():
                empty_lines += 1
                if empty_lines >= 2 and lines:  # Two consecutive empty lines end input
                    break
            else:
                empty_lines = 0
                lines.append(line)
        except EOFError:
            break
    
    return '\n'.join(lines).strip()

def main():
    print("=== Math Problem Importer with LLM ===")
    print("This tool helps you import math problems and generate variations using a local LLM.")
    print("Make sure you have the Ollama server running with a model like 'phi3' or 'llama3' loaded.\n")

    importer = ProblemImporter()
    
    while True:
        try:
            # Get problem details from user
            problem_data = get_user_input()
            if not problem_data:
                print("❌ No problem data provided. Exiting.")
                return

            # Import the problem
            problem = importer.import_problem(
                problem_text=problem_data['problem_text'],
                problem_type=problem_data['problem_type'],
                category=problem_data['category'],
                difficulty=problem_data['difficulty'],
                grade=problem_data['grade']
            )
            
            print("\n✅ Problem imported successfully!")
            print(f"Type: {problem['type']}")
            print(f"Category: {problem['category']}")
            print(f"Difficulty: {problem['difficulty']}")
            
            # Generate and show variations
            print("\n=== Generating Variations ===")
            variations = importer.generate_variations(
                problem['original_question'],
                problem['type'],
                num_variations=2  # Generate 2 variations for preview
            )
            
            for i, var in enumerate(variations, 1):
                print(f"\nVariation {i}:")
                print("-" * 50)
                print(var['text'])
                if 'explanation' in var:
                    print("\nExplanation:")
                    print(var['explanation'])
                print("-" * 50)
            
            # Save the problem (without variations to save space)
            save_path = f"data/problems/{problem['id']}.json"
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'w') as f:
                json.dump(problem, f, indent=2)
                
            print(f"\n✅ Problem saved to: {save_path}")
            print("\nNote: Variations are generated on-the-fly and not stored. "
                  "They will be regenerated when needed for worksheets.")
            
            # Ask if user wants to add another problem
            another = input("\nWould you like to add another problem? (y/n): ").strip().lower()
            if another not in ('y', 'yes'):
                print("\nThank you for using the Math Problem Importer!")
                break
                
            print("\n" + "="*50)
            print("ADDING ANOTHER PROBLEM")
            print("="*50 + "\n")
                
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Ask if user wants to try again
            again = input("\nWould you like to try again? (y/n): ").strip().lower()
            if again not in ('y', 'yes'):
                print("\nExiting...")
                break

if __name__ == "__main__":
    main()
