"""
Teacher Agent for the AI Math Tutor system.

This module implements the TeacherAgent class that generates math problems,
processes feedback from StudentAgent, and manages the iterative review process.
"""

import asyncio
import time
import random
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import logging
import os
import json

from .base_agent import Agent, AgentRole, Message
from .student_agent import ValidationResult, ProblemReview


class ProblemVariation:
    """Represents a variation of a math problem."""
    
    def __init__(
        self,
        original_question: str,
        variation: str,
        solution: str,
        problem_id: Optional[str] = None
    ):
        self.original_question = original_question
        self.variation = variation
        self.solution = solution
        self.problem_id = problem_id or f"prob_{int(time.time())}_{random.randint(1000, 9999)}"
        self.reviews: List[ProblemReview] = []
        self.status: str = "pending"  # pending, approved, rejected, needs_revision
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert the problem variation to a dictionary."""
        return {
            "problem_id": self.problem_id,
            "original_question": self.original_question,
            "variation": self.variation,
            "solution": self.solution,
            "status": self.status,
            "reviews": [
                {
                    "feedback": review.feedback,
                    "is_valid": review.is_valid,
                    "validation_result": review.validation_result.value,
                    "iteration": review.iteration,
                    "timestamp": review.timestamp
                }
                for review in self.reviews
            ]
        }
        
    def add_review(self, review: ProblemReview):
        """Add a review to this problem variation."""
        self.reviews.append(review)
        if review.is_valid:
            self.status = "approved"
        elif len(self.reviews) >= 3:  # Max iterations
            self.status = "rejected"
        else:
            self.status = "needs_revision"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary for serialization."""
        return {
            "problem_id": self.problem_id,
            "original_question": self.original_question,
            "variation": self.variation,
            "solution": self.solution,
            "status": self.status,
            "reviews": [
                {
                    "feedback": r.feedback,
                    "is_valid": r.is_valid,
                    "validation_result": r.validation_result.value,
                    "iteration": r.iteration,
                    "timestamp": r.timestamp
                }
                for r in self.reviews
            ]
        }


