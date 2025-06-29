import sympy as sp
import numpy as np
import random
from typing import List, Dict, Tuple, Optional
import json
from datetime import datetime
import os

class NCERTMathAgent:
    def __init__(self):
        self.class_topics = {
            '6': ['Number System', 'Geometry', 'Integers', 'Fractions & Decimals', 'Data Handling', 'Mensuration', 'Algebra', 'Ratio & Proportion', 'Symmetry'],
            '7': ['Integers', 'Fractions & Decimals', 'Data Handling', 'Simple Equations', 'Lines & Angles', 'The Triangle & Its Properties', 'Congruence of Triangles'],
            '8': ['Rational Numbers', 'Linear Equations in One Variable', 'Understanding Quadrilaterals', 'Practical Geometry', 'Data Handling', 'Squares & Square Roots'],
            '9': ['Number Systems', 'Polynomials', 'Coordinate Geometry', 'Linear Equations in Two Variables', 'Introduction to Euclids Geometry', 'Lines & Angles'],
            '10': ['Real Numbers', 'Polynomials', 'Pair of Linear Equations in Two Variables', 'Quadratic Equations', 'Arithmetic Progressions', 'Triangles'],
            '11': ['Sets', 'Relations & Functions', 'Trigonometric Functions', 'Principle of Mathematical Induction', 'Complex Numbers & Quadratic Equations', 'Linear Inequalities']
        }
        
        self.problem_generators = {
            'algebra': self.generate_algebra_problem,
            'geometry': self.generate_geometry_problem,
            'arithmetic': self.generate_arithmetic_problem,
            'trigonometry': self.generate_trigonometry_problem
        }
        
        # Initialize progress tracking
        self.progress_file = 'progress.json'
        self.progress = self.load_progress()
        self.max_attempts = 3

    def load_progress(self) -> Dict:
        """Load user progress from file"""
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            return {}
        except json.JSONDecodeError:
            return {}

    def save_progress(self):
        """Save user progress to file"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=4)

    def update_progress(self, class_level: str, topic: str, is_correct: bool):
        """Update user's progress for a specific topic"""
        if class_level not in self.progress:
            self.progress[class_level] = {}
        
        if topic not in self.progress[class_level]:
            self.progress[class_level][topic] = {
                'correct': 0,
                'total': 0,
                'last_practiced': datetime.now().isoformat()
            }
        
        self.progress[class_level][topic]['total'] += 1
        if is_correct:
            self.progress[class_level][topic]['correct'] += 1
        self.progress[class_level][topic]['last_practiced'] = datetime.now().isoformat()
        
        self.save_progress()

    def generate_algebra_problem(self, difficulty: str = 'medium') -> Tuple[str, str]:
        """Generate an algebraic equation problem"""
        if difficulty == 'easy':
            x = sp.symbols('x')
            a = random.randint(1, 5)
            b = random.randint(1, 5)
            equation = f"{a}x + {b} = 0"
            solution = f"x = {-b/a}"
        elif difficulty == 'medium':
            x = sp.symbols('x')
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            c = random.randint(1, 10)
            equation = f"{a}x^2 + {b}x + {c} = 0"
            solution = f"x = {-b} ± sqrt({b}^2 - 4*{a}*{c}) / (2*{a})"
        else:
            x, y = sp.symbols('x y')
            a = random.randint(1, 10)
            b = random.randint(1, 10)
            c = random.randint(1, 10)
            d = random.randint(1, 10)
            equation = f"{a}x + {b}y = {c}\n{d}x - {y} = 0"
            solution = f"Solve the system of equations"
        
        return equation, solution

    def generate_geometry_problem(self, difficulty: str = 'medium') -> Tuple[str, str]:
        """Generate a geometry problem"""
        if difficulty == 'easy':
            side = random.randint(5, 20)
            problem = f"Find the area of a square with side length {side} cm."
            solution = f"Area = {side}^2 = {side**2} cm²"
        elif difficulty == 'medium':
            base = random.randint(5, 20)
            height = random.randint(5, 20)
            problem = f"Find the area of a triangle with base {base} cm and height {height} cm."
            solution = f"Area = 1/2 * {base} * {height} = {0.5 * base * height} cm²"
        else:
            radius = random.randint(5, 20)
            problem = f"Find the area and circumference of a circle with radius {radius} cm."
            solution = f"Area = π{radius}² ≈ {np.pi * radius**2:.2f} cm²\nCircumference = 2π{radius} ≈ {2 * np.pi * radius:.2f} cm"
        
        return problem, solution

    def generate_arithmetic_problem(self, difficulty: str = 'medium') -> Tuple[str, str]:
        """Generate an arithmetic problem"""
        if difficulty == 'easy':
            a = random.randint(1, 100)
            b = random.randint(1, 100)
            problem = f"What is the sum of {a} and {b}?"
            solution = f"{a} + {b} = {a + b}"
        elif difficulty == 'medium':
            a = random.randint(1, 100)
            b = random.randint(1, 100)
            c = random.randint(1, 100)
            problem = f"What is the average of {a}, {b}, and {c}?"
            solution = f"Average = ({a} + {b} + {c}) / 3 = {round((a + b + c) / 3, 2)}"
        else:
            a = random.randint(1, 100)
            b = random.randint(1, 100)
            problem = f"What is {a} as a percentage of {b}?"
            solution = f"({a} / {b}) * 100 = {(a / b) * 100:.2f}%"
        
        return problem, solution

    def generate_trigonometry_problem(self, difficulty: str = 'medium') -> Tuple[str, str]:
        """Generate a trigonometry problem"""
        if difficulty == 'easy':
            angle = random.choice([30, 45, 60])
            problem = f"What is sin({angle}°)?"
            solution = f"sin({angle}°) = {np.sin(np.radians(angle)):.2f}"
        elif difficulty == 'medium':
            angle = random.choice([30, 45, 60])
            problem = f"A ladder is leaning against a wall at an angle of {angle}°. If the ladder is 10m long, how high does it reach?"
            solution = f"Height = 10 * sin({angle}°) ≈ {10 * np.sin(np.radians(angle)):.2f} m"
        else:
            angle = random.choice([30, 45, 60])
            problem = f"In a right triangle, if one angle is {angle}° and the adjacent side is 5m, find the hypotenuse."
            solution = f"Hypotenuse = 5 / cos({angle}°) ≈ {5 / np.cos(np.radians(angle)):.2f} m"
        
        return problem, solution

    def get_random_problem(self, class_level: str, difficulty: str = 'medium') -> Tuple[str, str]:
        """Get a random problem based on class level and difficulty"""
        topics = self.class_topics.get(class_level, [])
        if not topics:
            return "Invalid class level", ""
            
        topic = random.choice(topics)
        
        # Map topics to problem generators
        if 'Algebra' in topic or 'Equations' in topic:
            return self.problem_generators['algebra'](difficulty)
        elif 'Geometry' in topic or 'Triangle' in topic:
            return self.problem_generators['geometry'](difficulty)
        elif 'Arithmetic' in topic or 'Number' in topic:
            return self.problem_generators['arithmetic'](difficulty)
        elif 'Trigonometry' in topic:
            return self.problem_generators['trigonometry'](difficulty)
        else:
            return self.problem_generators['arithmetic'](difficulty)

    def verify_solution(self, correct_answer: str, user_answer: str) -> bool:
        """Verify if the user's solution is correct"""
        try:
            # Try to evaluate both answers as mathematical expressions
            correct_val = eval(correct_answer)
            user_val = eval(user_answer)
            return abs(correct_val - user_val) < 1e-6  # Allow for small floating point errors
        except:
            # If evaluation fails, do a string comparison
            return str(correct_answer).strip() == str(user_answer).strip()

