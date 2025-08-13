#!/usr/bin/env python3
"""
Debug script for problem generation.
"""
import sys
import json
from problem_importer import ProblemImporter

def debug_problem_generation():
    print("=== Debugging Problem Generation ===\n")
    
    # Initialize the importer
    print("Initializing ProblemImporter...")
    importer = ProblemImporter()
    print("✅ ProblemImporter initialized\n")
    
    # Test data - Using an actual math problem instead of a prompt
    problem_data = {
        'problem_text': "A shopkeeper in Delhi has a profit of ₹2,500 on Monday and a loss of ₹1,200 on Tuesday. What is his net profit or loss for these two days?",
        'problem_type': 'integer',
        'difficulty': 'medium',
        'grade': 'Grade 7',
        'category': 'Number System',
        'source': 'debug_test'
    }
    
    print("Calling import_problem with test data...")
    try:
        result = importer.import_problem(**problem_data)
        print("\n✅ import_problem completed successfully")
        print("\n=== Result ===")
        print(json.dumps(result, indent=2, default=str))
        
        if 'variations' in result and result['variations']:
            print("\n✅ Variations generated:", len(result['variations']))
            for i, var in enumerate(result['variations'], 1):
                print(f"\n--- Variation {i} ---")
                print("Text:", var.get('text', 'No variation text'))
                print("Explanation:", var.get('explanation', 'No explanation'))
        else:
            print("\n❌ No variations generated")
            
    except Exception as e:
        print("\n❌ Error in import_problem:", str(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_problem_generation()