class TeacherAgent(Agent):
    """
    An agent that generates math problems and processes feedback from StudentAgent.
    
    The TeacherAgent is responsible for:
    1. Generating variations of math problems
    2. Managing the iterative review process with StudentAgent
    3. Maintaining a collection of approved problems
    4. Ensuring problems meet quality standards
    """
    
    def __init__(
        self,
        student_agent: 'StudentAgent',
        problems_dir: str = "data/problems",
        **kwargs
    ):
        """
        Initialize the TeacherAgent.
        
        Args:
            student_agent: The StudentAgent instance to validate problems
            problems_dir: Directory containing original problems
            **kwargs: Additional arguments passed to the base Agent class
        """
        super().__init__(
            agent_id="teacher_agent",
            role=AgentRole.TUTOR,
            **kwargs
        )
        
        self.student_agent = student_agent
        self.problems_dir = problems_dir
        self.problem_templates: List[Dict[str, Any]] = []
        self.variations: Dict[str, ProblemVariation] = {}
        self.approved_problems: List[ProblemVariation] = []
        self.rejected_problems: List[ProblemVariation] = []
        
        # Load problem templates
        self._load_problem_templates()
        
        # Load existing variations if any
        self._load_variations()
    
    async def generate_problem_variation(
        self,
        template_id: Optional[str] = None,
        max_retries: int = 3
    ) -> Optional[ProblemVariation]:
        """
        Generate a variation of a math problem from templates.
        
        Args:
            template_id: Optional ID of a specific template to use
            max_retries: Maximum number of generation attempts
            
        Returns:
            A ProblemVariation object if successful, None otherwise
        """
        # Get a template (random or specific)
        template = None
        if template_id:
            template = next((t for t in self.problem_templates if t.get('id') == template_id), None)
            if not template:
                self.logger.warning(f"Template {template_id} not found")
                return None
        
        if not template and self.problem_templates:
            template = random.choice(self.problem_templates)
        
        if not template:
            self.logger.error("No problem templates available")
            return None
            
        # Generate a variation using the template
        variation = await self._generate_llm_variation(template)
        
        if not variation:
            self.logger.error("Failed to generate problem variation")
            return None
            
        problem = ProblemVariation(
            original_question=template['problem'],
            variation=variation['problem'],
            solution=variation['solution']
        )
        
        # Validate the problem with the student agent
        result = await self._validate_problem(problem)
        
        if result["is_valid"]:
            self.approved_problems.append(problem)
            self.variations[problem.problem_id] = problem
        else:
            self.rejected_problems.append(problem)
            
        return problem if result["is_valid"] else None
        
    async def _generate_llm_variation(self, template: Dict[str, Any]) -> Optional[Dict[str, str]]:
        """Generate a problem variation using LLM based on a template."""
        prompt = f"""
        Create a variation of the following math problem while maintaining the same structure and difficulty.
        
        Original Problem: {template['problem']}
        Original Solution: {template['solution']}
        
        Requirements:
        1. Change the numbers and context but keep the same mathematical structure
        2. Ensure the problem is clear and complete
        3. Include the solution with step-by-step working
        4. Make it culturally appropriate for Indian students
        5. Use metric units and Indian currency (₹)
        
        Respond in JSON format with 'problem' and 'solution' fields.
        """
        
        try:
            # Use the LLM to generate a variation
            response = await self.llm.generate(
                prompt=prompt,
                system_prompt="You are an expert math teacher creating problem variations.",
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            # Parse the response
            result = json.loads(response.choices[0].message.content)
            
            # Validate the response
            if 'problem' not in result or 'solution' not in result:
                self.logger.error("Invalid response format from LLM")
                return None
                
            return {
                'problem': result['problem'].strip(),
                'solution': result['solution'].strip()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating LLM variation: {e}")
            return None
    
    async def _validate_problem(
        self,
        problem: ProblemVariation,
        max_iterations: int = 3,
        iteration_timeout: float = 30.0,
        total_timeout: float = 120.0
    ) -> Dict[str, Any]:
        """
        Validate a problem with the StudentAgent through iterative review.
        
        Args:
            problem: The problem variation to validate
            max_iterations: Maximum number of review iterations
            iteration_timeout: Timeout per iteration in seconds
            total_timeout: Total timeout for the entire review in seconds
            
        Returns:
            Dict containing validation results
        """
        start_time = time.time()
        iteration = 0
        
        while iteration < max_iterations and (time.time() - start_time) < total_timeout:
            try:
                # Validate with student agent
                result = await asyncio.wait_for(
                    self.student_agent.validate_problem(
                        problem.variation,
                        problem.solution,
                        problem.problem_id
                    ),
                    timeout=min(iteration_timeout, total_timeout - (time.time() - start_time))
                )
                
                # Create review object
                review = ProblemReview(
                    problem_text=problem.variation,
                    solution=problem.solution,
                    feedback=result["feedback"],
                    is_valid=result["is_valid"],
                    validation_result=ValidationResult(result["validation_result"]),
                    iteration=iteration
                )
                
                problem.add_review(review)
                
                if result["is_valid"]:
                    return {
                        "is_valid": True,
                        "feedback": "Problem validated successfully",
                        "iterations": iteration + 1,
                        "reviews": [r.to_dict() for r in problem.reviews]
                    }
                
                # If we need to revise, update the problem
                if problem.status == "needs_revision":
                    revised = await self._revise_problem(problem, result["feedback"])
                    if not revised:
                        return {
                            "is_valid": False,
                            "feedback": "Failed to revise problem",
                            "iterations": iteration + 1,
                            "reviews": [r.to_dict() for r in problem.reviews]
                        }
                
                iteration += 1
                
            except asyncio.TimeoutError:
                return {
                    "is_valid": False,
                    "feedback": "Validation timed out",
                    "iterations": iteration,
                    "reviews": [r.to_dict() for r in problem.reviews]
                }
        
        return {
            "is_valid": False,
            "feedback": "Maximum iterations or time limit reached",
            "iterations": iteration,
            "reviews": [r.to_dict() for r in problem.reviews]
        }
    
    async def _revise_problem(
        self,
        problem: ProblemVariation,
        feedback: str
    ) -> bool:
        """
        Revise a problem based on feedback using LLM.
        
        Args:
            problem: The problem to revise
            feedback: Feedback from the StudentAgent
            
        Returns:
            True if revision was successful, False otherwise
        """
        prompt = f"""
        Revise the following math problem based on the feedback.
        
        Original Problem: {problem.original_question}
        Current Variation: {problem.variation}
        Current Solution: {problem.solution}
        
        Feedback:
        {feedback}
        
        Please provide:
        1. A revised version of the problem that addresses the feedback
        2. An updated solution
        
        Respond in JSON format with 'revised_problem' and 'revised_solution' fields.
        """
        
        try:
            # Get revision from LLM
            response = await self.llm.generate(
                prompt=prompt,
                system_prompt="You are an expert math teacher revising problems based on feedback.",
                response_format={"type": "json_object"},
                temperature=0.5  # Lower temperature for more conservative revisions
            )
            
            # Parse and apply the revision
            result = json.loads(response.choices[0].message.content)
            
            if 'revised_problem' in result and 'revised_solution' in result:
                problem.variation = result['revised_problem'].strip()
                problem.solution = result['revised_solution'].strip()
                return True
                
        except Exception as e:
            self.logger.error(f"Error revising problem: {e}")
            
        return False
    
    def _load_problem_templates(self):
        """Load problem templates from the problems directory."""
        if not os.path.exists(self.problems_dir):
            self.logger.warning(f"Problem templates directory not found: {self.problems_dir}")
            return
            
        for filename in os.listdir(self.problems_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(self.problems_dir, filename), 'r') as f:
                        template = json.load(f)
                        if self._validate_template(template):
                            self.problem_templates.append(template)
                            self.logger.info(f"Loaded template: {template.get('id', 'unknown')}")
                        else:
                            self.logger.warning(f"Invalid template format in {filename}")
                except Exception as e:
                    self.logger.error(f"Error loading template from {filename}: {e}")
    
    def _load_variations(self):
        """Load existing problem variations."""
        variations_dir = os.path.join(os.path.dirname(self.problems_dir), 'variations')
        if not os.path.exists(variations_dir):
            return
            
        for filename in os.listdir(variations_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(variations_dir, filename), 'r') as f:
                        data = json.load(f)
                        variation = ProblemVariation(
                            original_question=data.get('original_question', ''),
                            variation=data.get('variation', ''),
                            solution=data.get('solution', ''),
                            problem_id=data.get('problem_id', f"var_{len(self.variations) + 1}")
                        )
                        self.variations[variation.problem_id] = variation
                except Exception as e:
                    self.logger.error(f"Error loading variation from {filename}: {e}")
    
    def _validate_template(self, template: Dict[str, Any]) -> bool:
        """Validate a problem template has all required fields."""
        required_fields = ['id', 'problem', 'type', 'difficulty', 'solution', 'variations']
        return all(field in template for field in required_fields)
    
    def save_problems(self, output_dir: Optional[str] = None):
        """Save approved problems to disk."""
        output_dir = output_dir or os.path.join(os.path.dirname(self.problems_dir), 'approved')
        os.makedirs(output_dir, exist_ok=True)
        
        for problem in self.approved_problems:
            try:
                filepath = os.path.join(output_dir, f"{problem.problem_id}.json")
                with open(filepath, 'w') as f:
                    json.dump(problem.to_dict(), f, indent=2)
                self.logger.info(f"Saved approved problem: {problem.problem_id}")
            except Exception as e:
                self.logger.error(f"Error saving problem {problem.problem_id}: {e}")
    
    def get_approved_problems(self) -> List[Dict[str, Any]]:
        """Get a list of all approved problems."""
        return [p.to_dict() for p in self.approved_problems]
    
    def get_rejected_problems(self) -> List[Dict[str, Any]]:
        """Get a list of all rejected problems."""
        return [p.to_dict() for p in self.rejected_problems]


# Example usage
async def example():
    """Example usage of the TeacherAgent with StudentAgent."""
    # Create a student agent
    student = StudentAgent(grade_level=7)
    
    # Create a teacher agent with the student agent
    teacher = TeacherAgent(student_agent=student)
    
    # Check if we have any problem templates
    if not teacher.problem_templates:
        print("No problem templates found. Please add some to the data/problems directory.")
        return
    
    print(f"Loaded {len(teacher.problem_templates)} problem templates")
    
    # Generate and validate a problem variation
    problem = await teacher.generate_problem_variation()
    
    if problem:
        print("\n✅ Generated problem:")
        print(f"Original: {problem.original_question}")
        print(f"Variation: {problem.variation}")
        print(f"Solution: {problem.solution}")
        print("Status: Approved")
        
        # Save approved problems
        teacher.save_problems()
        print("\nProblems saved successfully!")
    else:
        print("\n❌ Failed to generate a valid problem variation")


if __name__ == "__main__":
    import asyncio
    asyncio.run(example())
