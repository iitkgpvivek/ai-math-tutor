import os
import sys
import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from learning_tracker import LearningTracker, StudentProgress
from problem_discovery import ProblemDiscoverer
from grade7_problems import Grade7ProblemGenerator

class EnhancedMathPractice:
    def __init__(self):
        self.tracker = LearningTracker()
        self.discoverer = ProblemDiscoverer()
        self.problem_generator = Grade7ProblemGenerator()
        self.current_student = None
        
        # Problem type mappings
        self.problem_types = {
            'number_system': [
                'integer_operations', 'fractions', 'decimals', 
                'word_problems', 'number_patterns', 'absolute_value'
            ],
            'algebra': [
                'expressions', 'equations', 'inequalities',
                'sequences', 'algebraic_word_problems'
            ],
            'geometry': [
                'angles', 'triangles', 'quadrilaterals',
                'circles', 'area_perimeter', 'volume'
            ],
            'data_handling': [
                'data_interpretation', 'probability',
                'statistics', 'graphs_charts'
            ]
        }
    
    def start(self):
        """Start the enhanced math practice application."""
        print("\n=== Enhanced Math Practice ===\n")
        self._authenticate_student()
        self._main_menu()
    
    def _authenticate_student(self):
        """Handle student authentication or registration."""
        while True:
            name = input("Enter your name (or 'exit' to quit): ").strip().title()
            if name.lower() == 'exit':
                print("Goodbye!")
                sys.exit(0)
            
            # Try to load existing student
            student_id = self._get_student_id(name)
            student = self.tracker.get_student(student_id)
            
            if student:
                print(f"\nWelcome back, {student.name}!")
                print(f"Grade: {student.grade}")
                print(f"Current Difficulty: {student.difficulty_level.title()}")
            else:
                print("\nNew student detected! Let's set up your profile.")
                grade = self._select_grade()
                difficulty = self._select_difficulty()
                student = self.tracker.create_student(name, grade, difficulty)
                print(f"\nWelcome, {student.name}! Your profile has been created.")
            
            self.current_student = student
            break
    
    def _get_student_id(self, name: str) -> str:
        """Generate a consistent student ID from name."""
        return hashlib.sha256(name.lower().encode()).hexdigest()[:8]
    
    def _select_grade(self) -> str:
        """Let student select their grade level."""
        print("\nSelect your grade level:")
        print("1. Grade 6")
        print("2. Grade 7")
        print("3. Grade 8")
        
        while True:
            choice = input("Enter your choice (1-3): ").strip()
            if choice in ['1', '2', '3']:
                return str(int(choice) + 5)  # Converts 1->6, 2->7, 3->8
            print("Invalid choice. Please try again.")
    
    def _select_difficulty(self) -> str:
        """Let student select starting difficulty."""
        print("\nSelect your starting difficulty:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        
        while True:
            choice = input("Enter your choice (1-3): ").strip()
            if choice == '1':
                return 'easy'
            elif choice == '2':
                return 'medium'
            elif choice == '3':
                return 'hard'
            print("Invalid choice. Please try again.")
    
    def _main_menu(self):
        """Display the main menu and handle user choices."""
        while True:
            print("\n=== Main Menu ===")
            print("1. Practice (Recommended)")
            print("2. Discover New Problems")
            print("3. View Progress")
            print("4. Practice Weak Areas")
            print("5. Change Settings")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                self._practice_mode()
            elif choice == '2':
                self._discover_mode()
            elif choice == '3':
                self._view_progress()
            elif choice == '4':
                self._practice_weak_areas()
            elif choice == '5':
                self._change_settings()
            elif choice == '6':
                print("\nGoodbye! Keep practicing!")
                break
            else:
                print("\nInvalid choice. Please try again.")
    
    def _practice_mode(self, topic: Optional[str] = None, subtopic: Optional[str] = None):
        """Practice math problems."""
        print("\n=== Practice Mode ===")
        
        # If topic/subtopic not provided, let student choose
        if not topic or not subtopic:
            topic, subtopic = self._select_topic_subtopic()
        
        difficulty = self.current_student.difficulty_level
        
        while True:
            # Generate problem
            problem, answer = self.problem_generator.generate_problem(topic, subtopic, difficulty)
            
            # Display problem
            print(f"\nTopic: {topic} > {subtopic}")
            print(f"Difficulty: {difficulty.title()}")
            print(f"\nProblem: {problem}")
            
            # Get and check answer
            start_time = time.time()
            user_answer = input("Your answer (or 'menu' to return): ").strip()
            
            if user_answer.lower() == 'menu':
                break
                
            time_taken = time.time() - start_time
            is_correct = self._check_answer(user_answer, answer)
            
            # Record attempt
            self.tracker.record_attempt(
                student_id=self.current_student.student_id,
                problem_text=problem,
                correct=is_correct,
                time_taken=time_taken,
                difficulty=difficulty,
                topic=topic,
                subtopic=subtopic,
                problem_type=self._determine_problem_type(problem)
            )
            
            # Update difficulty based on performance
            self._update_difficulty(is_correct)
            
            # Show feedback
            if is_correct:
                print("✅ Correct! Great job!")
            else:
                print(f"❌ Incorrect. The correct answer is {answer}.")
            
            # Ask to continue
            if input("\nPress Enter to continue or 'menu' to return: ").lower() == 'menu':
                break
    
    def _discover_mode(self):
        """Discover new problem types."""
        print("\n=== Discover New Problems ===")
        print("Searching for new problem types...")
        
        # Get topics to search for (focus on current grade level)
        topics = list(self.problem_types.keys())
        topic = random.choice(topics)  # Or let student choose
        
        # Search for new problems
        discovered = self.discoverer.discover_new_problems(
            topic=topic,
            grade=self.current_student.grade,
            max_results=5
        )
        
        if not discovered:
            print("Couldn't find new problems right now. Try again later!")
            return
        
        print(f"\nFound {len(discovered)} new problem types!")
        
        # Show discovered problems
        for i, problem in enumerate(discovered, 1):
            print(f"\n{i}. {problem['title']}")
            print(f"   Source: {problem.get('source', 'Unknown')}")
            print(f"   Type: {problem.get('problem_type', 'General')}")
        
        # Let student try one
        while True:
            choice = input("\nEnter a number to try a problem, or 'menu' to return: ").strip()
            if choice.lower() == 'menu':
                break
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(discovered):
                    self._try_discovered_problem(discovered[idx])
                    break
            except ValueError:
                pass
            
            print("Invalid choice. Please try again.")
    
    def _try_discovered_problem(self, problem: Dict):
        """Try a discovered problem."""
        print(f"\n=== New Problem Type ===")
        print(f"Title: {problem['title']}")
        print(f"Source: {problem.get('source', 'Unknown')}")
        print("\nNote: This is an external problem. Please solve it on paper.")
        print("After solving, you can enter your answer to check.")
        
        # In a real implementation, we'd fetch the actual problem content
        # For now, we'll simulate with a generated problem
        topic = problem.get('topic', 'general')
        subtopic = problem.get('subtopic', 'practice')
        difficulty = problem.get('difficulty', 'medium')
        
        generated_problem, answer = self.problem_generator.generate_problem(
            topic, subtopic, difficulty
        )
        
        print(f"\nProblem: {generated_problem}")
        
        # Get and check answer
        user_answer = input("Your answer (or 'skip' to return): ").strip()
        
        if user_answer.lower() == 'skip':
            return
        
        is_correct = self._check_answer(user_answer, answer)
        
        # Record attempt
        self.tracker.record_attempt(
            student_id=self.current_student.student_id,
            problem_text=generated_problem,
            correct=is_correct,
            time_taken=0,  # Not tracking time for external problems
            difficulty=difficulty,
            topic=topic,
            subtopic=subtopic,
            problem_type=problem.get('problem_type', 'discovered')
        )
        
        # Show feedback
        if is_correct:
            print("✅ Correct! Great job!")
        else:
            print(f"❌ Incorrect. The correct answer is {answer}.")
        
        input("\nPress Enter to continue...")
    
    def _view_progress(self):
        """View student progress and statistics."""
        summary = self.tracker.get_practice_summary(self.current_student.student_id)
        
        print("\n=== Your Progress ===")
        print(f"Total Attempts: {summary.get('total_attempts', 0)}")
        print(f"Overall Accuracy: {summary.get('accuracy', 0):.1f}%")
        
        if 'topics_accuracy' in summary and summary['topics_accuracy']:
            print("\nAccuracy by Topic:")
            for topic, accuracy in summary['topics_accuracy'].items():
                print(f"- {topic}: {accuracy:.1f}%")
        
        if 'weak_areas' in summary and summary['weak_areas']:
            print("\nAreas Needing Improvement:")
            for area, score in summary['weak_areas'].items():
                print(f"- {area} (difficulty score: {score:.2f})")
        
        if 'last_practiced' in summary and summary['last_practiced']:
            print(f"\nLast Practiced: {summary['last_practiced']}")
        
        input("\nPress Enter to continue...")
    
    def _practice_weak_areas(self):
        """Practice problems from weak areas."""
        weak_areas = self.tracker.get_recommended_topics(
            self.current_student.student_id
        )
        
        if not weak_areas:
            print("\nNot enough data to determine weak areas. Keep practicing!")
            return
        
        print("\n=== Practice Weak Areas ===")
        print("Let's focus on areas where you need more practice:")
        
        for i, (topic, subtopic) in enumerate(weak_areas, 1):
            print(f"{i}. {topic} > {subtopic}")
        
        print(f"{len(weak_areas) + 1}. Let me choose a topic")
        
        while True:
            choice = input("\nSelect an area to practice (or 'menu' to return): ").strip()
            
            if choice.lower() == 'menu':
                return
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(weak_areas):
                    topic, subtopic = weak_areas[idx]
                    self._practice_mode(topic, subtopic)
                    break
                elif idx == len(weak_areas):
                    self._practice_mode()
                    break
            except ValueError:
                pass
            
            print("Invalid choice. Please try again.")
    
    def _change_settings(self):
        """Change student settings."""
        print("\n=== Settings ===")
        print(f"Current Grade: {self.current_student.grade}")
        print(f"Current Difficulty: {self.current_student.difficulty_level.title()}")
        
        print("\n1. Change Grade Level")
        print("2. Change Difficulty")
        print("3. Back to Main Menu")
        
        while True:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                new_grade = self._select_grade()
                self.current_student.grade = new_grade
                self.tracker.save_student(self.current_student.student_id)
                print(f"Grade level updated to {new_grade}.")
                break
            elif choice == '2':
                new_difficulty = self._select_difficulty()
                self.current_student.difficulty_level = new_difficulty
                self.tracker.save_student(self.current_student.student_id)
                print(f"Difficulty level updated to {new_difficulty}.")
                break
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _select_topic_subtopic(self) -> Tuple[str, str]:
        """Let student select a topic and subtopic."""
        print("\nSelect a topic:")
        topics = list(self.problem_types.keys())
        for i, topic in enumerate(topics, 1):
            print(f"{i}. {topic.replace('_', ' ').title()}")
        
        while True:
            try:
                choice = int(input("\nEnter your choice (1-{}): ".format(len(topics)))) - 1
                if 0 <= choice < len(topics):
                    topic = topics[choice]
                    break
            except ValueError:
                pass
            print("Invalid choice. Please try again.")
        
        print(f"\nSelect a subtopic for {topic.replace('_', ' ').title()}:")
        subtopics = self.problem_types[topic]
        for i, subtopic in enumerate(subtopcs, 1):
            print(f"{i}. {subtopic.replace('_', ' ').title()}")
        
        while True:
            try:
                choice = int(input("\nEnter your choice (1-{}): ".format(len(subtopics)))) - 1
                if 0 <= choice < len(subtopics):
                    return topic, subtopics[choice]
            except ValueError:
                pass
            print("Invalid choice. Please try again.")
    
    def _check_answer(self, user_answer: str, correct_answer: Any) -> bool:
        """Check if the user's answer is correct."""
        try:
            # Try to convert both to float for numerical comparison
            user_float = float(user_answer)
            correct_float = float(correct_answer)
            return abs(user_float - correct_float) < 0.01
        except (ValueError, TypeError):
            # For non-numerical answers, do case-insensitive string comparison
            return str(user_answer).strip().lower() == str(correct_answer).lower()
    
    def _update_difficulty(self, is_correct: bool):
        """Adjust difficulty based on performance."""
        current = self.current_student.difficulty_level
        
        if is_correct:
            if current == 'easy':
                self.current_student.difficulty_level = 'medium'
            elif current == 'medium':
                self.current_student.difficulty_level = 'hard'
        else:
            if current == 'hard':
                self.current_student.difficulty_level = 'medium'
            elif current == 'medium':
                self.current_student.difficulty_level = 'easy'
        
        # Save the updated difficulty
        self.tracker.save_student(self.current_student.student_id)
    
    def _determine_problem_type(self, problem_text: str) -> str:
        """Determine the type of problem based on its content."""
        # This is a simplified version - in a real app, you'd use more sophisticated analysis
        problem_text = problem_text.lower()
        
        if any(word in problem_text for word in ['+', '-', '×', '÷', 'add', 'subtract', 'multiply', 'divide']):
            return 'arithmetic_operation'
        elif any(word in problem_text for word in ['solve', 'equation', 'x =', 'y =']):
            return 'algebra_equation'
        elif any(word in problem_text for word in ['angle', 'degree', 'triangle', 'circle']):
            return 'geometry'
        elif any(word in problem_text for word in ['percent', 'fraction', 'decimal']):
            return 'number_conversion'
        elif any(word in problem_text for word in ['if', 'then', 'how many', 'how much']):
            return 'word_problem'
        else:
            return 'general'

if __name__ == "__main__":
    import hashlib  # For student ID generation
    app = EnhancedMathPractice()
    app.start()
