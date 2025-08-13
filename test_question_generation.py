import re
import json
from custom_worksheet_creator import generate_llm_problems

def validate_question(problem_text):
    """Validate that the problem text is a complete question."""
    if not problem_text.strip():
        return False, "Question is empty"
    
    # Check if it ends with a question mark
    if not problem_text.strip().endswith('?'):
        return False, "Question must end with '?'"
    
    # Check if it starts with a capital letter
    if not problem_text[0].isupper():
        return False, "Question must start with a capital letter"
    
    # Check for common question starters
    question_words = ['what', 'how', 'why', 'when', 'where', 'which', 'who', 'whom', 'whose', 'can', 'could', 'would', 'will', 
                     'is', 'are', 'was', 'were', 'do', 'does', 'did', 'find', 'calculate', 'determine', 'solve', 'compute']
    
    first_word = problem_text.lower().split()[0].strip('"\'').rstrip('?')
    if not any(first_word.startswith(word) for word in question_words):
        return False, f"Question should start with a question word (e.g., 'What', 'How', 'Find', etc.)"
    
    return True, ""

def test_question_generation():
    print("Testing question generation with enhanced prompt...\n")
    
    # Test with a single integer problem
    problems = generate_llm_problems('integer', 1, 'medium')
    
    if not problems:
        print("❌ Failed to generate any problems")
        return
    
    problem = problems[0]
    print("✅ Generated Problem:")
    print(f"\n{problem['problem']}")
    
    # Validate the problem
    is_valid, error_msg = validate_question(problem['problem'])
    if not is_valid:
        print(f"\n❌ Validation Error: {error_msg}")
    else:
        print("\n✅ Question is properly formatted")
    
    print("\n🔍 Solution:")
    print(problem['solution'])
    
    # Check if solution is complete
    if not problem['solution'].strip():
        print("\n❌ Error: Solution is empty")
    elif 'final answer' not in problem['solution'].lower():
        print("\n⚠️ Warning: Solution may be incomplete (missing 'Final answer')")
    else:
        print("\n✅ Solution appears complete")

if __name__ == "__main__":
    test_question_generation()
