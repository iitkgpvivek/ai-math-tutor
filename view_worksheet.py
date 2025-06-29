import json
import os
from pathlib import Path

def view_latest_worksheet():
    # Find the most recent worksheet file
    data_dir = Path('data')
    worksheet_files = list(data_dir.glob('math_problems_*.json'))
    if not worksheet_files:
        print("No worksheet files found.")
        return
    
    latest_file = max(worksheet_files, key=os.path.getmtime)
    
    print(f"\n{'='*80}")
    print(f"WORKSHEET: {latest_file.name}")
    print(f"{'='*80}\n")
    
    # Read and display the problems
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    # Extract problems from the data structure
    problems = []
    if isinstance(data, dict) and 'problems' in data:
        problems = data['problems']
    elif isinstance(data, list):
        problems = data
    
    for i, item in enumerate(problems, 1):
        if isinstance(item, dict):
            print(f"{i}. {item.get('problem', 'No problem text')}")
            print(f"   Answer: {item.get('answer', 'No answer')}")
            if 'type' in item:
                print(f"   Type: {item['type']}")
            if i < len(problems):
                print()
        else:
            print(f"{i}. {str(item)}")
    
    print(f"\n{'='*80}")
    print(f"Total problems: {len(problems)}")
    print(f"{'='*80}")

if __name__ == "__main__":
    view_latest_worksheet()
