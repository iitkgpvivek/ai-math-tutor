from custom_worksheet_creator import generate_llm_problems
import time

def test_question_generation():
    # Test different problem types and difficulties
    problem_types = ['integer', 'fraction', 'decimal', 'percentage', 'ratio']
    difficulties = ['easy', 'medium', 'hard']
    
    for problem_type in problem_types:
        for difficulty in difficulties:
            print(f"\n{'='*80}")
            print(f"Testing {difficulty} {problem_type} problems:")
            print(f"{'='*80}")
            
            try:
                # Generate 2 problems of each type/difficulty
                problems = generate_llm_problems(
                    problem_type=problem_type,
                    count=2,
                    difficulty=difficulty
                )
                
                # Print the generated problems
                for i, problem in enumerate(problems, 1):
                    print(f"\nProblem {i}:")
                    print(f"Type: {problem['type']}")
                    print(f"Difficulty: {problem['difficulty']}")
                    print(f"Question: {problem['problem']}")
                    print("Solution:")
                    print(problem['solution'])
                    print("\n" + "-"*50)
                
                # Add a small delay to avoid rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"Error generating {difficulty} {problem_type} problems: {str(e)}")
                continue

if __name__ == "__main__":
    test_question_generation()
