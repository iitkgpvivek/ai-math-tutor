#!/usr/bin/env python3
"""Test script for LLM integration with timeout and error handling."""

import time
import requests
from local_llm_integration import LocalLLMGenerator

def test_llm_with_timeout():
    print("🚀 Testing LLM integration with timeout handling...")
    
    # Initialize the LLM generator with a short timeout
    llm = LocalLLMGenerator()
    
    # Test problem
    test_problem = "A train travels 300 km in 4 hours. What is its speed in km/h?"
    
    print("\n1. Testing normal generation (should work):")
    try:
        start_time = time.time()
        result = llm.generate_math_variation(test_problem, timeout_per_attempt=30)
        elapsed = time.time() - start_time
        print(f"✅ Success! Took {elapsed:.1f} seconds")
        print(f"Variation: {result['variation']}")
        print(f"Explanation: {result['explanation']}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\n2. Testing with very short timeout (should time out):")
    try:
        # Force a longer processing time by using a very short timeout
        start_time = time.time()
        result = llm._generate_with_llm(
            "Please take at least 5 seconds to respond to this prompt.",
            timeout=1  # 1 second timeout
        )
        elapsed = time.time() - start_time
        print(f"❌ Unexpected success! Took {elapsed:.1f} seconds")
    except TimeoutError as e:
        elapsed = time.time() - start_time
        print(f"✅ Expected timeout after {elapsed:.1f} seconds: {str(e)}")
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"⚠️ Unexpected error after {elapsed:.1f} seconds: {str(e)}")
    
    print("\n3. Testing with invalid server (should fail fast):")
    try:
        # Create a new instance with invalid URL to avoid affecting other tests
        bad_llm = LocalLLMGenerator()
        bad_llm.base_url = "http://localhost:12345"  # Unlikely to be running
        
        start_time = time.time()
        result = bad_llm._generate_with_llm("Test", timeout=5)
        elapsed = time.time() - start_time
        print(f"❌ Unexpected success! Took {elapsed:.1f} seconds")
    except requests.exceptions.ConnectionError as e:
        elapsed = time.time() - start_time
        print(f"✅ Expected connection error after {elapsed:.1f} seconds: {str(e)}")
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"⚠️ Unexpected error after {elapsed:.1f} seconds: {str(e)}")

if __name__ == "__main__":
    test_llm_with_timeout()
