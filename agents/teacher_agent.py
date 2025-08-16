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
from .student_agent import StudentAgent, ValidationResult, ProblemReview


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
        elif not review.is_valid and not review.validation_result == ValidationResult.TOO_EASY:
            # Reject immediately if the problem is invalid for reasons other than being too easy
            self.status = "rejected"
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
        original_question: Optional[str] = None,
        template_id: Optional[str] = None,
        max_retries: int = 3
    ) -> Optional[ProblemVariation]:
        """
        Generate a variation of a math problem from templates or a direct question.

        Args:
            original_question: Optional text of a question to use as a template.
            template_id: Optional ID of a specific template to use.
            max_retries: Maximum number of generation attempts.

        Returns:
            A ProblemVariation object if successful, None otherwise.
        """
        template = None
        if original_question:
            # Use the provided question text as a one-off template
            template = {"original_question": original_question}
        elif template_id:
            # Find a template by its ID
            template = next((t for t in self.problem_templates if t.get('id') == template_id), None)
            if not template:
                self.logger.warning(f"Template {template_id} not found")
                return None
        elif self.problem_templates:
            # Pick a random template if none is specified
            template = random.choice(self.problem_templates)

        if not template:
            self.logger.error("No problem templates or original question provided.")
            return None
            
        # Generate a variation using the template
        variation = await self._generate_llm_variation(template)
        
        if not variation:
            self.logger.error("Failed to generate problem variation from LLM")
            return None
            
        problem = ProblemVariation(
            original_question=template['original_question'],
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
            
        return problem
        
    async def _generate_llm_variation(self, template: Dict[str, Any]) -> Optional[Dict[str, str]]:
        """Generate a problem variation using LLM based on a template."""
        prompt = f"""You are an expert math teacher creating variations of problems for 7th grade Indian students following the CBSE curriculum.

=== ORIGINAL PROBLEM ===
{template['original_question']}

=== TASK ===
Your task is to create a new problem that is a variation of the original, preserving its exact algebraic structure.

=== CRITICAL INSTRUCTIONS ===
1.  **Analyze the Original Problem**: First, write down the exact algebraic equation that represents the original problem. For example, if the problem is "The sum of a number and 5 is 12", the algebraic structure is `x + 5 = 12`.
2.  **Create a Variation**: Create a new word problem or direct question that resolves to the *exact same algebraic structure*, just with different numbers and a different context. The complexity must be identical.
3.  **Maintain Stylistic Similarity**: The variation should be stylistically similar to the original. If the original is a direct question, the variation should also be a direct question. If it's a word problem, the new version must also be a word problem.
4.  **Use Clear and Unambiguous Language**: The problem must be stated clearly. Avoid vague phrases like "X is two times less than Y". Instead, use precise statements like "Y is twice X" (Y = 2X) or "X is half of Y" (X = Y/2).
5.  **Ensure Integer Solutions**: For problems involving discrete items (like coins, people, or objects), the numbers you choose for the variation MUST result in a whole number (integer) answer. Double-check your calculations.
6.  **Maintain Numerical Complexity**: If the original problem uses fractions, decimals, or mixed numbers, the variation MUST also use numbers of similar complexity. Do not oversimplify the problem by replacing complex numbers with basic integers.

=== EXAMPLE ===
- **Original Problem**: "If one-fourth, half and one-third of a number are added to the number itself, then the result is equal to 25. Find the number."
- **Analysis**: The algebraic structure is `(1/4)x + (1/2)x + (1/3)x + x = 25`.
- **Good Variation**: "A piece of land is divided into three parts. One-fifth of the land is given to a school, one-fourth is a park, and one-half is for a community hall. The remaining 50 acres are for residential use. What is the total area of the land?"
- **Explanation**: The variation's structure is `(1/5)x + (1/4)x + (1/2)x + 50 = x`, which has the same structural complexity as the original.

=== REQUIRED JSON FORMAT ===
You MUST respond with a valid JSON object containing exactly these two fields:
- "problem": The new problem text (ending with a question mark)
- "solution": A detailed, step-by-step solution for the new problem.

Example:
{{
  "problem": "If a train travels 300 km in 5 hours, what is its speed in km/h?",
  "solution": "Step 1: Formula for speed is distance/time. Step 2: Speed = 300 km / 5 hours. Step 3: Speed = 60 km/h."
}}

RULES:
1. The response MUST be valid JSON.
2. The 'problem' MUST end with a question mark (?).
3. The 'problem' MUST be a complete, self-contained question.
4. The 'solution' MUST be detailed and step-by-step.

Your response (ONLY the JSON object, no other text):
"""

        try:
            # Use the base class method to generate a response
            response = await self.generate_with_llm(
                prompt=prompt,
                system_prompt="You are an expert math teacher creating problem variations. Always respond with valid JSON.",
                temperature=0.7,
                json_mode=True
            )

            # Get the response content
            content = response.get("content", "")
            if not content:
                self.logger.error("Empty response from LLM")
                return None

            # Clean and parse the JSON response
            try:
                # Remove any markdown code block markers if present
                content = content.strip().strip('```json').strip('```').strip()
                result = json.loads(content)
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse LLM response as JSON: {e}\nContent: {content}")
                return None

            # Validate the response
            if 'problem' not in result or 'solution' not in result:
                self.logger.error(f"Invalid response format from LLM: {content}")
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
        
        The validation process works as follows:
        1. First attempt: Generate and validate initial variation with minimal constraints
        2. If validation fails, use feedback to revise the problem
        3. Continue for max_iterations or until problem is validated
        
        Args:
            problem: The problem variation to validate
            max_iterations: Maximum number of review iterations
            iteration_timeout: Timeout per iteration in seconds
            total_timeout: Total timeout for the entire review in seconds
            
        Returns:
            Dict containing validation results and final problem state
        """
        start_time = time.time()
        iteration = 0
        
        while iteration < max_iterations and (time.time() - start_time) < total_timeout:
            try:
                # Get student's review
                review_result = await asyncio.wait_for(
                    self.student_agent.validate_problem(
                        problem_text=problem.variation,
                        solution=problem.solution,
                        problem_id=problem.problem_id,
                        original_question=problem.original_question
                    ),
                    timeout=iteration_timeout
                )
                
                # Create review object
                review = ProblemReview(
                    problem_text=problem.variation,
                    solution=problem.solution,
                    feedback=review_result.get('feedback', 'No feedback provided'),
                    is_valid=review_result.get('is_valid', False),
                    validation_result=ValidationResult(review_result.get('validation_result', 'invalid_format')),
                    iteration=iteration
                )
                problem.add_review(review)
                
                # If problem is valid, return success
                if review_result.get('is_valid', False):
                    return {
                        "is_valid": True,
                        "feedback": "Problem validated successfully!",
                        "iterations": iteration + 1,
                        "reviews": [r.to_dict() for r in problem.reviews]
                    }
                
                # If we have more iterations left, try to revise the problem
                if iteration < max_iterations - 1:
                    revision_successful = await self._revise_problem(
                        problem=problem,
                        feedback=review.feedback
                    )
                    
                    if not revision_successful:
                        return {
                            "is_valid": False,
                            "feedback": "Failed to revise problem based on feedback",
                            "iterations": iteration + 1,
                            "reviews": [r.to_dict() for r in problem.reviews]
                        }
                    self.logger.info("Problem revised. Re-validating...")
                else:
                    # If status is not 'needs_revision' (e.g., rejected), stop.
                    return {
                        "is_valid": False,
                        "feedback": "Problem rejected after review.",
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
        prompt = f"""You are an expert math teacher revising a math problem based on feedback.

=== ORIGINAL PROBLEM ===
{problem.original_question}

=== CURRENT VARIATION (WITH ISSUES) ===
Problem: {problem.variation}
Solution: {problem.solution}

=== FEEDBACK ===
{feedback}

=== TASK ===
Revise the problem and solution to address the feedback. The revised problem MUST follow these critical instructions:

=== CRITICAL INSTRUCTIONS ===
1.  **Analyze the Original Problem**: First, identify the core mathematical concept and the algebraic structure of the original problem. For example, does it resolve to a simple linear equation like `ax + b = c`?
2.  **Create a Variation**: Create a new problem with different numbers (and a different context if it's a word problem), but which resolves to the *exact same algebraic structure*.
3.  **Maintain Stylistic Similarity**: The variation should be stylistically similar to the original. If the original is a direct question (e.g., "Solve for x..."), the variation should also be a direct question. If the original is a word problem, the variation should be a word problem.

=== REQUIRED JSON FORMAT ===
You MUST respond with a valid JSON object containing exactly these two fields:
- "problem": The revised problem text (ending with a question mark)
- "solution": A detailed, step-by-step solution for the revised problem.

Your response (ONLY the JSON object, no other text):
"""

        try:
            response = await self.generate_with_llm(
                prompt=prompt,
                system_prompt="You are an expert math teacher revising problems. Always respond with valid JSON.",
                temperature=0.6,
                json_mode=True
            )

            content = response.get("content", "")
            if not content:
                self.logger.error("Empty revision response from LLM")
                return False

            content = content.strip().strip('```json').strip('```').strip()
            result = json.loads(content)

            if 'problem' in result and 'solution' in result:
                problem_content = result['problem']
                solution_content = result['solution']

                if isinstance(problem_content, dict):
                    problem.variation = json.dumps(problem_content)
                else:
                    problem.variation = str(problem_content).strip()

                if isinstance(solution_content, dict):
                    problem.solution = json.dumps(solution_content)
                else:
                    problem.solution = str(solution_content).strip()
                    
                return True
            else:
                self.logger.error(f"Invalid revision format from LLM: {content}")
                return False

        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse LLM revision as JSON: {e}\nContent: {content}")
            return False
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
        required_fields = ['id', 'original_question']
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


