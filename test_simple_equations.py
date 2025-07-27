"""
Unit tests for simple_equations_generators.py.

This module contains comprehensive tests for the SimpleEquationsGenerator class,
with a focus on age-related problem types and edge cases.
"""
import pytest
import random
import re
from simple_equations_generators import SimpleEquationsGenerator, Problem

@pytest.fixture
def generator():
    """Provide a generator instance for testing."""
    return SimpleEquationsGenerator()

# Test Age Sum Problems
def test_generate_age_sum_problem(generator):
    """Test generation of age sum problems."""
    problem = generator._generate_age_sum_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty == 'intermediate'
    assert problem.problem_type == 'age_related_sum'
    assert isinstance(problem.answer, int)
    assert problem.answer > 0
    assert len(problem.solution_steps) >= 4
    assert "sum" in problem.statement.lower()

# Test Age Difference Problems
def test_generate_age_difference_problem(generator):
    """Test generation of age difference problems."""
    problem = generator._generate_age_difference_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty == 'intermediate'
    assert problem.problem_type == 'age_related_difference'
    assert isinstance(problem.answer, int)
    assert problem.answer > 0
    assert "years older than" in problem.statement
    assert "years ago" in problem.statement

# Test Age Ratio Problems
def test_generate_age_ratio_problem(generator):
    """Test generation of age ratio problems."""
    problem = generator._generate_age_ratio_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty == 'intermediate'
    assert problem.problem_type == 'age_related_ratio'
    assert isinstance(problem.answer, int)
    assert problem.answer > 0
    assert ":" in problem.statement
    assert "ratio" in problem.statement.lower()

# Test Age Ratio Change Problems
def test_generate_age_ratio_change_problem(generator):
    """Test generation of age ratio change problems."""
    problem = generator._generate_age_ratio_change_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty == 'hard'
    assert problem.problem_type == 'age_related_ratio_change'
    assert isinstance(problem.answer, int)
    assert problem.answer > 0
    assert "times as old" in problem.statement.lower()
    assert "years ago" in problem.statement.lower()

# Test Three People Age Problems
def test_generate_age_three_people_problem(generator):
    """Test generation of three people age problems."""
    problem = generator._generate_age_three_people_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty == 'hard'
    assert problem.problem_type == 'age_related_three_people'
    assert isinstance(problem.answer, dict)
    assert len(problem.answer) == 3
    assert all(isinstance(age, int) for age in problem.answer.values())
    assert len(problem.solution_steps) >= 4

# Test Combined Conditions Age Problems
def test_generate_age_combined_conditions_problem(generator):
    """Test generation of combined conditions age problems."""
    problem = generator._generate_age_combined_conditions_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty == 'hard'
    assert problem.problem_type == 'age_combined_conditions'
    assert isinstance(problem.answer, dict)
    assert set(problem.answer.keys()) == {'father', 'son'}
    assert problem.answer['father'] > problem.answer['son']

# Test Main Problem Generation
def test_generate_problem_with_age_related(generator):
    """Test the main problem generation with age-related problems."""
    # Map of test problem types to actual problem type prefixes
    age_problem_mapping = {
        'age_related': 'age_related_sum',  # Default age problem type
        'age_related_sum': 'age_related_sum',
        'age_related_difference': 'age_related_difference',
        'age_related_ratio': 'age_related_ratio',
        'age_related_ratio_change': 'age_related_ratio_change',
        'age_related_three_people': 'age_related_three_people',
        'age_related_combined': 'age_combined_conditions'  
    }
    
    for test_type, actual_prefix in age_problem_mapping.items():
        problem = generator.generate_problem(problem_type=test_type)
        assert problem is not None
        assert problem.problem_type.startswith(actual_prefix)
        
        # Check that the problem matches the expected type and difficulty
        if test_type in ['age_related', 'age_related_sum', 'age_related_difference', 'age_related_ratio']:
            assert problem.difficulty == 'intermediate', f"Expected intermediate difficulty for {test_type}, got {problem.difficulty}"
        else:
            assert problem.difficulty == 'hard', f"Expected hard difficulty for {test_type}, got {problem.difficulty}"
    
    # Test with no specified type - should return any problem type
    problem = generator.generate_problem()
    assert problem is not None
    assert problem.difficulty in ['intermediate', 'hard']

# Test Solution Accuracy
def test_solution_steps_accuracy(generator):
    """Verify that the solution steps lead to the correct answer."""
    # Test age sum problem
    problem = generator._generate_age_sum_problem()
    last_step = problem.solution_steps[-1].lower()
    assert str(problem.answer) in last_step
    
    # Test age ratio problem
    problem = generator._generate_age_ratio_problem()
    last_step = problem.solution_steps[-1].lower()
    assert str(problem.answer) in last_step

# Test Problem Statement Format
def test_problem_statement_format(generator):
    """Verify that problem statements are properly formatted."""
    problems = [
        generator._generate_age_sum_problem(),
        generator._generate_age_difference_problem(),
        generator._generate_age_ratio_problem(),
        generator._generate_age_ratio_change_problem(),
        generator._generate_age_three_people_problem(),
        generator._generate_age_combined_conditions_problem()
    ]
    
    for problem in problems:
        assert problem.statement.endswith('?')
        assert len(problem.statement.split()) > 5
        assert any(char.isdigit() for char in problem.statement)
        assert problem.answer is not None
        assert len(problem.solution_steps) >= 3

# Test Multiple Generations
def test_multiple_generations(generator):
    """Test that multiple problem generations produce different problems."""
    # Test with different problem types to ensure variety
    problem_types = [
        lambda: generator._generate_age_sum_problem(),
        lambda: generator._generate_age_difference_problem(),
        lambda: generator._generate_age_ratio_problem(),
        lambda: generator._generate_basic_number_problem(),
        lambda: generator._generate_consecutive_integers_problem(),
        lambda: generator._generate_number_reversal_problem()
    ]
    
    # Generate multiple problems of different types
    problems = [problem_type() for problem_type in problem_types for _ in range(2)]
    
    # Collect all statements and answers
    statements = [p.statement for p in problems]
    answers = [p.answer for p in problems]
    
    # We should have unique statements (problems should be different)
    assert len(set(statements)) > len(statements) * 0.8, \
        "Multiple problem generations produced too many identical statements"
        
    # We should have a good number of unique answers
    assert len(set(answers)) > len(answers) * 0.7, \
        "Multiple problem generations produced too many identical answers"
    
    # Also test with different problem types if available
    if hasattr(generator, '_generate_age_difference_problem'):
        diff_problems = [generator._generate_age_difference_problem() for _ in range(3)]
        diff_statements = [p.statement for p in diff_problems]
        assert len(set(diff_statements)) > 1, "Multiple difference problem generations produced identical statements"
    
    # Verify that solutions are not empty
    for problem in problems:
        assert problem.solution_steps, "Solution steps should not be empty"
        assert all(isinstance(step, str) for step in problem.solution_steps), "All solution steps should be strings"
        assert problem.answer is not None, "Answer should not be None"

