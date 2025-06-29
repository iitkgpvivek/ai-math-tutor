from grade7_problems import Grade7ProblemGenerator

def show_problem_examples():
    generator = Grade7ProblemGenerator()
    
    print("\n=== FRACTION & DECIMAL PROBLEMS ===")
    for difficulty in ['easy', 'medium', 'hard']:
        print(f"\n--- {difficulty.upper()} ---")
        for _ in range(3):  # Show 3 examples of each
            problem, answer = generator.generate_fraction_decimal_problem(difficulty)
            print(f"Problem: {problem}")
            print(f"Answer: {answer}\n")
    
    print("\n=== RATIONAL NUMBER PROBLEMS ===")
    for difficulty in ['easy', 'medium', 'hard']:
        print(f"\n--- {difficulty.upper()} ---")
        for _ in range(3):  # Show 3 examples of each
            problem, answer = generator.generate_rational_number_problem(difficulty)
            print(f"Problem: {problem}")
            print(f"Answer: {answer}\n")

if __name__ == "__main__":
    show_problem_examples()
