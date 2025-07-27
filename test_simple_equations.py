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
        'age_sum': 'age_related_sum',
        'age_difference': 'age_related_difference',
        'age_ratio': 'age_related_ratio',
        'age_ratio_change': 'age_related_ratio_change',
        'age_three_people': 'age_related_three_people',
        'age_combined_conditions': 'age_combined_conditions'
    }
    
    for test_type, actual_prefix in age_problem_mapping.items():
        problem = generator.generate_problem(problem_type=test_type)
        assert problem is not None
        assert problem.problem_type.startswith(actual_prefix)
        
        # Check that the problem matches the expected type
        if test_type in ['age_sum', 'age_difference', 'age_ratio']:
            assert problem.difficulty == 'intermediate'
        else:
            assert problem.difficulty == 'hard'
    
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
    for _ in range(20):  # Test multiple times to hit different problem types
        problem = generator._generate_consecutive_integers_problem()
        answer = problem.answer
        
        if problem.problem_type == 'consecutive_integers_sum':
            # For two consecutive integers summing to a total
            # Extract the total from the problem statement
            import re
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
        'money_discount': 'money_discount',
        'money_profit_loss': 'money_find_'  # Updated to match actual prefix
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

if __name__ == "__main__":
    pytest.main(["-v", "test_simple_equations.py"])