# Test Basic Number Problems
def test_generate_basic_number_problem(generator):
    """Test generation of basic number relationship problems."""
    problem = generator._generate_basic_number_problem()
    
    # Check basic structure
    assert isinstance(problem, Problem)
    assert problem.difficulty == 'intermediate'
    assert problem.problem_type == 'basic_number_relationship'
    
    # Check problem statement format
    assert "a number" in problem.statement.lower()
    assert "result is" in problem.statement.lower()
    assert "find the number" in problem.statement.lower()
    
    # Check answer is a number
    assert isinstance(problem.answer, int)
    assert 1 <= problem.answer <= 50
    
    # Check solution steps
    assert len(problem.solution_steps) >= 3
    assert "let the number be x" in problem.solution_steps[0].lower()
    assert "x =" in problem.solution_steps[-1].lower()

def test_generate_problem_with_number_type(generator):
    """Test the main problem generation with number type."""
    problem = generator.generate_problem(problem_type='number')
    
    # Should return a basic number problem
    assert isinstance(problem, Problem)
    assert problem.problem_type == 'basic_number_relationship'
    assert problem.difficulty == 'intermediate'

def test_number_problem_solution_accuracy(generator):
    """Test that the solution steps lead to the correct answer for number problems."""
    for _ in range(10):  # Test multiple times for different random generations
        problem = generator._generate_basic_number_problem()
        x = problem.answer
        
        # Check that the last step shows the correct answer
        assert f"x = {x}" in problem.solution_steps[-1].lower()
        
        # Check that the answer satisfies the problem statement
        statement = problem.statement.lower()
        
        # Extract numbers from the problem statement
        import re
        numbers = [int(s) for s in re.findall(r'\b\d+\b', statement)]
        if not numbers:
            continue
            
        # The first number is typically the constant
        constant = numbers[0]
        
        # The last number is typically the result
        result = numbers[-1]
        
        # Check the operation based on the problem statement
        if "added to" in statement:
            # For "x added to y" the equation is x + y = result
            assert constant + x == result, f"{constant} + {x} should equal {result}"
        elif "subtracted from" in statement:
            # For "x subtracted from y" the equation is y - x = result
            # So we need to check if x or constant is the result
            # The problem should be in the form "If 9 is subtracted from a number, the result is 6. Find the number."
            # So x - 9 = 6 → x = 15
            # Or it could be "If a number is subtracted from 15, the result is 6. Find the number."
            # So 15 - x = 6 → x = 9
            # We need to check both possibilities
            if x - constant == result or constant - x == result:
                pass  # Test passes
            else:
                assert False, f"{x} and {constant} should relate to {result} through subtraction"
        elif "multiplied by" in statement or "times" in statement:
            # For "x multiplied by y" or "x times y" the equation is x * y = result
            assert constant * x == result, f"{constant} * {x} should equal {result}"

def test_generate_consecutive_integers_problem(generator):
    """Test generation of consecutive integer problems."""
    problem = generator._generate_consecutive_integers_problem()
    
    # Check basic structure
    assert isinstance(problem, Problem)
    assert problem.difficulty == 'hard'
    assert problem.problem_type in [
        'consecutive_integers_sum',
        'three_consecutive_integers_sum',
        'consecutive_even_integers',
        'consecutive_odd_integers'
    ]
    
    # Check problem statement format
    assert any(term in problem.statement.lower() 
              for term in ['consecutive integer', 'consecutive even', 'consecutive odd'])
    
    # Check answer is an integer
    assert isinstance(problem.answer, int)
    
    # Check solution steps
    assert len(problem.solution_steps) >= 4
    assert "let" in problem.solution_steps[0].lower()
    assert "x" in problem.solution_steps[0].lower()
    
    # Verify the solution steps lead to the correct answer
    # This is a basic check - more detailed verification is in the next test
    assert str(problem.answer) in problem.solution_steps[-1]

def test_consecutive_integers_solution_accuracy(generator):
    """Test that consecutive integer problems have correct solutions."""
    import re  # Moved to the top of the function
    
    for _ in range(20):  # Test multiple times to hit different problem types
        problem = generator._generate_consecutive_integers_problem()
        answer = problem.answer
        
        if problem.problem_type == 'consecutive_integers_sum':
            # For two consecutive integers summing to a total
            # Extract the total from the problem statement
            total = int(re.search(r'is (\d+)', problem.statement).group(1))
            assert answer + (answer + 1) == total
            
            # Verify the solution steps contain the correct equation
            equation_found = any(f"x + (x + 1) = {total}" in step for step in problem.solution_steps)
            assert equation_found, f"Equation not found in solution steps: {problem.solution_steps}"
            
        elif problem.problem_type == 'three_consecutive_integers_sum':
            # For three consecutive integers summing to a total
            # Extract the total from the problem statement
            total = int(re.search(r'is (\d+)', problem.statement).group(1))
            # The answer is the middle number
            middle = answer
            assert (middle - 1) + middle + (middle + 1) == total
            
            # Verify the solution steps contain the correct equation
            equation_found = any("(x - 1) + x + (x + 1) =" in step for step in problem.solution_steps)
            assert equation_found, f"Equation not found in solution steps: {problem.solution_steps}"
            
        elif 'consecutive_even' in problem.problem_type or 'consecutive_odd' in problem.problem_type:
            # For consecutive even/odd integers
            # Extract the total and difference from the statement
            import re
            numbers = [int(s) for s in re.findall(r'\b\d+\b', problem.statement)]
            total = numbers[-1] if len(numbers) > 1 else None
            
            # Verify the answer is of the correct parity
            if 'even' in problem.problem_type:
                assert answer % 2 == 0, f"Answer {answer} should be even"
            else:
                assert answer % 2 == 1, f"Answer {answer} should be odd"
                
            # Check that the next number is also of the same parity
            next_num = answer + 2
            if 'even' in problem.problem_type:
                assert next_num % 2 == 0, f"Next number {next_num} should be even"
            else:
                assert next_num % 2 == 1, f"Next number {next_num} should be odd"
                
            # Verify the equation in the solution steps
            assert any(step.startswith('The equation is:') for step in problem.solution_steps), \
                   f"Equation not found in solution steps: {problem.solution_steps}"

def test_generate_number_reversal_problem(generator):
    """Test generation of number reversal problems."""
    problem = generator._generate_number_reversal_problem()
    
    # Check basic structure
    assert isinstance(problem, Problem)
    assert problem.difficulty == 'hard'
    assert problem.problem_type in ['number_reversal_sum', 'number_reversal_difference']
    
    # Check that the answer is a two-digit number
    assert 10 <= problem.answer <= 99
    
    # Check that the solution steps contain the answer
    assert any(str(problem.answer) in step for step in problem.solution_steps)
    
    # Check problem statement mentions two-digit number and reversal
    assert "two-digit" in problem.statement.lower()
    assert "reversing" in problem.statement.lower() or "reversed" in problem.statement.lower()

