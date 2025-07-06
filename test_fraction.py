#!/usr/bin/env python3
"""
Test script for fraction operations problem generators.
Tests addition, subtraction, and multiplication of fractions.
"""
from fractions_word_problem_generators import FractionWordProblemGenerator

def test_operation(operation_name, operation_func, difficulty, count=3):
    """Helper function to test a specific operation and difficulty level."""
    print(f"\n{operation_name.upper()} - {difficulty.upper()} DIFFICULTY:" + "\n" + "-"*50)
    generator = FractionWordProblemGenerator()
    
    for _ in range(count):
        problem, answer = operation_func(difficulty)
        print(f"Problem: {problem}")
        print(f"Answer: {answer}\n")

def test_addition_problems():
    """Test the fraction addition problem generator with all difficulty levels."""
    print("\n" + "="*60)
    print("TESTING FRACTION ADDITION PROBLEMS".center(60))
    print("="*60)
    
    for difficulty in ['easy', 'medium', 'hard']:
        test_operation("Addition", 
                      lambda d: FractionWordProblemGenerator()._generate_addition_problem(d), 
                      difficulty)

def test_subtraction_problems():
    """Test the fraction subtraction problem generator with all difficulty levels."""
    print("\n" + "="*60)
    print("TESTING FRACTION SUBTRACTION PROBLEMS".center(60))
    print("="*60)
    
    for difficulty in ['easy', 'medium', 'hard']:
        test_operation("Subtraction",
                      lambda d: FractionWordProblemGenerator()._generate_subtraction_problem(d),
                      difficulty)

def test_multiplication_problems():
    """Test the fraction multiplication problem generator with all difficulty levels."""
    print("\n" + "="*60)
    print("TESTING FRACTION MULTIPLICATION PROBLEMS".center(60))
    print("="*60)
    
    for difficulty in ['easy', 'medium', 'hard']:
        test_operation("Multiplication",
                      lambda d: FractionWordProblemGenerator()._generate_multiplication_problem(d),
                      difficulty)

def test_division_problems():
    """Test the fraction division problem generator with all difficulty levels."""
    print("\n" + "="*60)
    print("TESTING FRACTION DIVISION PROBLEMS".center(60))
    print("="*60)
    
    for difficulty in ['easy', 'medium', 'hard']:
        test_operation("Division",
                      lambda d: FractionWordProblemGenerator()._generate_division_problem(d),
                      difficulty)

def test_comparison_problems():
    """Test the fraction comparison problem generator with all difficulty levels."""
    print("\n" + "="*60)
    print("TESTING FRACTION COMPARISON PROBLEMS".center(60))
    print("="*60)
    
    for difficulty in ['easy', 'medium', 'hard']:
        test_operation("Comparison",
                      lambda d: FractionWordProblemGenerator()._generate_comparison_problem(d),
                      difficulty)

def test_conversion_problems():
    """Test the fraction conversion problem generator with all difficulty levels."""
    print("\n" + "="*60)
    print("TESTING FRACTION CONVERSION PROBLEMS".center(60))
    print("="*60)
    
    for difficulty in ['easy', 'medium', 'hard']:
        test_operation("Conversion",
                      lambda d: FractionWordProblemGenerator()._generate_conversion_problem(d),
                      difficulty)

def test_mixed_operations_problems():
    """Test the mixed operations problem generator with all difficulty levels."""
    print("\n" + "="*60)
    print("TESTING MIXED OPERATIONS PROBLEMS".center(60))
    print("="*60)
    
    for difficulty in ['easy', 'medium', 'hard']:
        test_operation("Mixed Operations",
                     lambda d: FractionWordProblemGenerator()._generate_mixed_operations_problem(d),
                     difficulty)

def test_measurement_problems():
    """Test the measurement problem generator with all difficulty levels."""
    print("\n" + "="*60)
    print("TESTING MEASUREMENT PROBLEMS".center(60))
    print("="*60)
    
    for difficulty in ['easy', 'medium', 'hard']:
        test_operation("Measurement",
                      lambda d: FractionWordProblemGenerator()._generate_measurement_problem(d),
                      difficulty,
                      count=2)  # Fewer tests since measurement problems are more complex

def test_all_operations():
    """Test all fraction operations."""
    test_addition_problems()
    test_subtraction_problems()
    test_multiplication_problems()
    test_division_problems()
    test_comparison_problems()
    test_conversion_problems()
    test_mixed_operations_problems()
    test_measurement_problems()

if __name__ == "__main__":
    test_all_operations()
