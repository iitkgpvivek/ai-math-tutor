import sys
import json
from local_llm_integration import LocalLLMGenerator

def test_llm_parsing():
    """Test the LLM prompt and JSON parsing with various problem types."""
    llm = LocalLLMGenerator()
    
    test_cases = [
        # Simple arithmetic
        "A car travels 450 km on 30 liters of petrol. How far will it travel on 50 liters?",
        
        # Multi-part problem
        "A test has 10 questions. Each correct answer scores 3 points, each wrong answer loses 1 point.\n"
        "(i) If a student gets 7 correct answers, what is their score?\n"
        "(ii) If another student scores 18 points, how many answers did they get correct?",
        
        # Problem with units
        "A rectangular garden is 12 meters long and 8 meters wide. What is its area in square meters?",
        
        # Problem with fractions
        "If 3/4 of a number is 27, what is the number?"
    ]
    
    for i, problem in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}:")
        print("-" * 80)
        print("ORIGINAL PROBLEM:")
        print(problem)
        
        try:
            print("\nGENERATING VARIATION...")
            result = llm.generate_math_variation(problem)
            
            print("\nRESULT:")
            print(json.dumps(result, indent=2))
            
            # Basic validation
            if not isinstance(result, dict):
                print("❌ ERROR: Result is not a dictionary")
                continue
                
            if 'variation' not in result:
                print("❌ ERROR: Missing 'variation' field")
                continue
                
            if 'explanation' not in result:
                print("⚠️ WARNING: Missing 'explanation' field")
                
            print("\nVALIDATION:")
            if not result['variation'].strip():
                print("❌ ERROR: Empty variation")
            elif not result['variation'].strip().endswith('?'):
                print("⚠️ WARNING: Variation does not end with a question mark")
            else:
                print("✅ Variation looks good!")
                
            if not result.get('explanation', '').strip():
                print("⚠️ WARNING: Empty explanation")
            else:
                print("✅ Explanation provided")
                
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*80)
    print("TESTING COMPLETE")

if __name__ == "__main__":
    test_llm_parsing()