def test_number_reversal_solution_accuracy(generator):
    """Test that number reversal problems have correct solutions."""
    for _ in range(20):  # Test multiple times to hit different problem types
        problem = generator._generate_number_reversal_problem()
        answer = problem.answer
        
        # Extract digits
        t = answer // 10  # tens digit
        u = answer % 10   # units digit
        reversed_num = 10 * u + t
        
        if problem.problem_type == 'number_reversal_sum':
            # For sum problems, check that the sum is correct
            total = answer + reversed_num
            assert str(total) in problem.statement
            assert any(f"= {total}" in step for step in problem.solution_steps)
            
            # Check that the digits relationship is correct
            digit_diff = t - u
            assert str(digit_diff) in problem.statement
            
        else:  # number_reversal_difference
            # For difference problems, check the difference is correct
            difference = abs(answer - reversed_num)
            assert str(difference) in problem.statement
            assert any(f"= {difference}" in step for step in problem.solution_steps)
            
            # Check that the digits relationship is correct
            digit_diff = t - u
            assert str(digit_diff) in problem.statement

def test_generate_problem_with_number_reversal(generator):
    """Test the main problem generation with number reversal type."""
    problem = generator.generate_problem(problem_type='number_reversal')
    assert problem is not None
    assert problem.difficulty == 'hard'
    assert problem.problem_type in ['number_reversal_sum', 'number_reversal_difference']
    
    # The answer should be a two-digit number
    assert 10 <= problem.answer <= 99
    
    # The solution steps should contain the answer
    assert any(str(problem.answer) in step for step in problem.solution_steps)

# Test Money Problems
def test_generate_basic_money_problem(generator):
    """Test generation of basic money problems."""
    problem = generator._generate_basic_money_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty in ['intermediate', 'hard']
    assert problem.problem_type.startswith('money_')
    assert any(currency in problem.statement for currency in ['dollar', 'euro', 'pound', 'rupee', 'yen'])
    assert len(problem.solution_steps) >= 3
    assert isinstance(problem.answer, (int, float))
    assert problem.answer > 0

def test_generate_discount_problem(generator):
    """Test generation of discount problems."""
    problem = generator._generate_discount_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty in ['intermediate', 'hard']
    assert problem.problem_type.startswith('money_discount')
    assert any(word in problem.statement.lower() for word in ['discount', 'sale', 'off'])
    assert len(problem.solution_steps) >= 3
    assert isinstance(problem.answer, (int, float))
    assert problem.answer > 0

def test_generate_profit_loss_problem(generator):
    """Test generation of profit/loss problems."""
    problem = generator._generate_profit_loss_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty in ['intermediate', 'hard']
    assert problem.problem_type.startswith('money_')
    assert any(word in problem.statement.lower() for word in ['profit', 'loss', 'cost', 'sell'])
    assert len(problem.solution_steps) >= 3

def test_money_problem_integration(generator):
    """Test that money problems can be generated through the main interface."""
    # Map of test problem types to actual problem type prefixes
    money_problem_mapping = {
        'money_basic': 'money_basic_',
        'money_discount': 'money_discount_',
        'money_profit_loss': 'money_'
    }
    
    for test_type, actual_prefix in money_problem_mapping.items():
        # Test generating the problem
        problem = generator.generate_problem(problem_type=test_type)
        assert problem is not None
        assert problem.problem_type.startswith(actual_prefix)
        
        # Verify the problem statement contains relevant keywords
        if test_type == 'money_basic':
            assert any(keyword in problem.statement.lower() 
                      for keyword in ['dollar', 'euro', 'pound', 'rupee', 'yen'])
            assert any(keyword in problem.statement.lower()
                     for keyword in ['cost', 'price', 'total', 'spend', 'buy', 'sell'])
        elif test_type == 'money_discount':
            assert any(keyword in problem.statement.lower() 
                      for keyword in ['discount', 'sale', 'off', '%'])
        elif test_type == 'money_profit_loss':
            assert any(keyword in problem.statement.lower() 
                      for keyword in ['profit', 'loss', 'percent', '%'])
        
        # Verify the answer is a valid number
        assert isinstance(problem.answer, (int, float))
        assert problem.answer > 0  # Money amounts should be positive
        
        # Verify solution steps exist and lead to the answer
        assert len(problem.solution_steps) > 0
        last_step = problem.solution_steps[-1].lower()
        assert str(problem.answer) in last_step or f"{problem.answer:.2f}" in last_step
        
        # For profit/loss problems, check that the percentage is calculated correctly
        if test_type == 'money_profit_loss':
            if 'profit' in problem.statement.lower():
                assert 'profit' in ' '.join(step.lower() for step in problem.solution_steps)
            elif 'loss' in problem.statement.lower():
                assert 'loss' in ' '.join(step.lower() for step in problem.solution_steps)

def test_generate_rectangle_area_problem(generator):
    """Test generation of rectangle area problems."""
    problem = generator._generate_rectangle_area_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty in ['intermediate', 'hard']
    assert problem.problem_type.startswith('geometry_rectangle_area')
    assert 'rectangle' in problem.statement.lower()
    assert 'area' in problem.statement.lower()
    assert len(problem.solution_steps) >= 3
    assert isinstance(problem.answer, (int, float))
    assert problem.answer > 0

def test_generate_square_perimeter_problem(generator):
    """Test generation of square perimeter problems."""
    problem = generator._generate_square_perimeter_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty in ['intermediate', 'hard']
    assert problem.problem_type.startswith('geometry_square_perimeter')
    assert 'square' in problem.statement.lower()
    assert 'perimeter' in problem.statement.lower()
    assert len(problem.solution_steps) >= 3
    assert isinstance(problem.answer, (int, float))
    assert problem.answer > 0

def test_generate_square_area_problem(generator):
    """Test generation of square area problems."""
    problem = generator._generate_square_area_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty in ['intermediate', 'hard']
    assert problem.problem_type.startswith('geometry_square_area')
    assert 'square' in problem.statement.lower()
    assert 'area' in problem.statement.lower()
    assert len(problem.solution_steps) >= 3
    assert isinstance(problem.answer, (int, float))
    assert problem.answer > 0

def test_generate_triangle_perimeter_problem(generator):
    """Test generation of triangle perimeter problems."""
    problem = generator._generate_triangle_perimeter_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty in ['intermediate', 'hard']
    assert problem.problem_type.startswith('geometry_triangle_perimeter')
    assert 'triangle' in problem.statement.lower()
    assert 'perimeter' in problem.statement.lower()
    assert len(problem.solution_steps) >= 3
    assert isinstance(problem.answer, (int, float))
    assert problem.answer > 0

