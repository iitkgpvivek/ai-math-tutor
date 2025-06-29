import random
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

# Add the current directory to the path so we can import our problem generator
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from grade7_problems import Grade7ProblemGenerator

# NCERT Syllabus Structure
NCERT_SYLLABUS = {
    '6': {
        'Number System': ['Whole Numbers', 'Integers', 'Fractions', 'Decimals'],
        'Algebra': ['Basic Concepts', 'Simple Equations'],
        'Geometry': ['Basic Shapes', 'Angles', 'Triangles', 'Quadrilaterals', 'Circles'],
        'Mensuration': ['Perimeter', 'Area'],
        'Data Handling': ['Pictographs', 'Bar Graphs']
    },
    '7': {
        'Number System': ['Integers', 'Fractions and Decimals', 'Rational Numbers'],
        'Algebra': ['Algebraic Expressions', 'Simple Equations', 'Exponents and Powers'],
        'Geometry': ['Lines and Angles', 'Triangles', 'Congruence', 'Symmetry'],
        'Mensuration': ['Perimeter and Area', 'Visualizing Solid Shapes'],
        'Data Handling': ['Probability', 'Chance and Probability']
    },
    '8': {
        'Number System': ['Rational Numbers', 'Squares and Square Roots', 'Cubes and Cube Roots'],
        'Algebra': ['Algebraic Expressions', 'Linear Equations in One Variable', 'Playing with Numbers'],
        'Geometry': ['Understanding Quadrilaterals', 'Practical Geometry', 'Visualizing Solid Shapes'],
        'Mensuration': ['Mensuration'],
        'Data Handling': ['Data Handling', 'Graphs']
    }
    # Can be extended for higher classes
}

class StudentProgress:
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        self.progress_file = os.path.join(data_dir, 'progress.json')
        self.progress: Dict[str, Any] = {}
        self.current_student: Optional[str] = None
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Load existing progress
        self._load_progress()
    
    def _load_progress(self):
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    self.progress = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.progress = {}
        else:
            self.progress = {}
    
    def save_progress(self):
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def get_student(self, name: str) -> Dict[str, Any]:
        """Get or create student record."""
        if name not in self.progress:
            self.progress[name] = {
                'grade': None,
                'topics': {},
                'last_activity': None,
                'difficulty_level': 'medium',  # Start with medium difficulty
                'scores': []
            }
        return self.progress[name]
    
    def update_student_grade(self, name: str, grade: str):
        student = self.get_student(name)
        student['grade'] = grade
        student['last_activity'] = datetime.now().isoformat()
        self.save_progress()
    
    def update_student_progress(self, name: str, topic: str, subtopic: str, correct: bool):
        student = self.get_student(name)
        
        # Initialize topic if not exists
        if topic not in student['topics']:
            student['topics'][topic] = {}
        if subtopic not in student['topics'][topic]:
            student['topics'][topic][subtopic] = {'attempts': 0, 'correct': 0}
        
        # Update stats
        student['topics'][topic][subtopic]['attempts'] += 1
        if correct:
            student['topics'][topic][subtopic]['correct'] += 1
        
        # Update last activity
        student['last_activity'] = datetime.now().isoformat()
        
        # Update difficulty level based on performance
        self._update_difficulty(student, correct)
        
        self.save_progress()
    
    def _update_difficulty(self, student: Dict[str, Any], correct: bool):
        """Adjust difficulty based on recent performance."""
        # Simple difficulty adjustment
        if correct and student['difficulty_level'] == 'easy':
            student['difficulty_level'] = 'medium'
        elif correct and student['difficulty_level'] == 'medium':
            student['difficulty_level'] = 'hard'
        elif not correct and student['difficulty_level'] == 'hard':
            student['difficulty_level'] = 'medium'
        elif not correct and student['difficulty_level'] == 'medium':
            student['difficulty_level'] = 'easy'

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_choice(options: List[str], prompt: str) -> int:
    """Display a menu and get user's choice."""
    while True:
        print("\n" + prompt)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        try:
            choice = int(input("\nEnter your choice: ").strip())
            if 1 <= choice <= len(options):
                return choice - 1  # Convert to 0-based index
            print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Please enter a valid number.")

