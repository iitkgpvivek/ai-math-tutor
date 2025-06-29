import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

def save_problems_to_file(problems: List[Dict[str, Any]], filename: str = None) -> str:
    """
    Save problems to a JSON file.
    
    Args:
        problems: List of problem dictionaries
        filename: Optional custom filename (without extension)
        
    Returns:
        Path to the saved file
    """
    # Create data directory if it doesn't exist
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    # Create filename with timestamp if not provided
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'math_problems_{timestamp}'
    
    # Add .json extension if not present
    if not filename.endswith('.json'):
        filename += '.json'
    
    filepath = data_dir / filename
    
    # Prepare data to save
    data = {
        'generated_at': datetime.now().isoformat(),
        'problems': problems
    }
    
    # Save to file
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    return str(filepath)