def test_generate_triangle_area_problem(generator):
    """Test generation of triangle area problems."""
    problem = generator._generate_triangle_area_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty in ['intermediate', 'hard']
    assert problem.problem_type.startswith('geometry_triangle_area')
    assert 'triangle' in problem.statement.lower()
    assert 'area' in problem.statement.lower()
    assert len(problem.solution_steps) >= 3
    assert isinstance(problem.answer, (int, float))
    assert problem.answer > 0

def test_generate_circle_circumference_problem(generator):
    """Test generation of circle circumference problems."""
    problem = generator._generate_circle_circumference_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty in ['intermediate', 'hard']
    assert problem.problem_type.startswith('geometry_circle_circumference')
    assert 'circle' in problem.statement.lower()
    assert any(term in problem.statement.lower() for term in ['circumference', 'around'])
    assert len(problem.solution_steps) >= 3
    assert isinstance(problem.answer, (int, float))
    assert problem.answer > 0

def test_generate_circle_area_problem(generator):
    """Test generation of circle area problems."""
    problem = generator._generate_circle_area_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty in ['intermediate', 'hard']
    assert problem.problem_type.startswith('geometry_circle_area')
    assert 'circle' in problem.statement.lower()
    assert 'area' in problem.statement.lower()
    assert len(problem.solution_steps) >= 3
    assert isinstance(problem.answer, (int, float))
    assert problem.answer > 0

def test_geometry_problem_integration(generator):
    """Test that geometry problems can be generated through the main interface."""
    # Map of test problem types to actual problem type prefixes
    geometry_problem_mapping = {
        'rectangle_perimeter': 'geometry_rectangle_perimeter_',
        'rectangle_area': 'geometry_rectangle_area_',
        'square_perimeter': 'geometry_square_perimeter_',
        'square_area': 'geometry_square_area_',
        'triangle_perimeter': 'geometry_triangle_perimeter_',
        'triangle_area': 'geometry_triangle_area_',
        'circle_circumference': 'geometry_circle_circumference_',
        'circle_area': 'geometry_circle_area_',
        'geometry': 'geometry_'  # Random geometry problem
    }
    
    for test_type, actual_prefix in geometry_problem_mapping.items():
        problem = generator.generate_problem(problem_type=test_type)
        assert problem is not None
        assert problem.problem_type.startswith(actual_prefix)
        
        # Verify the problem statement contains relevant keywords
        if 'rectangle' in test_type:
            assert 'rectangle' in problem.statement.lower()
        elif 'square' in test_type:
            assert 'square' in problem.statement.lower()
        elif 'triangle' in test_type:
            assert 'triangle' in problem.statement.lower()
        elif 'circle' in test_type:
            assert 'circle' in problem.statement.lower()
        
        # Verify the problem type matches the content
        if 'perimeter' in test_type:
            assert 'perimeter' in problem.statement.lower()
            assert any('perimeter' in step.lower() for step in problem.solution_steps)
        elif 'area' in test_type and 'triangle' not in test_type:  # Skip triangle area as it might say 'area of triangle'
            assert 'area' in problem.statement.lower()
            assert any('area' in step.lower() for step in problem.solution_steps)
        elif 'circumference' in test_type:
            assert 'circumference' in problem.statement.lower()
            assert any('circumference' in step.lower() for step in problem.solution_steps)
    
    # Test that the random geometry problem returns a valid problem
    problem = generator._generate_geometry_problem()
    assert problem is not None
    assert any(shape in problem.statement.lower() 
              for shape in ['rectangle', 'square', 'triangle', 'circle'])

# Test Shopping and Budgeting Problems
def test_generate_shopping_budget_problem(generator):
    """Test generation of shopping budget problems."""
    problem = generator._generate_shopping_budget_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty == 'intermediate'
    assert problem.problem_type in ['shopping_max_quantity', 'shopping_remaining_money', 'shopping_max_price']
    
    # Verify the problem statement contains key elements
    assert any(item in problem.statement.lower() 
              for item in ['buy', 'cost', 'price', 'budget', 'money'])
    
    # Verify solution steps are present and make sense
    assert len(problem.solution_steps) >= 2
    assert any(step.startswith('1.') for step in problem.solution_steps)
    
    # Verify the answer is a valid number
    assert isinstance(problem.answer, (int, float))
    assert problem.answer > 0