def main():
    # Initialize progress tracking
    progress = StudentProgress()
    
    # Clear screen and show welcome
    clear_screen()
    print("=== NCERT Math Practice ===\n")
    
    # Get student's name
    name = input("What's your name? ").strip().title()
    student = progress.get_student(name)
    
    # Welcome back or welcome new student
    if student['grade']:
        print(f"\nWelcome back, {name}!")
        print(f"Grade: {student['grade']}")
        print(f"Difficulty: {student['difficulty_level'].title()}")
    else:
        print(f"\nHello, {name}! Let's get started with your grade.")
        
        # Grade selection
        grades = list(NCERT_SYLLABUS.keys())
        grade_choice = get_choice([f"Grade {grade}" for grade in grades], "Select your grade:")
        selected_grade = grades[grade_choice]
        progress.update_student_grade(name, selected_grade)
        print(f"\nGreat! You're in Grade {selected_grade}.")
    
    # Main menu
    while True:
        print("\n=== Main Menu ===")
        print("1. Practice")
        print("2. View Progress")
        print("3. Change Grade")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            practice_mode(progress, name, student)
        elif choice == '2':
            view_progress(student)
        elif choice == '3':
            grades = list(NCERT_SYLLABUS.keys())
            grade_choice = get_choice([f"Grade {grade}" for grade in grades], "Select your new grade:")
            selected_grade = grades[grade_choice]
            progress.update_student_grade(name, selected_grade)
            student = progress.get_student(name)  # Refresh student data
            print(f"\nGrade updated to {selected_grade}.")
        elif choice == '4':
            print("\nGoodbye! Keep practicing!")
            break
        else:
            print("\nInvalid choice. Please try again.")

def practice_mode(progress: StudentProgress, name: str, student: Dict[str, Any]):
    """Practice mode where students solve problems."""
    grade = student['grade']
    difficulty = student['difficulty_level']
    
    # Initialize problem generator
    problem_generator = Grade7ProblemGenerator()
    
    # Select topic
    topics = list(NCERT_SYLLABUS[grade].keys())
    topic_idx = get_choice(topics, "\nSelect a topic:")
    topic = topics[topic_idx]
    
    # Select subtopic or choose random
    subtopics = NCERT_SYLLABUS[grade][topic]
    print("\nAvailable subtopics:")
    for i, subtopic in enumerate(subtopics, 1):
        print(f"{i}. {subtopic}")
    print(f"{len(subtopics) + 1}. Random")
    
    try:
        subtopic_choice = input("\nSelect a subtopic (or press Enter for random): ").strip()
        if not subtopic_choice:
            subtopic = random.choice(subtopics)
        else:
            subtopic_idx = int(subtopic_choice) - 1
            if 0 <= subtopic_idx < len(subtopics):
                subtopic = subtopics[subtopic_idx]
            else:
                print("Invalid choice. Selecting random subtopic.")
                subtopic = random.choice(subtopics)
    except ValueError:
        print("Invalid input. Selecting random subtopic.")
        subtopic = random.choice(subtopics)
    
    # Generate and present problem
    print(f"\nPracticing {subtopic} in {topic} (Difficulty: {difficulty})...")
    
    try:
        # Get problem from generator
        problem, answer = problem_generator.generate_problem(topic, subtopic, difficulty)
        print(f"\nProblem: {problem}")
        
        # Get and validate user's answer
        user_answer = input("Your answer: ").strip()
        
        # Check if answer is correct
        is_correct = False
        try:
            # Try to convert both to float for numerical comparison
            user_float = float(user_answer)
            answer_float = float(answer)
            is_correct = abs(user_float - answer_float) < 0.01  # Allow for small floating point differences
        except (ValueError, TypeError):
            # For non-numerical answers, do case-insensitive string comparison
            is_correct = str(user_answer).strip().lower() == str(answer).lower()
        
        # Update progress
        progress.update_student_progress(name, topic, subtopic, is_correct)
        
        # Provide feedback
        if is_correct:
            print("✅ Correct! Great job!")
        else:
            print(f"❌ Incorrect. The correct answer is {answer}.")
            
    except Exception as e:
        print(f"\nSorry, there was an error generating the problem: {e}")
        print("Please try a different topic or subtopic.")

def view_progress(student: Dict[str, Any]):
    """Display student's progress."""
    print("\n=== Your Progress ===")
    print(f"Grade: {student['grade']}")
    print(f"Current Difficulty: {student['difficulty_level'].title()}")
    
    if not student['topics']:
        print("\nNo practice history yet.")
        return
    
    print("\nTopics practiced:")
    for topic, subtopics in student['topics'].items():
        print(f"\n{topic}:")
        for subtopic, stats in subtopics.items():
            attempts = stats['attempts']
            correct = stats['correct']
            accuracy = (correct / attempts * 100) if attempts > 0 else 0
            print(f"  - {subtopic}: {correct}/{attempts} correct ({accuracy:.1f}%)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! Your progress has been saved.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please report this issue. Your progress has been saved.")
