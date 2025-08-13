import sys
from custom_worksheet_creator import generate_llm_problems

def generate_questions(problem_types=None, count=2, difficulty='medium'):
    """Generate random math questions of different types."""
    if problem_types is None:
        problem_types = ['integer', 'fraction', 'decimal', 'simple_equations']
    
    all_problems = []
    
    for p_type in problem_types:
        print(f"\n{'='*50}")
        print(f"Generating {difficulty} {p_type} problems...")
        print(f"{'='*50}")
        
        problems = generate_llm_problems(p_type, count, difficulty)
        
        if not problems:
            print(f"❌ Failed to generate {p_type} problems")
            continue
            
        all_problems.extend(problems)
        
        for i, problem in enumerate(problems, 1):
            print(f"\n📝 {p_type.capitalize()} Problem {i}:")
            print(f"\n{problem['problem']}")
            print("\n🔍 Solution:")
            print(problem['solution'])
            print("\n" + "-"*80)
    
    return all_problems

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate random math problems using AI')
    parser.add_argument('--types', nargs='+', default=['integer', 'fraction', 'decimal', 'simple_equations'],
                       help='Types of problems to generate (integer, fraction, decimal, simple_equations)')
    parser.add_argument('--count', type=int, default=2,
                       help='Number of problems to generate per type')
    parser.add_argument('--difficulty', choices=['easy', 'medium', 'hard'], default='medium',
                       help='Difficulty level of the problems')
    
    args = parser.parse_args()
    
    print("\n🎲 Generating Random Math Questions 🎲")
    print(f"Types: {', '.join(args.types)}")
    print(f"Count: {args.count} per type")
    print(f"Difficulty: {args.difficulty}")
    print("="*50 + "\n")
    
    try:
        generate_questions(args.types, args.count, args.difficulty)
    except KeyboardInterrupt:
        print("\n👋 Stopping question generation...")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    finally:
        print("\n✨ Question generation complete! ✨")
