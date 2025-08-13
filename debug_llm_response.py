#!/usr/bin/env python3
"""Debug script for analyzing problematic LLM responses."""

import json
import os
from datetime import datetime
from local_llm_integration import LocalLLMGenerator

class ResponseDebugger:
    def __init__(self):
        self.debug_dir = "debug_responses"
        os.makedirs(self.debug_dir, exist_ok=True)
        self.llm = LocalLLMGenerator()
    
    def save_problematic_response(self, response: str, context: dict = None):
        """Save a problematic response to a file for analysis."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.debug_dir, f"response_{timestamp}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=== ORIGINAL RESPONSE ===\n")
            f.write(response)
            f.write("\n\n=== CONTEXT ===\n")
            f.write(json.dumps(context or {}, indent=2))
            
        print(f"\n⚠️ Saved problematic response to: {filename}")
        return filename
    
    def test_parsing(self, response: str):
        """Test parsing a response with our improved method."""
        print("\n=== TESTING RESPONSE PARSING ===")
        print(f"Response length: {len(response)} characters")
        print("\nFirst 200 characters:")
        print(response[:200] + ("..." if len(response) > 200 else ""))
        
        try:
            result = self.llm._clean_json_response(response)
            print("\n✅ Successfully parsed response:")
            print(json.dumps(result, indent=2))
            return True
        except Exception as e:
            print(f"\n❌ Failed to parse response: {str(e)}")
            return False

def capture_problematic_response():
    """Run a test to capture and analyze a problematic response."""
    debugger = ResponseDebugger()
    llm = LocalLLMGenerator()
    
    # Test problem that was causing issues
    test_problem = "A train travels 300 km in 4 hours. What is its speed in km/h?"
    
    print("Testing with problem:", test_problem)
    
    try:
        # Generate a response with a very short timeout to simulate failure
        response = llm._generate_with_llm(
            "Please respond with a JSON object containing a math problem variation and explanation.",
            temperature=0.8
        )
        
        if not response:
            print("⚠️ Empty response from LLM")
            return
            
        # Save the raw response
        debug_file = debugger.save_problematic_response(
            response,
            {"test_problem": test_problem}
        )
        
        # Test parsing the response
        debugger.test_parsing(response)
        
        print(f"\nYou can examine the full response in: {debug_file}")
        
    except Exception as e:
        print(f"\n❌ Error during test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== LLM Response Debugger ===")
    print("This will test the LLM response parsing with a sample problem.")
    print("Press Ctrl+C at any time to exit.\n")
    
    capture_problematic_response()
