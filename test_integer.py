#!/usr/bin/env python3
"""
Test script for integer word problem generators.
Tests all integer problem types across all difficulty levels.
"""
from typing import Callable, Tuple, Union, List
from integer_word_problem_generators import IntegerWordProblemGenerator

def test_operation(operation_name: str, operation_func: Callable, difficulty: str, count: int = 2) -> None:
    """Helper function to test a specific operation and difficulty level.
    
    Args:
        operation_name: Name of the operation being tested
        operation_func: The function to generate problems
        difficulty: Difficulty level ('easy', 'medium', 'hard')
        count: Number of test cases to generate
    """
    print(f"\n{operation_name.upper()} - {difficulty.upper()} DIFFICULTY:" + "\n" + "-"*50)
    
    for i in range(count):
        try:
            problem, answer = operation_func(difficulty)
            print(f"Test {i+1}:")
            print(f"Problem: {problem}")
            print(f"Answer: {answer}")
            
            # Basic validation of the output
            assert isinstance(problem, str), "Problem should be a string"
            assert problem.strip() != "", "Problem should not be empty"
            
            # Answer can be int, float, str, or list depending on the problem type
            assert answer is not None, "Answer should not be None"
            assert isinstance(answer, (int, float, str, list)), \
                   f"Unexpected answer type: {type(answer)}"
            
            if isinstance(answer, (int, float)):
                assert str(answer).strip() != "", "Answer should not be empty"
            elif isinstance(answer, str):
                assert answer.strip() != "", "Answer string should not be empty"
            elif isinstance(answer, list):
                assert len(answer) > 0, "Answer list should not be empty"
                
        except Exception as e:
            print(f"Error in {operation_name} ({difficulty}): {str(e)}")
            raise

def test_all_difficulties(operation_name: str, operation_func: Callable) -> None:
    """Test an operation across all difficulty levels."""
    for difficulty in ['easy', 'medium', 'hard']:
        test_operation(operation_name, operation_func, difficulty)

def test_temperature_problems() -> None:
    """Test temperature problem generator."""
    print("\n" + "="*70)
    print("TESTING TEMPERATURE PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Temperature", IntegerWordProblemGenerator()._generate_temperature_problem)

def test_elevation_problems() -> None:
    """Test elevation problem generator."""
    print("\n" + "="*70)
    print("TESTING ELEVATION PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Elevation", IntegerWordProblemGenerator()._generate_elevation_problem)

def test_money_problems() -> None:
    """Test money problem generator."""
    print("\n" + "="*70)
    print("TESTING MONEY PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Money", IntegerWordProblemGenerator()._generate_money_problem)

def test_sequence_problems() -> None:
    """Test sequence problem generator."""
    print("\n" + "="*70)
    print("TESTING SEQUENCE PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Sequence", IntegerWordProblemGenerator()._generate_sequence_problem)

def test_average_problems() -> None:
    """Test average problem generator."""
    print("\n" + "="*70)
    print("TESTING AVERAGE PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Average", IntegerWordProblemGenerator()._generate_average_problem)

def test_quiz_scoring_problems() -> None:
    """Test quiz scoring problem generator."""
    print("\n" + "="*70)
    print("TESTING QUIZ SCORING PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Quiz Scoring", IntegerWordProblemGenerator()._generate_quiz_scoring_problem)

def test_sports_games_problems() -> None:
    """Test sports games problem generator."""
    print("\n" + "="*70)
    print("TESTING SPORTS GAMES PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Sports Games", IntegerWordProblemGenerator()._generate_sports_games_problem)

def test_financial_problems() -> None:
    """Test financial problem generator."""
    print("\n" + "="*70)
    print("TESTING FINANCIAL PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Financial", IntegerWordProblemGenerator()._generate_financial_problem)

def test_academic_competition_problems() -> None:
    """Test academic competition problem generator."""
    print("\n" + "="*70)
    print("TESTING ACADEMIC COMPETITION PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Academic Competition", IntegerWordProblemGenerator()._generate_academic_competition_problem)

def test_real_world_problems() -> None:
    """Test real world problem generator."""
    print("\n" + "="*70)
    print("TESTING REAL WORLD PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Real World", IntegerWordProblemGenerator()._generate_real_world_problem)

def test_advanced_challenge_problems() -> None:
    """Test advanced challenge problem generator."""
    print("\n" + "="*70)
    print("TESTING ADVANCED CHALLENGE PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Advanced Challenge", IntegerWordProblemGenerator()._generate_advanced_challenge_problem)

def test_classroom_problems() -> None:
    """Test classroom problem generator."""
    print("\n" + "="*70)
    print("TESTING CLASSROOM PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Classroom", IntegerWordProblemGenerator()._generate_classroom_problem)

def test_puzzle_problems() -> None:
    """Test puzzle problem generator."""
    print("\n" + "="*70)
    print("TESTING PUZZLE PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Puzzle", IntegerWordProblemGenerator()._generate_puzzle_problem)

def test_multi_step_problems() -> None:
    """Test multi-step problem generator."""
    print("\n" + "="*70)
    print("TESTING MULTI-STEP PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Multi-step", IntegerWordProblemGenerator()._generate_multi_step_problem)

def test_assessment_problems() -> None:
    """Test assessment problem generator."""
    print("\n" + "="*70)
    print("TESTING ASSESSMENT PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Assessment", IntegerWordProblemGenerator()._generate_assessment_problem)

def test_real_life_scenarios() -> None:
    """Test real life scenario generator."""
    print("\n" + "="*70)
    print("TESTING REAL LIFE SCENARIOS".center(70))
    print("="*70)
    test_all_difficulties("Real Life Scenario", IntegerWordProblemGenerator()._generate_real_life_scenario)

def test_time_zone_problems() -> None:
    """Test time zone problem generator."""
    print("\n" + "="*70)
    print("TESTING TIME ZONE PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Time Zone", IntegerWordProblemGenerator()._generate_time_zone_problem)

def test_height_change_problems() -> None:
    """Test height change problem generator."""
    print("\n" + "="*70)
    print("TESTING HEIGHT CHANGE PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Height Change", IntegerWordProblemGenerator()._generate_height_change_problem)

def test_game_scoring_problems() -> None:
    """Test game scoring problem generator."""
    print("\n" + "="*70)
    print("TESTING GAME SCORING PROBLEMS".center(70))
    print("="*70)
    test_all_difficulties("Game Scoring", IntegerWordProblemGenerator()._generate_game_scoring_problem)

def test_all_problem_types() -> None:
    """Test all problem types."""
    test_functions = [
        test_temperature_problems,
        test_elevation_problems,
        test_money_problems,
        test_sequence_problems,
        test_average_problems,
        test_quiz_scoring_problems,
        test_sports_games_problems,
        test_financial_problems,
        test_academic_competition_problems,
        test_real_world_problems,
        test_advanced_challenge_problems,
        test_classroom_problems,
        test_puzzle_problems,
        test_multi_step_problems,
        test_assessment_problems,
        test_real_life_scenarios,
        test_time_zone_problems,
        test_height_change_problems,
        test_game_scoring_problems
    ]
    
    for test_func in test_functions:
        try:
            test_func()
        except Exception as e:
            print(f"Error in {test_func.__name__}: {str(e)}")
            raise

if __name__ == "__main__":
    print("\n" + "#"*80)
    print("STARTING INTEGER WORD PROBLEM GENERATOR TESTS".center(80))
    print("#"*80 + "\n")
    
    test_all_problem_types()
    
    print("\n" + "#"*80)
    print("ALL TESTS COMPLETED SUCCESSFULLY!".center(80))
    print("#"*80)
