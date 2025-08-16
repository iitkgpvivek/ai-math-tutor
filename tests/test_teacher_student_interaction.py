"""
Test script for TeacherAgent and StudentAgent interaction.

This script demonstrates how to use the TeacherAgent to generate problem variations
and validate them using the StudentAgent.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from agents
sys.path.append(str(Path(__file__).parent.parent))

from agents import StudentAgent, TeacherAgent

async def test_teacher_student_interaction():
    """Test the interaction between TeacherAgent and StudentAgent."""
    # Create a student agent for 7th grade
    print("Creating StudentAgent for 7th grade...")
    student = StudentAgent(grade_level=7)
    
    # Create a teacher agent with the student agent
    print("Creating TeacherAgent...")
    teacher = TeacherAgent(student_agent=student)
    
    # Example original questions
    original_questions = [
        "If John has 5 apples and gives 2 to Mary, how many apples does he have left?",
        "A rectangle has a length of 8 units and width of 3 units. What is its area?",
        "What is 3/4 of 20?"
    ]
    
    # Test each question
    for i, question in enumerate(original_questions, 1):
        print(f"\n--- Testing Question {i} ---")
        print(f"Original: {question}")
        
        # Generate a variation
        print("\nGenerating problem variation...")
        problem = await teacher.generate_problem_variation(question)
        
        if problem:
            print(f"\n✅ Generated Problem: {problem.variation}")
            print(f"   Solution: {problem.solution}")
            print(f"   Status: {problem.status.upper()}")
            
            # Show review history
            if problem.reviews:
                print("\nReview History:")
                for j, review in enumerate(problem.reviews, 1):
                    print(f"  {j}. {'✅' if review.is_valid else '❌'} {review.validation_result.value}")
                    print(f"     Feedback: {review.feedback}")
        else:
            print("\n❌ Failed to generate a valid problem variation")
    
    # Save approved problems
    output_dir = "data/approved_problems"
    os.makedirs(output_dir, exist_ok=True)
    teacher.save_problems(output_dir)
    print(f"\nSaved approved problems to {output_dir}/")
    
    # Show summary
    print("\n--- Summary ---")
    print(f"Approved problems: {len(teacher.approved_problems)}")
    print(f"Rejected problems: {len(teacher.rejected_problems)}")

if __name__ == "__main__":
    asyncio.run(test_teacher_student_interaction())
