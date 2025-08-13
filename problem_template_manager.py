"""
Problem Template Manager

This module handles loading and managing problem templates from JSON files
and using them to generate similar problems with Mistral.
"""

import json
import os
import random
from pathlib import Path
from typing import Dict, List, Optional, TypedDict, Set


class ProblemTemplate(TypedDict):
    """Type definition for a problem template."""
    id: str
    type: str
    category: str
    difficulty: str
    original_question: str
    variations: List[Dict[str, str]]


class ProblemTemplateManager:
    """Manages problem templates for generating similar problems."""
    
    def __init__(self, templates_dir: str = "data/problems"):
        """Initialize the template manager.
        
        Args:
            templates_dir: Directory containing problem template JSON files
        """
        self.templates_dir = Path(templates_dir)
        self.templates: List[ProblemTemplate] = []
        self._load_templates()
        self.used_template_ids: Set[str] = set()
    
    def _load_templates(self) -> None:
        """Load all problem templates from the templates directory."""
        if not self.templates_dir.exists():
            print(f"Warning: Templates directory {self.templates_dir} does not exist")
            return
            
        for file_path in self.templates_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    template = json.load(f)
                    # Ensure required fields exist
                    if all(key in template for key in ['id', 'type', 'difficulty', 'original_question']):
                        if 'variations' not in template:
                            template['variations'] = []
                        self.templates.append(template)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading template {file_path}: {e}")
    
    def get_templates_by_type_and_difficulty(
        self, 
        problem_type: str, 
        difficulty: Optional[str] = None
    ) -> List[ProblemTemplate]:
        """Get templates matching the specified type and optional difficulty.
        
        Args:
            problem_type: Type of problem to filter by (e.g., 'integer', 'fraction')
            difficulty: Optional difficulty level to filter by
            
        Returns:
            List of matching problem templates
        """
        problem_type = problem_type.lower()
        
        filtered = []
        for template in self.templates:
            # Check if the template's type contains the problem_type (case-insensitive)
            if problem_type in template['type'].lower():
                if not difficulty or template['difficulty'].lower() == difficulty.lower():
                    filtered.append(template)
        
        return filtered
    
    def get_random_template(
        self, 
        problem_type: str, 
        difficulty: Optional[str] = None,
        avoid_used: bool = True
    ) -> Optional[ProblemTemplate]:
        """Get a random template matching the criteria.
        
        Args:
            problem_type: Type of problem to filter by
            difficulty: Optional difficulty level to filter by
            avoid_used: If True, avoid templates that have been used before
            
        Returns:
            A random problem template or None if none found
        """
        candidates = self.get_templates_by_type_and_difficulty(problem_type, difficulty)
        
        if not candidates:
            # If no templates found with difficulty, try any difficulty
            if difficulty is not None:
                candidates = self.get_templates_by_type_and_difficulty(problem_type)
            
            if not candidates:
                return None
        
        # Filter out used templates if needed
        if avoid_used:
            unused = [t for t in candidates if t['id'] not in self.used_template_ids]
            if unused:  # Only use unused templates if available
                candidates = unused
        
        # Select a random template and mark it as used
        template = random.choice(candidates)
        self.used_template_ids.add(template['id'])
        return template
    
    def get_prompt_for_variation(
        self, 
        template: ProblemTemplate,
        num_variations: int = 1
    ) -> str:
        """Generate a prompt for creating variations of a problem.
        
        Args:
            template: The problem template to generate variations for
            num_variations: Number of variations to generate
            
        Returns:
            A formatted prompt for the LLM
        """
        prompt = f"""You are a math teacher creating variations of problems for 7th grade students.

Original Problem (Type: {template['type']}, Difficulty: {template['difficulty'].title()}):
{template['original_question']}

Your task is to create {num_variations} new variations of this problem that:
1. Have the same core mathematical concept and structure
2. Use different numbers and contexts
3. Are appropriate for {template['difficulty']} difficulty
4. Are clear, complete, and end with a question mark
5. Are suitable for 7th grade students following the CBSE curriculum

For each variation, provide:
- A completely new version of the problem
- Different numbers and context while maintaining the same mathematical structure
- A clear question that ends with a question mark

Format your response as a JSON array of problem strings.

Example variations:"""

        # Add examples if available
        if template['variations']:
            for i, var in enumerate(template['variations'][:2], 1):
                prompt += f"\n\nVariation {i}:\n{var['text']}"
        
        prompt += "\n\nYour new variations:"
        return prompt
    
    def reset_usage_tracking(self) -> None:
        """Reset the tracking of used templates."""
        self.used_template_ids.clear()


def test_template_manager():
    """Test the template manager."""
    print("Testing ProblemTemplateManager...")
    
    # Create a temporary directory with test templates
    import tempfile
    import shutil
    
    test_dir = Path(tempfile.mkdtemp())
    try:
        # Create test templates
        test_templates = [
            {
                "id": "test1",
                "type": "integer",
                "category": "Number System",
                "difficulty": "easy",
                "original_question": "What is 5 + 3?",
                "variations": [
                    {"text": "If you have 5 apples and get 3 more, how many do you have?", 
                     "explanation": "Simple addition word problem"}
                ]
            },
            {
                "id": "test2",
                "type": "fraction",
                "category": "Number System",
                "difficulty": "medium",
                "original_question": "What is 1/2 + 1/4?",
                "variations": []
            }
        ]
        
        # Save test templates
        for i, template in enumerate(test_templates, 1):
            with open(test_dir / f"test{i}.json", 'w') as f:
                json.dump(template, f, indent=2)
        
        # Test the manager
        manager = ProblemTemplateManager(test_dir)
        
        # Test loading
        assert len(manager.templates) == 2, f"Expected 2 templates, got {len(manager.templates)}"
        
        # Test filtering
        int_templates = manager.get_templates_by_type_and_difficulty("integer")
        assert len(int_templates) == 1, f"Expected 1 integer template, got {len(int_templates)}"
        
        # Test random template selection
        template = manager.get_random_template("integer")
        assert template is not None, "Failed to get random integer template"
        assert template['type'].lower() == 'integer', "Incorrect template type"
        
        print("All tests passed!")
        
    finally:
        # Clean up
        shutil.rmtree(test_dir)


if __name__ == "__main__":
    test_template_manager()
