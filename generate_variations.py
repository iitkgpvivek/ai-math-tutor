#!/usr/bin/env python3
"""
Script to generate variations for existing math problems.

This script allows you to generate variations for problems that were previously
imported but had issues with variation generation.
"""
import datetime
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add the current directory to the path so we can import local_llm_integration
sys.path.append(str(Path(__file__).parent))

from local_llm_integration import LocalLLMGenerator

class ProblemVariationGenerator:
    def __init__(self, data_dir: str = "data/problems"):
        """Initialize the variation generator with the data directory."""
        self.data_dir = Path(data_dir)
        self.llm = LocalLLMGenerator()
        
    def load_problem(self, problem_id: str) -> Optional[Dict[str, Any]]:
        """Load a problem from its ID."""
        path = self.data_dir / f"{problem_id}.json"
        if not path.exists():
            print(f"Error: Problem file {path} not found")
            return None
            
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading problem {problem_id}: {e}")
            return None
            
    def save_problem(self, problem: Dict[str, Any]) -> bool:
        """Save an updated problem back to disk."""
        try:
            path = self.data_dir / f"{problem['id']}.json"
            with open(path, 'w') as f:
                json.dump(problem, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving problem {problem.get('id', 'unknown')}: {e}")
            return False
            
    def generate_variations_for_problem(self, problem: Dict[str, Any], num_variations: int = 2) -> Dict[str, Any]:
        """Generate variations for a single problem."""
        print(f"\nGenerating {num_variations} variations for problem: {problem['id']}")
        print("-" * 80)
        print(problem['original_question'])
        print("-" * 80)
        
        # Generate variations
        variations = []
        variation_texts = set()  # Track unique variations to avoid duplicates
        
        for i in range(num_variations):
            try:
                # Pass the variation index to ensure unique variations
                result = self.llm.generate_math_variation(
                    problem['original_question'], 
                    variation_index=i
                )
                
                if not result or 'variation' not in result:
                    print(f"Warning: Failed to generate valid variation {i+1}")
                    continue
                    
                variation_text = result['variation'].strip()
                
                # Skip if we've already seen this variation
                if variation_text in variation_texts:
                    print(f"Skipping duplicate variation {i+1}")
                    continue
                    
                variation = {
                    'text': variation_text,
                    'explanation': result.get('explanation', 'No explanation provided'),
                    'source': 'llm_generated',
                    'variation_number': i + 1,
                    'generated_at': datetime.datetime.now().isoformat()
                }
                
                variations.append(variation)
                variation_texts.add(variation_text)
                
                print(f"\n✅ Variation {i+1}:")
                print("-" * 50)
                print(variation['text'])
                if 'explanation' in variation:
                    print("\n📝 Explanation:")
                    print(variation['explanation'])
                print("-" * 50)
                
            except Exception as e:
                print(f"\n❌ Error generating variation {i+1}: {e}")
                import traceback
                traceback.print_exc()
        
        # Update the problem with the new variations
        problem['variations'] = variations
        problem['metadata']['has_variations'] = len(variations) > 0
        problem['metadata']['variation_count'] = len(variations)
        problem['metadata']['last_updated'] = datetime.datetime.now().isoformat()
        
        return problem

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate variations for existing math problems')
    parser.add_argument('problem_ids', nargs='*', help='Problem IDs to generate variations for')
    parser.add_argument('--all', action='store_true', help='Process all problems')
    parser.add_argument('--num-variations', type=int, default=2, help='Number of variations to generate per problem')
    parser.add_argument('--data-dir', default='data/problems', help='Directory containing problem files')
    
    args = parser.parse_args()
    
    generator = ProblemVariationGenerator(data_dir=args.data_dir)
    
    # Get list of problem IDs to process
    if args.all:
        problem_files = list(generator.data_dir.glob('*.json'))
        problem_ids = [f.stem for f in problem_files]
    else:
        problem_ids = args.problem_ids
        if not problem_ids:
            print("No problem IDs provided. Use --all to process all problems or specify problem IDs.")
            return
    
    print(f"Generating variations for {len(problem_ids)} problems...")
    
    for problem_id in problem_ids:
        problem = generator.load_problem(problem_id)
        if problem:
            updated_problem = generator.generate_variations_for_problem(
                problem, 
                num_variations=args.num_variations
            )
            if updated_problem and generator.save_problem(updated_problem):
                print(f"\n✅ Successfully updated problem: {problem_id}")
            else:
                print(f"\n❌ Failed to update problem: {problem_id}")
        else:
            print(f"\n⚠️  Skipping problem (not found or error loading): {problem_id}")

if __name__ == "__main__":
    main()
