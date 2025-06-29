from grade7_problems import Grade7ProblemGenerator
from file_utils import save_problems_to_file

def generate_daily_problems(count=10):
    """Generate and save math problems to a file."""
    generator = Grade7ProblemGenerator()
    problems = []
    
    print(f"Generating {count} math problems...")
    
    # Generate fraction and decimal problems at hard difficulty
    problem_types = ['fraction_decimal', 'rational_number']
    
    for i in range(count):
        prob_type = problem_types[i % len(problem_types)]
        if prob_type == 'fraction_decimal':
            problem, answer = generator.generate_fraction_decimal_problem('hard')
        else:  # 'rational_number'
            problem, answer = generator.generate_rational_number_problem('hard')
            
        problems.append({
            'problem': problem,
            'answer': answer,
            'type': prob_type
        })
    
    # Save to file
    filepath = save_problems_to_file(problems)
    print(f"Problems saved to: {filepath}")
    return filepath

if __name__ == "__main__":
    generate_daily_problems(10)
