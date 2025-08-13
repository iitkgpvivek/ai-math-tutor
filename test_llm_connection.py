#!/usr/bin/env python3
"""
Test script to verify LLM connection and basic problem generation.
"""
import sys
from local_llm_integration import LocalLLMGenerator

def test_llm_connection():
    print("Testing LLM connection...")
    
    # Initialize LLM with auto-start disabled
    print("Initializing LLM...")
    llm = LocalLLMGenerator(auto_start_server=True)
    
    # Test server connection
    print("\nChecking server status...")
    if llm._check_server():
        print("✅ LLM server is running and accessible")
    else:
        print("❌ Could not connect to LLM server")
        return False
    
    # Test basic generation
    print("\nTesting basic text generation...")
    try:
        response = llm._generate_with_llm("Hello, this is a test. Please respond with 'Hello from LLM!'")
        print(f"LLM Response: {response}")
        if "hello from llm" in response.lower():
            print("✅ Basic text generation works")
            return True
        else:
            print("❌ Unexpected response from LLM")
            return False
    except Exception as e:
        print(f"❌ Error during text generation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if test_llm_connection():
        print("\n✅ LLM connection test passed!")
        sys.exit(0)
    else:
        print("\n❌ LLM connection test failed")
        sys.exit(1)