if __name__ == "__main__":
    agent = NCERTMathAgent()
    
    while True:
        print("\n" + "="*50)
        print("NCERT Math Practice Agent")
        print("="*50)
        print("\n1. Practice a problem")
        print("2. View progress")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            print("\nAvailable class levels:")
            for level in sorted(agent.class_topics.keys()):
                print(f"Class {level}")
            
            class_level = input("\nEnter class level (6-11): ").strip()
            difficulty = input("Choose difficulty (easy/medium/hard): ").strip()
            
            if class_level not in agent.class_topics:
                print("\nInvalid class level!")
                continue
                
            topic = input("Choose a topic or press Enter for random: ").strip()
            if not topic:
                topic = random.choice(agent.class_topics[class_level])
            
            print(f"\nGenerating {difficulty} difficulty problem for Class {class_level} - {topic}...")
            
            # Get a problem based on topic
            problem_type = None
            if 'Algebra' in topic or 'Equations' in topic:
                problem_type = 'algebra'
            elif 'Geometry' in topic or 'Triangle' in topic:
                problem_type = 'geometry'
            elif 'Arithmetic' in topic or 'Number' in topic:
                problem_type = 'arithmetic'
            elif 'Trigonometry' in topic:
                problem_type = 'trigonometry'
            
            if problem_type:
                problem, solution = agent.problem_generators[problem_type](difficulty)
                print("\nProblem:", problem)
                
                attempts = 0
                while attempts < agent.max_attempts:
                    user_answer = input(f"\nAttempt {attempts + 1}/{agent.max_attempts}: ").strip()
                    
                    if agent.verify_solution(solution, user_answer):
                        print("\nCorrect! Well done!")
                        agent.update_progress(class_level, topic, True)
                        break
                    else:
                        attempts += 1
                        if attempts < agent.max_attempts:
                            print(f"\nNot quite right. Try again! ({attempts}/{agent.max_attempts} attempts used)")
                        else:
                            print(f"\nMaximum attempts reached. The correct solution is:")
                            print(solution)
                            agent.update_progress(class_level, topic, False)
            else:
                print("\nCould not generate problem for this topic.")
                
        elif choice == '2':
            print("\nYour Progress:")
            for class_level, topics in agent.progress.items():
                print(f"\nClass {class_level}:")
                for topic, stats in topics.items():
                    accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
                    print(f"  {topic}:")
                    print(f"    Total attempts: {stats['total']}")
                    print(f"    Correct: {stats['correct']}")
                    print(f"    Accuracy: {accuracy:.1f}%")
                    print(f"    Last practiced: {stats['last_practiced']}")
        
        elif choice == '3':
            print("\nThank you for using NCERT Math Practice Agent!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")
