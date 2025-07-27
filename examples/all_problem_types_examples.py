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
    
    # 7. Shopping and Budgeting Problems
    print("\n" + "*"*40 + "\n* SHOPPING AND BUDGETING PROBLEMS\n" + "*"*40)
    
    # 7.1 Maximum Quantity Within Budget
    print("\n7.1 Maximum Quantity Within Budget:")
    problem = generator._generate_shopping_budget_problem()
    # Make sure we get the max quantity type
    while problem.problem_type != 'shopping_max_quantity':
        problem = generator._generate_shopping_budget_problem()
    print_problem(problem)
    
    # 7.2 Remaining Money After Purchase
    print("\n7.2 Remaining Money After Purchase:")
    problem = generator._generate_shopping_budget_problem()
    # Make sure we get the remaining money type
    while problem.problem_type != 'shopping_remaining_money':
        problem = generator._generate_shopping_budget_problem()
    print_problem(problem)
    
    # 7.3 Maximum Price Per Item
    print("\n7.3 Maximum Price Per Item:")
    problem = generator._generate_shopping_budget_problem()
    # Make sure we get the max price type
    while problem.problem_type != 'shopping_max_price':
        problem = generator._generate_shopping_budget_problem()
    print_problem(problem)
    
    # 8. Time and Scheduling Problems
    print("\n" + "*"*40 + "\n* TIME AND SCHEDULING PROBLEMS\n" + "*"*40)
    
    # 8.1 Time Duration Problem
    print("\n8.1 Time Duration Calculation:")
    problem = generator._generate_time_scheduling_problem()
    # Make sure we get the time duration type
    while problem.problem_type != 'time_duration':
        problem = generator._generate_time_scheduling_problem()
    print_problem(problem)
    
    # 8.2 End Time Calculation
    print("\n8.2 End Time Calculation:")
    problem = generator._generate_time_scheduling_problem()
    # Make sure we get the end time type
    while problem.problem_type != 'end_time':
        problem = generator._generate_time_scheduling_problem()
    print_problem(problem)
    
    # 8.3 Schedule Activities
    print("\n8.3 Schedule Activities:")
    problem = generator._generate_time_scheduling_problem()
    # Make sure we get the schedule activities type
    while problem.problem_type != 'schedule_activities':
        problem = generator._generate_time_scheduling_problem()
    print_problem(problem)
    
    # 9. Mixture Problems
    print("\n" + "*"*40 + "\n* MIXTURE PROBLEMS\n" + "*"*40)
    
    # 9.1 Solution Mixture Problem (Intermediate)
    print("\n9.1 Solution Mixture Problem (Intermediate):")
    problem = generator._generate_mixture_problem('mixture_solution', 'intermediate')
    print_problem(problem)
    
    # 9.2 Alloy Mixture Problem (Hard)
    print("\n9.2 Alloy Mixture Problem (Hard):")
    problem = generator._generate_mixture_problem('mixture_alloy', 'hard')
    print_problem(problem)
    
    # 9.3 Ingredients Mixture Problem (Intermediate)
    print("\n9.3 Ingredients Mixture Problem (Intermediate):")
    problem = generator._generate_mixture_problem('mixture_ingredients', 'intermediate')
    print_problem(problem)
    
    # 9.4 Random Mixture Problem
    print("\n9.4 Random Mixture Problem:")
    problem = generator._generate_mixture_problem()
    print("\n9.6 Ingredients Mixture (Hard):")
    problem = generator._generate_mixture_problem('mixture_ingredients', 'hard')
    print_problem(problem)
    
    # 10. Work and Rate Problems
    print("\n" + "*"*40 + "\n* WORK AND RATE PROBLEMS\n" + "*"*40)
    
    # 10.1 Basic Work Rate Problem (Intermediate)
    print("\n10.1 Basic Work Rate Problem (Intermediate):")
    problem = generator._generate_work_rate_problem('basic')
    print_problem(problem)
    
    # 10.2 Combined Work Rate Problem (Hard)
    print("\n10.2 Combined Work Rate Problem (Hard):")
    problem = generator._generate_work_rate_problem('combined')
    print_problem(problem)
    
    # 10.3 Efficiency Work Rate Problem (Intermediate)
    print("\n10.3 Efficiency Work Rate Problem (Intermediate):")
    problem = generator._generate_work_rate_problem('efficiency', 'intermediate')
    print_problem(problem)
    
    # 10.4 Efficiency Work Rate Problem (Hard)
    print("\n10.4 Efficiency Work Rate Problem (Hard):")
    problem = generator._generate_work_rate_problem('efficiency', 'hard')
    print_problem(problem)
    
    # 10.5 Random Work Rate Problem
    print("\n10.5 Random Work Rate Problem:")
    problem = generator._generate_work_rate_problem()
    print_problem(problem)
    
    # 11. Distance, Rate, and Time (DRT) Problems
    print("\n" + "*"*40 + "\n* DISTANCE, RATE, AND TIME PROBLEMS\n" + "*"*40)
    
    # 11.1 Basic DRT Problem - Find Distance (Intermediate)
    print("\n11.1 Basic DRT Problem - Find Distance (Intermediate):")
    problem = generator._generate_basic_drt_problem('intermediate')
    # Make sure we get a 'find_distance' variant
    while 'how many' not in problem.statement.lower() or 'travel' not in problem.statement.lower():
        problem = generator._generate_basic_drt_problem('intermediate')
    print_problem(problem)
    
    # 11.2 Basic DRT Problem - Find Rate (Hard)
    print("\n11.2 Basic DRT Problem - Find Rate (Hard):")
    problem = generator._generate_basic_drt_problem('hard')
    # Make sure we get a 'find_rate' variant
    while 'average speed' not in problem.statement.lower():
        problem = generator._generate_basic_drt_problem('hard')
    print_problem(problem)
    
    # 11.3 Two Objects Moving Toward Each Other (Intermediate)
    print("\n11.3 Two Objects Moving Toward Each Other (Intermediate):")
    problem = generator._generate_two_objects_drt_problem('intermediate')
    # Make sure we get a 'toward' variant
    while 'toward each other' not in problem.statement:
        problem = generator._generate_two_objects_drt_problem('intermediate')
    print_problem(problem)
    
    # 11.4 Two Objects Moving Apart (Hard)
    print("\n11.4 Two Objects Moving Apart (Hard):")
    problem = generator._generate_two_objects_drt_problem('hard')
    # Make sure we get an 'away' variant
    while 'opposite directions' not in problem.statement:
        problem = generator._generate_two_objects_drt_problem('hard')
    print_problem(problem)
    
    # 11.5 Relative Speed - Overtaking (Intermediate)
    print("\n11.5 Relative Speed - Overtaking (Intermediate):")
    problem = generator._generate_relative_speed_drt_problem('intermediate')
    print_problem(problem)
    
    # 11.6 Relative Speed - Overtaking (Hard)
    print("\n11.6 Relative Speed - Overtaking (Hard):")
    problem = generator._generate_relative_speed_drt_problem('hard')
    print_problem(problem)
    
    # 11.7 Random DRT Problem
    print("\n11.7 Random DRT Problem:")
    problem = generator._generate_drt_problem()
    print_problem(problem)
    
    # 12. Using the main generate_problem method
    print("\n" + "*"*40 + "\n* RANDOM PROBLEM GENERATION\n" + "*"*40)
    
    # 11.1 Random problem with intermediate difficulty
    print("\n11.1 Random Intermediate Problem:")
    problem = generator.generate_problem(difficulty='intermediate')
    print_problem(problem)
    
    # 11.2 Random problem with hard difficulty
    print("\n11.2 Random Hard Problem:")
    problem = generator.generate_problem(difficulty='hard')
    print_problem(problem)
    
    # 11.3 Completely random problem
    print("\n11.3 Completely Random Problem:")
    problem = generator.generate_problem()
    print_problem(problem)

if __name__ == "__main__":
    generate_examples()