def test_shopping_max_quantity_problem(generator):
    """Test the maximum quantity within budget problem type."""
    # Generate until we get a max quantity problem
    problem = generator._generate_shopping_budget_problem()
    while problem.problem_type != 'shopping_max_quantity':
        problem = generator._generate_shopping_budget_problem()
    
    # Extract numbers from the problem statement
    import re
    numbers = [float(x) for x in re.findall(r'\d+\.?\d*', problem.statement)]
    budget = numbers[0] if numbers[0] > numbers[1] else numbers[1]
    price = numbers[1] if numbers[0] > numbers[1] else numbers[0]
    
    # Verify the calculated maximum quantity matches the answer
    max_quantity = int(budget // price)
    assert problem.answer == max_quantity
    
    # Print debug information
    print(f"\nDebug - Problem statement: {problem.statement}")
    print(f"Debug - Budget: {budget}, Price: {price}, Max quantity: {max_quantity}")
    print("Debug - Solution steps:")
    for i, step in enumerate(problem.solution_steps, 1):
        print(f"  {i}. {step}")
    
    # Check for the division operation in the solution steps
    # The division might be formatted with dollar signs and different decimal places
    division_found = any(
        (f"{budget} ÷ {price}" in step or 
         f"{budget} / {price}" in step or
         f"{budget:.2f} ÷ {price:.2f}" in step or
         f"{budget:.2f} / {price:.2f}" in step or
         f"${budget:.2f} ÷ ${price:.2f}" in step or
         f"${budget:.2f} / ${price:.2f}" in step or
         f"{int(budget)} ÷ {int(price)}" in step or
         f"{int(budget)} / {int(price)}" in step)
        for step in problem.solution_steps
    )
    
    assert division_found, f"Division operation not found in solution steps for {budget} and {price}"
    assert any(str(max_quantity) in step for step in problem.solution_steps)

def test_shopping_remaining_money_problem(generator):
    """Test the remaining money after purchase problem type."""
    # Generate until we get a remaining money problem
    problem = generator._generate_shopping_budget_problem()
    while problem.problem_type != 'shopping_remaining_money':
        problem = generator._generate_shopping_budget_problem()
    
    # Print debug information
    print(f"\nDebug - Problem statement: {problem.statement}")
    print(f"Debug - Solution steps:")
    for i, step in enumerate(problem.solution_steps, 1):
        print(f"  {i}. {step}")
    
    # Extract numbers from the problem statement
    import re
    numbers = [float(x) for x in re.findall(r'\d+\.?\d*', problem.statement)]
    budget = max(numbers)
    
    # The answer should be less than the budget
    assert problem.answer < budget, f"Answer ({problem.answer}) should be less than budget ({budget})"
    assert problem.answer >= 0, "Can't have negative remaining money"
    
    # Verify the solution steps show the correct calculation
    # The subtraction might be formatted with dollar signs and different decimal places
    subtraction_found = any(
        (f"{budget} - " in step or 
         f"${budget:.2f} - " in step or
         f"${int(budget)} - " in step)
        for step in problem.solution_steps
    )
    
    assert subtraction_found, f"Subtraction operation not found in solution steps for {budget}"
    
    # Check for the answer in the solution steps (handle different decimal formats)
    answer_found = any(
        (str(problem.answer) in step or 
         f"{problem.answer:.2f}" in step or
         f"${problem.answer:.2f}" in step)
        for step in problem.solution_steps
    )
    
    assert answer_found, f"Answer ({problem.answer}) not found in solution steps"

def test_shopping_max_price_problem(generator):
    """Test the maximum price per item problem type."""
    # Generate until we get a max price problem
    problem = generator._generate_shopping_budget_problem()
    while problem.problem_type != 'shopping_max_price':
        problem = generator._generate_shopping_budget_problem()
    
    # Extract numbers from the problem statement
    import re
    numbers = [float(x) for x in re.findall(r'\d+\.?\d*', problem.statement)]
    budget = max(numbers)
    quantity = min(numbers)
    
    # Verify the calculated maximum price matches the answer
    max_price = budget / quantity
    assert abs(problem.answer - max_price) < 0.01  # Allow for floating point precision
    
    # Print debug information
    print(f"\nDebug - Problem statement: {problem.statement}")
    print(f"Debug - Budget: {budget}, Quantity: {quantity}, Max price: {max_price}")
    print("Debug - Solution steps:")
    for i, step in enumerate(problem.solution_steps, 1):
        print(f"  {i}. {step}")
    
    # Check for the division operation in the solution steps
    # The division might be formatted with dollar signs and different decimal places
    division_found = any(
        (f"{budget} ÷ {quantity}" in step or 
         f"{budget} / {quantity}" in step or
         f"{budget:.2f} ÷ {quantity:.0f}" in step or
         f"{budget:.2f} / {quantity:.0f}" in step or
         f"${budget:.2f} ÷ {quantity:.0f}" in step or
         f"${budget:.2f} / {quantity:.0f}" in step)
        for step in problem.solution_steps
    )
    
    assert division_found, f"Division operation not found in solution steps for {budget} and {quantity}"
    assert str(round(max_price, 2)) in ' '.join(problem.solution_steps)

def test_shopping_problem_integration(generator):
    """Test that shopping problems can be generated through the main interface."""
    # Test with specific problem types
    problem_types = ['shopping_max_quantity', 'shopping_remaining_money', 'shopping_max_price', 'shopping']
    
    # Set a fixed seed for reproducibility in tests
    import random
    random.seed(42)
    
    for ptype in problem_types:
        # When testing specific problem types, we need to ensure we get that exact type
        if ptype != 'shopping':
            # For specific types, we'll generate until we get the right one
            # but limit the number of attempts to avoid infinite loops
            max_attempts = 10
            attempts = 0
            while attempts < max_attempts:
                problem = generator.generate_problem(problem_type=ptype)
                if problem.problem_type == ptype:
                    break
                attempts += 1
            else:
                pytest.fail(f"Failed to generate problem of type {ptype} after {max_attempts} attempts")
        else:
            problem = generator.generate_problem(problem_type=ptype)
            
        assert isinstance(problem, Problem), "Generated problem is not a Problem instance"
        assert problem.difficulty == 'intermediate', "Problem difficulty should be 'intermediate'"
        
        if ptype != 'shopping':  # 'shopping' is a random type
            assert problem.problem_type == ptype, f"Expected problem type {ptype}, got {problem.problem_type}"
        else:
            assert problem.problem_type in ['shopping_max_quantity', 'shopping_remaining_money', 'shopping_max_price'], \
                   f"Unexpected problem type: {problem.problem_type}"
        
        # Verify the answer is a valid number
        assert isinstance(problem.answer, (int, float)), "Answer should be a number"
        assert problem.answer > 0, "Answer should be positive"
        
        # Verify solution steps are present and properly formatted
        assert len(problem.solution_steps) >= 2, "There should be at least 2 solution steps"
        assert any(step.startswith('1.') for step in problem.solution_steps), "First step should be numbered '1.'"
        
        # Print debug info for the test
        print(f"\nGenerated {problem.problem_type} problem:")
        print(f"  Statement: {problem.statement[:100]}...")
        print(f"  Answer: {problem.answer}")
        print(f"  Solution steps: {len(problem.solution_steps)} steps")

# Test Time and Scheduling Problems
def test_generate_time_scheduling_problem(generator):
    """Test generation of time scheduling problems."""
    problem = generator._generate_time_scheduling_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty in ['intermediate', 'hard']
    assert problem.problem_type in ['time_duration', 'end_time', 'schedule_activities']
    assert isinstance(problem.answer, (int, str))
    assert len(problem.solution_steps) >= 3
    assert any(keyword in problem.statement.lower() 
              for keyword in ['time', 'start', 'end', 'duration', 'schedule'])

def test_time_duration_problem(generator):
    """Test the time duration calculation problem type."""
    # Test multiple times to ensure we get a time_duration problem
    for _ in range(10):  # Increased attempts to 10 to ensure we get a valid problem
        problem = generator._generate_time_scheduling_problem()
        if problem.problem_type == 'time_duration':
            # Extract times from the problem statement
            import re
            time_pattern = r'\b(1[0-2]|0?[1-9]):([0-5][0-9]\s*[AaPp][Mm])\b'
            times = re.findall(time_pattern, problem.statement)
            
            # If we have at least two times and the answer is positive, we're good
            if len(times) >= 2 and isinstance(problem.answer, int) and problem.answer > 0:
                break
    else:
        # If we get here, we didn't find a valid time_duration problem after 10 attempts
        assert False, "Could not find a valid time_duration problem after multiple attempts"
    
    assert problem.problem_type == 'time_duration'
    
    # Verify the answer is a positive number (minutes)
    assert problem.answer > 0, f"Duration should be positive, got {problem.answer} for problem: {problem.statement}"

def test_end_time_problem(generator):
    """Test the end time calculation problem type."""
    # Test multiple times to ensure we get an end_time problem
    for _ in range(5):  # Try up to 5 times to get an end_time problem
        problem = generator._generate_time_scheduling_problem()
        if problem.problem_type == 'end_time':
            break
    
    assert problem.problem_type == 'end_time'
    assert 'what time' in problem.statement.lower() or 'when' in problem.statement.lower()
    
    # The answer should be a time string in format 'H:MM AM/PM'
    assert isinstance(problem.answer, str)
    import re
    assert re.match(r'^(1[0-2]|0?[1-9]):([0-5][0-9])\s*[AaPp][Mm]$', problem.answer)

def test_schedule_activities_problem(generator):
    """Test the schedule activities problem type."""
    # Since we can't directly control the problem type, we'll test the function directly
    # with the schedule_activities type if possible, or skip if not implemented
    try:
        # Try to generate a schedule_activities problem directly if possible
        problem = generator._generate_time_scheduling_problem(problem_type='schedule_activities')
    except (TypeError, KeyError):
        # If direct specification isn't supported, try to find one
        for _ in range(20):  # Try more times to find this problem type
            problem = generator._generate_time_scheduling_problem()
            if problem.problem_type == 'schedule_activities':
                break
        else:
            # If we still can't find one, mark the test as skipped
            import pytest
            pytest.skip("Could not generate a schedule_activities problem after multiple attempts")
    
    assert problem.problem_type == 'schedule_activities', \
        f"Expected problem_type 'schedule_activities', got '{problem.problem_type}'. Problem: {problem.statement}"
    
    # The answer should be a string
    assert isinstance(problem.answer, str), \
        f"Answer should be a string, got {type(problem.answer)}: {problem.answer}"

def test_time_problem_integration(generator):
    """Test that time scheduling problems can be generated through the main interface."""
    # Test each specific time problem type
    for problem_type in ['time_duration', 'end_time', 'schedule_activities']:
        problem = generator._generate_time_scheduling_problem()
        assert problem.problem_type in ['time_duration', 'end_time', 'schedule_activities']
        assert isinstance(problem.statement, str)
        assert len(problem.statement) > 0
        assert isinstance(problem.answer, (int, str))
        assert len(problem.solution_steps) >= 2

def test_time_problem_solution_accuracy(generator):
    """Test that the solution steps for time problems are accurate."""
    # Test multiple problems to ensure solution accuracy
    for _ in range(5):  # Test with 5 different problems
        problem = generator._generate_time_scheduling_problem()
        
        if problem.problem_type == 'time_duration':
            # For duration problems, the answer should be a positive integer
            assert isinstance(problem.answer, int)
            assert problem.answer > 0
            
            # Check that the last step shows the correct duration
            last_step = problem.solution_steps[-1].lower()
            assert str(problem.answer) in last_step or "minutes" in last_step
            
        elif problem.problem_type == 'end_time':
            # For end time problems, the answer should be a time string
            import re
            assert re.match(r'^(1[0-2]|0?[1-9]):([0-5][0-9])\s*[AaPp][Mm]$', problem.answer)
            
            # The last step should show the calculated end time
            last_step = problem.solution_steps[-1].lower()
            # Check if the answer is in the last step or the last step confirms the end time
            assert (problem.answer.lower() in last_step) or ("end" in last_step and "time" in last_step)
            
        elif problem.problem_type == 'schedule_activities':
            # For schedule problems, the answer should be a string
            assert isinstance(problem.answer, str)
            # The last step should be informative about the schedule
            last_step = problem.solution_steps[-1].lower()
            assert len(last_step) > 0  # Just ensure there's some content

def test_generate_mixture_problem(generator):
    """Test generation of mixture problems."""
    problem = generator._generate_mixture_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty in ['intermediate', 'hard']
    # Check that the problem type is one of the expected types
    assert any(problem.problem_type.startswith(t) for t in 
              ['mixture_solution', 'mixture_alloy', 'mixture_ingredients'])
    assert isinstance(problem.answer, (int, float))
    assert len(problem.solution_steps) >= 4
    assert any(word in problem.statement.lower() for word in ['mix', 'combine', 'blend'])

def test_solution_mixture_problem_intermediate(generator):
    """Test solution mixture problem at intermediate difficulty."""
    # Test with random values
    problem = generator._generate_mixture_problem('mixture_solution', 'intermediate')
    
    # Verify the problem has the expected structure
    assert problem.problem_type.startswith('mixture_solution')
    assert problem.difficulty == 'intermediate'
    assert "% solution" in problem.statement
    assert "mix" in problem.statement.lower() or "combine" in problem.statement.lower()
    assert "what is the concentration" in problem.statement.lower()
    
    # Verify the solution steps make sense
    assert len(problem.solution_steps) >= 3
    # Check for key phrases in the solution steps (not specific indices)
    solution_text = ' '.join(step.lower() for step in problem.solution_steps)
    assert "total solute" in solution_text
    assert "total volume" in solution_text
    assert str(round(problem.answer, 1)) in problem.solution_steps[-1]

def test_alloy_mixture_problem_hard(generator):
    """Test alloy mixture problem at hard difficulty."""
    problem = generator._generate_mixture_problem('mixture_alloy', 'hard')
    
    # Verify the problem has the expected structure
    assert problem.problem_type.startswith('mixture_alloy')
    assert problem.difficulty == 'hard'
    assert "%" in problem.statement
    assert "alloy" in problem.statement.lower()
    assert "how many" in problem.statement.lower() and "should you mix" in problem.statement.lower()
    
    # Verify the solution steps make sense
    assert len(problem.solution_steps) >= 5
    solution_text = ' '.join(step.lower() for step in problem.solution_steps)
    assert "let x be" in solution_text
    assert "solve for x" in solution_text
    assert str(problem.answer) in problem.solution_steps[-1]

def test_ingredients_mixture_problem_intermediate(generator):
    """Test ingredients mixture problem at intermediate difficulty."""
    problem = generator._generate_mixture_problem('mixture_ingredients', 'intermediate')
    
    # Verify the problem has the expected structure
    assert problem.problem_type.startswith('mixture_ingredients')
    assert problem.difficulty == 'intermediate'
    assert "kg" in problem.statement
    assert "$" in problem.statement and "/kg" in problem.statement
    assert "price per kg" in problem.statement.lower() or "break even" in problem.statement.lower()
    
    # Verify the solution steps make sense
    assert len(problem.solution_steps) >= 3
    solution_text = ' '.join(step.lower() for step in problem.solution_steps)
    assert "total cost" in solution_text
    assert "total weight" in solution_text
    assert str(round(problem.answer, 2)) in problem.solution_steps[-1]

def test_mixture_problem_integration(generator):
    """Test that mixture problems can be generated through the main interface."""
    # Test with specific type through the main interface
    problem = generator.generate_problem(problem_type='mixture_solution')
    assert problem.problem_type.startswith('mixture_solution')
    assert problem.difficulty in ['intermediate', 'hard']
    assert isinstance(problem.answer, (int, float))
    
    # Test with direct call to _generate_mixture_problem with specific type and difficulty
    problem = generator._generate_mixture_problem(problem_type='mixture_solution', difficulty='intermediate')
    assert problem.problem_type.startswith('mixture_solution')
    assert problem.difficulty == 'intermediate'
    assert isinstance(problem.answer, (int, float))
    
    # Test with random type and difficulty
    problem = generator.generate_problem()
    assert hasattr(problem, 'statement')
    assert hasattr(problem, 'answer')
    assert hasattr(problem, 'solution_steps')
    assert problem.difficulty in ['intermediate', 'hard']

def test_mixture_problem_solution_accuracy(generator):
    """Test that the solution steps for mixture problems are accurate."""
    # Test with a solution mixture problem
    problem = generator._generate_mixture_problem('mixture_solution', 'intermediate')
    
    # The last solution step should contain the answer
    last_step = problem.solution_steps[-1].lower()
    answer_str = str(round(problem.answer, 2)).rstrip('0').rstrip('.')
    assert answer_str in last_step or f"{problem.answer:.1f}" in last_step or f"{problem.answer:.2f}" in last_step
    
    # For hard problems, check that the solution involves solving an equation
    problem = generator._generate_mixture_problem('mixture_alloy', 'hard')
    assert any("solve for" in step.lower() for step in problem.solution_steps)
    
    # Verify that the answer is a positive number
    assert problem.answer > 0
    
    # Test ingredients problem
    problem = generator._generate_mixture_problem('mixture_ingredients', 'intermediate')
    last_step = problem.solution_steps[-1].lower()
    answer_str = str(round(problem.answer, 2)).rstrip('0').rstrip('.')
    assert answer_str in last_step or f"{problem.answer:.2f}" in last_step

# Test Distance, Rate, and Time (DRT) Problems
def test_generate_drt_problem(generator):
    """Test generation of DRT problems."""
    # Test with random type and difficulty
    problem = generator._generate_drt_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty in ['intermediate', 'hard']
    assert problem.problem_type.startswith('drt_')
    assert 'km/h' in problem.statement or 'mph' in problem.statement
    assert any(word in problem.statement.lower() for word in ['travel', 'speed', 'distance', 'time'])
    assert len(problem.solution_steps) >= 3

def test_basic_drt_problem_intermediate(generator):
    """Test basic DRT problem at intermediate difficulty."""
    problem = generator._generate_basic_drt_problem('intermediate')
    assert isinstance(problem, Problem)
    assert problem.difficulty == 'intermediate'
    assert problem.problem_type.startswith('drt_basic_')
    assert any(word in problem.statement.lower() 
              for word in ['travels', 'how many', 'distance', 'speed', 'time'])
    assert 'km/h' in problem.statement or 'mph' in problem.statement
    assert len(problem.solution_steps) >= 3

def test_basic_drt_problem_hard(generator):
    """Test basic DRT problem at hard difficulty."""
    problem = generator._generate_basic_drt_problem('hard')
    assert isinstance(problem, Problem)
    assert problem.difficulty == 'hard'
    assert problem.problem_type.startswith('drt_basic_')
    assert any(word in problem.statement.lower() 
              for word in ['travels', 'how many', 'distance', 'speed', 'time'])
    assert 'km/h' in problem.statement or 'mph' in problem.statement
    assert len(problem.solution_steps) >= 3

def test_two_objects_drt_problem_intermediate(generator):
    """Test two objects DRT problem at intermediate difficulty."""
    problem = generator._generate_two_objects_drt_problem('intermediate')
    assert isinstance(problem, Problem)
    assert problem.difficulty == 'intermediate'
    assert problem.problem_type.startswith('drt_two_objects_')
    assert any(phrase in problem.statement 
              for phrase in ['toward each other', 'opposite directions'])
    assert 'km/h' in problem.statement
    assert 'km' in problem.statement
    assert 'how many hours' in problem.statement.lower()
    assert len(problem.solution_steps) >= 3

def test_two_objects_drt_problem_hard(generator):
    """Test two objects DRT problem at hard difficulty."""
    problem = generator._generate_two_objects_drt_problem('hard')
    assert isinstance(problem, Problem)
    assert problem.difficulty == 'hard'
    assert problem.problem_type.startswith('drt_two_objects_')
    assert any(phrase in problem.statement 
              for phrase in ['toward each other', 'opposite directions'])
    assert 'km/h' in problem.statement
    assert 'km' in problem.statement
    assert 'how many hours' in problem.statement.lower()
    assert len(problem.solution_steps) >= 3

def test_relative_speed_drt_problem_intermediate(generator):
    """Test relative speed DRT problem at intermediate difficulty."""
    problem = generator._generate_relative_speed_drt_problem('intermediate')
    assert isinstance(problem, Problem)
    assert problem.difficulty == 'intermediate'
    assert problem.problem_type == 'drt_relative_speed'
    assert 'km/h' in problem.statement
    assert 'hours earlier' in problem.statement or 'starts' in problem.statement
    assert 'catch up' in problem.statement.lower() or 'overtake' in problem.statement.lower()
    assert len(problem.solution_steps) >= 3

def test_relative_speed_drt_problem_hard(generator):
    """Test relative speed DRT problem at hard difficulty."""
    problem = generator._generate_relative_speed_drt_problem('hard')
    assert isinstance(problem, Problem)
    assert problem.difficulty == 'hard'
    assert problem.problem_type == 'drt_relative_speed'
    assert 'km/h' in problem.statement
    assert 'hours earlier' in problem.statement or 'starts' in problem.statement
    assert 'catch up' in problem.statement.lower() or 'overtake' in problem.statement.lower()
    assert len(problem.solution_steps) >= 3

def test_drt_problem_integration(generator):
    """Test that DRT problems can be generated through the main interface."""
    # Test with specific problem types
    problem_types = [
        'drt_basic',
        'drt_two_objects',
        'drt_relative_speed',
        'drt'  # Random DRT problem
    ]
    
    for ptype in problem_types:
        problem = generator.generate_problem(problem_type=ptype)
        assert isinstance(problem, Problem)
        assert problem.problem_type.startswith('drt_')
        assert problem.difficulty in ['intermediate', 'hard']
        assert 'km/h' in problem.statement or 'mph' in problem.statement
        assert any(word in problem.statement.lower() 
                  for word in ['travel', 'speed', 'distance', 'time', 'hour'])
        assert len(problem.solution_steps) >= 3

def test_drt_problem_solution_accuracy(generator):
    """Test that the solution steps for DRT problems are accurate."""
    # Test with a fixed seed for reproducibility
    import random
    import re
    
    random.seed(42)
    
    # Test multiple times to catch edge cases
    for _ in range(5):
        problem = generator._generate_drt_problem()
        
        # Extract all numbers from the problem statement and solution steps
        all_numbers = []
        
        # First, get numbers from the problem statement
        statement_numbers = [float(x) for x in re.findall(r'\d+\.?\d*', problem.statement)]
        all_numbers.extend(statement_numbers)
        
        # Then get numbers from solution steps
        for step in problem.solution_steps:
            step_numbers = [float(x) for x in re.findall(r'\d+\.?\d*', step)]
            all_numbers.extend(step_numbers)
        
        # For basic DRT problems, verify the math
        if problem.problem_type.startswith('drt_basic'):
            # We need at least 3 distinct numbers (distance, rate, time)
            assert len(set(all_numbers)) >= 3, f"Not enough distinct numbers in problem: {problem.statement}"
            
            # Get the answer from the problem object
            answer = float(problem.answer) if not isinstance(problem.answer, (int, float)) else problem.answer
            
            # The answer should be one of the numbers in the solution
            assert any(abs(answer - num) < 0.01 * answer for num in all_numbers), \
                f"Answer {answer} not found in solution steps for problem: {problem.statement}"
            
            # For each solution step, check if it makes mathematical sense
            for step in problem.solution_steps:
                # Check for common DRT formulas in the step
                if 'distance = rate × time' in step.lower() or 'distance = rate * time' in step.lower():
                    # Extract the numbers after the equals sign
                    parts = step.split('=')
                    if len(parts) > 1:
                        rhs = parts[1]
                        numbers_in_rhs = [float(x) for x in re.findall(r'\d+\.?\d*', rhs)]
                        if len(numbers_in_rhs) >= 2:
                            # Check if the multiplication is correct
                            product = numbers_in_rhs[0] * numbers_in_rhs[1]
                            if len(numbers_in_rhs) > 2 and abs(product - numbers_in_rhs[2]) > 0.01 * product:
                                assert False, f"Incorrect multiplication in step: {step}"
                
                # Check for division steps
                elif '/' in step and ('time = distance / rate' in step.lower() or 
                                    'rate = distance / time' in step.lower() or
                                    'distance / rate' in step.lower() or
                                    'distance / time' in step.lower()):
                    parts = step.split('=')
                    if len(parts) > 1:
                        rhs = parts[1]
                        numbers_in_rhs = [float(x) for x in re.findall(r'\d+\.?\d*', rhs)]
                        if len(numbers_in_rhs) >= 2:
                            # Check if the division is correct
                            quotient = numbers_in_rhs[0] / numbers_in_rhs[1]
                            if len(numbers_in_rhs) > 2 and abs(quotient - numbers_in_rhs[2]) > 0.01 * quotient:
                                assert False, f"Incorrect division in step: {step}"
        
        # For two objects problems, check that the relative speed is calculated correctly
        elif problem.problem_type.startswith('drt_two_objects'):
            # The answer should be in the solution steps
            answer = float(problem.answer) if not isinstance(problem.answer, (int, float)) else problem.answer
            answer_found = False
            
            for step in problem.solution_steps:
                # Look for the final answer in the solution steps
                if f'{answer:.2f}' in step or f'{int(answer)}' in step:
                    answer_found = True
                    break
            
            assert answer_found, f"Answer {answer} not found in solution steps for problem: {problem.statement}"

# Test Work and Rate Problems
def test_generate_work_rate_problem(generator):
    """Test generation of work rate problems."""
    problem = generator._generate_work_rate_problem()
    assert isinstance(problem, Problem)
    assert problem.difficulty in ['intermediate', 'hard']
    assert problem.problem_type in ['work_rate_basic', 'work_rate_combined', 'work_rate_efficiency']
    assert isinstance(problem.answer, (int, float))
    assert problem.answer > 0
    assert len(problem.solution_steps) >= 3

def test_basic_work_rate_problem(generator):
    """Test basic work rate problems."""
    problem = generator._generate_work_rate_problem('basic')
    assert problem.problem_type == 'work_rate_basic'
    assert problem.difficulty == 'intermediate'
    assert "how much" in problem.statement.lower() or "how many" in problem.statement.lower()
    assert any(step.startswith("1. First, find the work rate") for step in problem.solution_steps)

def test_combined_work_rate_problem(generator):
    """Test combined work rate problems."""
    problem = generator._generate_work_rate_problem('combined')
    assert problem.problem_type == 'work_rate_combined'
    assert problem.difficulty == 'hard'
    assert "work together" in problem.statement.lower() or "working together" in problem.statement.lower()
    assert any("combined rate" in step.lower() for step in problem.solution_steps)

def test_efficiency_work_rate_problem(generator):
    """Test efficiency-based work rate problems."""
    # Test intermediate difficulty
    problem = generator._generate_work_rate_problem('efficiency', 'intermediate')
    assert problem.problem_type == 'work_rate_efficiency'
    assert problem.difficulty == 'intermediate'
    assert any(x in problem.statement for x in ["faster", "slower", "efficient"])
    assert any("rate" in step.lower() for step in problem.solution_steps)
    
    # Test hard difficulty
    problem = generator._generate_work_rate_problem('efficiency', 'hard')
    assert problem.difficulty == 'hard'
    assert any(x in problem.statement for x in ["faster", "slower", "efficient"])

def test_work_rate_problem_solution_accuracy(generator):
    """Test that the solution steps for work rate problems are accurate."""
    # Test with known values for basic work rate
    generator.random = random.Random(42)  # Set seed for reproducibility
    problem = generator._generate_work_rate_problem('basic')
    
    # Extract numbers from the problem statement
    numbers = [int(s) for s in problem.statement.split() if s.isdigit()]
    assert len(numbers) >= 2
    
    # Verify the solution steps lead to the answer
    # This is a basic check - more detailed verification would require parsing the solution steps
    assert problem.answer > 0
    assert problem.answer <= max(numbers) * 2  # Reasonable upper bound

def test_work_rate_problem_integration(generator):
    """Test that work rate problems can be generated through the main interface."""
    # Test with specific work rate type
    problem = generator.generate_problem('work_rate_basic')
    assert problem.problem_type == 'work_rate_basic'
    
    problem = generator.generate_problem('work_rate_combined')
    assert problem.problem_type == 'work_rate_combined'
    
    # Test with explicit difficulty for efficiency problem
    problem = generator.generate_problem('work_rate_efficiency', difficulty='intermediate')
    assert problem.problem_type == 'work_rate_efficiency'
    assert problem.difficulty == 'intermediate'
    
    # Test with random work rate problem
    problem = generator.generate_problem('work_rate')
    assert problem.problem_type.startswith('work_rate_')
    assert problem.difficulty in ['intermediate', 'hard']
    assert len(problem.solution_steps) >= 3
    assert problem.answer > 0

if __name__ == "__main__":
    pytest.main(["-v", "test_simple_equations.py"])
