"""
Examples of all problem types in the Simple Equations Generator.

This script demonstrates each type of problem that the SimpleEquationsGenerator can create,
including age-related problems, basic number problems, consecutive integers, and number reversals.
"""
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from simple_equations_generators import SimpleEquationsGenerator, Problem

def print_problem(problem: Problem):
    """Helper function to print a problem with its solution."""
    print("\n" + "="*80)
    print("PROBLEM:")
    print(problem.statement)
    print("\nSOLUTION STEPS:")
    for i, step in enumerate(problem.solution_steps, 1):
        print(f"{i}. {step}")
    print(f"\nANSWER: {problem.answer}")
    print(f"TYPE: {problem.problem_type}")
    print(f"DIFFICULTY: {problem.difficulty}")
    print("="*80 + "\n")

def generate_examples():
    """Generate and display examples of each problem type."""
    generator = SimpleEquationsGenerator()
    
    # 1. Age-Related Problems
    print("\n" + "*"*40 + "\n* AGE-RELATED PROBLEMS\n" + "*"*40)
    
    # 1.1 Age Sum Problem (Intermediate)
    print("\n1.1 Age Sum Problem:")
    problem = generator._generate_age_sum_problem()
    print_problem(problem)
    
    # 1.2 Age Difference Problem (Intermediate)
    print("\n1.2 Age Difference Problem:")
    problem = generator._generate_age_difference_problem()
    print_problem(problem)
    
    # 1.3 Age Ratio Problem (Intermediate)
    print("\n1.3 Age Ratio Problem:")
    problem = generator._generate_age_ratio_problem()
    print_problem(problem)
    
    # 1.4 Age Ratio Change Problem (Hard)
    print("\n1.4 Age Ratio Change Problem:")
    problem = generator._generate_age_ratio_change_problem()
    print_problem(problem)
    
    # 1.5 Age Three People Problem (Hard)
    print("\n1.5 Age Three People Problem:")
    problem = generator._generate_age_three_people_problem()
    print_problem(problem)
    
    # 1.6 Age Combined Conditions Problem (Hard)
    print("\n1.6 Age Combined Conditions Problem:")
    problem = generator._generate_age_combined_conditions_problem()
    print_problem(problem)
    
    # 2. Basic Number Problems (Intermediate)
    print("\n" + "*"*40 + "\n* BASIC NUMBER PROBLEMS\n" + "*"*40)
    
    # 2.1 Basic Number Problem
    print("\n2.1 Basic Number Problem:")
    problem = generator._generate_basic_number_problem()
    print_problem(problem)
    
    # 3. Consecutive Integer Problems (Hard)
    print("\n" + "*"*40 + "\n* CONSECUTIVE INTEGER PROBLEMS\n" + "*"*40)
    
    # 3.1 Two Consecutive Integers Sum
    print("\n3.1 Two Consecutive Integers Sum:")
    problem = generator._generate_consecutive_integers_problem()
    # Make sure we get the two consecutive integers type
    while problem.problem_type != 'consecutive_integers_sum':
        problem = generator._generate_consecutive_integers_problem()
    print_problem(problem)
    
    # 3.2 Three Consecutive Integers Sum
    print("\n3.2 Three Consecutive Integers Sum:")
    problem = generator._generate_consecutive_integers_problem()
    # Make sure we get the three consecutive integers type
    while problem.problem_type != 'three_consecutive_integers_sum':
        problem = generator._generate_consecutive_integers_problem()
    print_problem(problem)
    
    # 3.3 Consecutive Even/Odd Integers
    print("\n3.3 Consecutive Even/Odd Integers:")
    problem = generator._generate_consecutive_integers_problem()
    # Make sure we get the even/odd consecutive integers type
    while 'consecutive_even' not in problem.problem_type and 'consecutive_odd' not in problem.problem_type:
        problem = generator._generate_consecutive_integers_problem()
    print_problem(problem)
    
    # 4. Number Reversal Problems
    print("\n" + "*"*40 + "\n* NUMBER REVERSAL PROBLEMS\n" + "*"*40)
    
    # 4.1 Number Reversal Problem (Hard)
    print("\n4.1 Number Reversal Problem:")
    problem = generator._generate_number_reversal_problem()
    print_problem(problem)
    
    # 4.2 Number Reversal Difference
    print("\n4.2 Number Reversal (Difference):")
    problem = generator._generate_number_reversal_problem()
    # Make sure we get the difference type
    while problem.problem_type != 'number_reversal_difference':
        problem = generator._generate_number_reversal_problem()
    print_problem(problem)
    
    # 5. Money and Financial Problems
    print("\n" + "*"*40 + "\n* MONEY AND FINANCIAL PROBLEMS\n" + "*"*40)
    
    # 5.1 Basic Money Problem (Intermediate)
    print("\n5.1 Basic Money Problem (Intermediate):")
    problem = generator._generate_basic_money_problem()
    print_problem(problem)
    
    # 5.2 Discount Problem (Intermediate/Hard)
    print("\n5.2 Discount Problem (Intermediate/Hard):")
    problem = generator._generate_discount_problem()
    print_problem(problem)
    
    # 5.3 Profit/Loss Problem (Hard)
    print("\n5.3 Profit/Loss Problem (Hard):")
    problem = generator._generate_profit_loss_problem()
    print_problem(problem)
    
    # 6. Geometry Problems
    print("\n" + "*"*40 + "\n* GEOMETRY PROBLEMS\n" + "*"*40)
    
    # 6.1 Rectangle Problems
    print("\n6.1 Rectangle Area Problem:")
    problem = generator._generate_rectangle_area_problem()
    print_problem(problem)
    
    print("\n6.2 Rectangle Perimeter Problem:")
    problem = generator._generate_rectangle_perimeter_problem()
    print_problem(problem)
    
    # 6.2 Square Problems
    print("\n6.3 Square Area Problem:")
    problem = generator._generate_square_area_problem()
    print_problem(problem)
    
    print("\n6.4 Square Perimeter Problem:")
    problem = generator._generate_square_perimeter_problem()
    print_problem(problem)
    
    # 6.3 Triangle Problems
    print("\n6.5 Triangle Area Problem:")
    problem = generator._generate_triangle_area_problem()
    print_problem(problem)
    
    print("\n6.6 Triangle Perimeter Problem:")
    problem = generator._generate_triangle_perimeter_problem()
    print_problem(problem)
    
    # 6.4 Circle Problems
    print("\n6.7 Circle Area Problem:")
    problem = generator._generate_circle_area_problem()
    print_problem(problem)
    
    print("\n6.8 Circle Circumference Problem:")
    problem = generator._generate_circle_circumference_problem()
    print_problem(problem)
    
    # 7. Using the main generate_problem method
    print("\n" + "*"*40 + "\n* RANDOM PROBLEM GENERATION\n" + "*"*40)
    
    # 6.1 Random problem with intermediate difficulty
    print("\n6.1 Random Intermediate Problem:")
    problem = generator.generate_problem(difficulty='intermediate')
    print_problem(problem)
    
    # 6.2 Random problem with hard difficulty
    print("\n6.2 Random Hard Problem:")
    problem = generator.generate_problem(difficulty='hard')
    print_problem(problem)
    
    # 6.3 Completely random problem
    print("\n6.3 Completely Random Problem:")
    problem = generator.generate_problem()
    print_problem(problem)

if __name__ == "__main__":
    generate_examples()
