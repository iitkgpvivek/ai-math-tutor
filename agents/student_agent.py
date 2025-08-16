"""
Student Agent for the AI Math Tutor system.

This module implements the StudentAgent class that validates math problems,
provides feedback, and participates in the iterative review process with the TeacherAgent.
"""

import asyncio
import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import logging

from .base_agent import Agent, AgentRole, Message


class ValidationResult(Enum):
    """Possible validation results for a math problem."""
    VALID = "valid"
    TOO_EASY = "too_easy"
    TOO_HARD = "too_hard"
    AMBIGUOUS = "ambiguous"
    INCOMPLETE = "incomplete"
    INVALID_FORMAT = "invalid_format"


@dataclass
class ProblemReview:
    """Represents a review of a math problem."""
    problem_text: str
    solution: str
    feedback: str
    is_valid: bool
    validation_result: ValidationResult
    iteration: int
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the review to a dictionary."""
        return {
            "problem_text": self.problem_text,
            "solution": self.solution,
            "feedback": self.feedback,
            "is_valid": self.is_valid,
            "validation_result": self.validation_result.value,
            "iteration": self.iteration,
            "timestamp": self.timestamp
        }


class StudentAgent(Agent):
    """
    An agent that validates math problems and provides feedback.
    
    The StudentAgent is responsible for:
    1. Validating if math problems are grade-appropriate
    2. Providing constructive feedback on problems
    3. Participating in the iterative review process
    4. Managing time limits for reviews
    """
    
    def __init__(
        self,
        grade_level: int,
        max_iterations: int = 3,
        iteration_timeout: float = 30.0,
        total_timeout: float = 120.0,
        **kwargs
    ):
        """
        Initialize the StudentAgent.
        
        Args:
            grade_level: The grade level of the student (used for validation)
            max_iterations: Maximum number of review iterations (default: 3)
            iteration_timeout: Timeout per iteration in seconds (default: 30s)
            total_timeout: Total timeout for the entire review in seconds (default: 120s)
            **kwargs: Additional arguments passed to the base Agent class
        """
        super().__init__(
            agent_id=f"student_grade_{grade_level}",
            role=AgentRole.STUDENT,
            **kwargs
        )
        
        self.grade_level = grade_level
        self.max_iterations = max_iterations
        self.iteration_timeout = iteration_timeout
        self.total_timeout = total_timeout
        self.reviews: Dict[str, List[ProblemReview]] = {}
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initialized StudentAgent for grade %d", grade_level)
    
    async def validate_problem(
        self,
        problem_text: str,
        solution: str,
        problem_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate if a math problem is appropriate for the student's grade level.
        
        Args:
            problem_text: The math problem text to validate
            solution: The proposed solution to the problem
            problem_id: Optional unique identifier for the problem
            
        Returns:
            Dict containing validation results and feedback
        """
        problem_id = problem_id or str(hash(problem_text))
        self.logger.debug("Validating problem: %s", problem_text[:50] + "...")
        
        # Check if we've reviewed this problem before
        if problem_id in self.reviews:
            last_review = self.reviews[problem_id][-1]
            return {
                "is_valid": last_review.is_valid,
                "validation_result": last_review.validation_result.value,
                "feedback": last_review.feedback,
                "iteration": last_review.iteration,
                "timestamp": last_review.timestamp
            }
        
        # Start a new review
        self.reviews[problem_id] = []
        return await self._start_review(problem_text, solution, problem_id)
    
    async def _start_review(
        self,
        problem_text: str,
        solution: str,
        problem_id: str,
        iteration: int = 0
    ) -> Dict[str, Any]:
        """
        Start or continue a review iteration.
        
        Args:
            problem_text: The math problem text
            solution: The proposed solution
            problem_id: Unique identifier for the problem
            iteration: Current iteration number (0-based)
            
        Returns:
            Dict containing review results
        """
        if iteration >= self.max_iterations:
            return self._finalize_review(
                problem_id,
                is_valid=False,
                result=ValidationResult.TOO_HARD,
                feedback="Maximum number of iterations reached"
            )
        
        try:
            # Validate the problem
            is_valid, result, feedback = await asyncio.wait_for(
                self._validate_problem(problem_text, solution, iteration),
                timeout=self.iteration_timeout
            )
            
            # Record the review
            review = ProblemReview(
                problem_text=problem_text,
                solution=solution,
                feedback=feedback,
                is_valid=is_valid,
                validation_result=result,
                iteration=iteration
            )
            self.reviews[problem_id].append(review)
            
            return {
                "is_valid": is_valid,
                "validation_result": result.value,
                "feedback": feedback,
                "iteration": iteration,
                "timestamp": review.timestamp
            }
            
        except asyncio.TimeoutError:
            return self._handle_timeout(problem_id, problem_text, solution, iteration)
    
    async def _validate_problem(
        self,
        problem_text: str,
        solution: str,
        iteration: int
    ) -> Tuple[bool, ValidationResult, str]:
        """
        Validate a math problem and its solution.
        
        Args:
            problem_text: The math problem text
            solution: The solution to the problem
            iteration: Current iteration number (1-based)
            
        Returns:
            Tuple of (is_valid, validation_result, feedback)
        """
        # Basic validation checks
        if not problem_text.strip() or not solution.strip():
            return False, ValidationResult.INCOMPLETE, "Problem or solution is empty"
            
        if len(solution.split()) < 3:  # Very basic check
            return False, ValidationResult.POOR_SOLUTION, "Solution is too brief"
        
        # Check grade appropriateness
        is_appropriate, grade_feedback = await self._check_grade_appropriateness(problem_text)
        if not is_appropriate:
            return False, ValidationResult.TOO_HARD if "too complex" in grade_feedback.lower() else ValidationResult.INVALID_FORMAT, grade_feedback
            
        # Check math correctness
        is_math_correct, math_feedback = await self._validate_math_correctness(problem_text, solution)
        if not is_math_correct:
            return False, ValidationResult.INCORRECT, math_feedback
            
        # Check explanation quality
        explanation_ok, explanation_feedback = await self._check_explanation_quality(solution)
        if not explanation_ok:
            return False, ValidationResult.POOR_EXPLANATION, explanation_feedback
            
        return True, ValidationResult.VALID, "Problem is valid"
    
    async def _validate_math_correctness(self, problem: str, solution: str) -> Tuple[bool, str]:
        """
        Use AI to validate that the solution correctly solves the problem.
        
        Args:
            problem: The math problem text
            solution: The proposed solution
            
        Returns:
            Tuple of (is_correct, feedback)
        """
        prompt = f"""
        Verify if this solution correctly solves the math problem.
        
        Problem: {problem}
        Solution: {solution}
        
        Check for:
        1. Correct application of mathematical principles
        2. Logical flow and reasoning
        3. Correct final answer
        4. No calculation errors
        
        Respond with a JSON object containing:
        - is_correct (boolean): Whether the solution is mathematically correct
        - feedback (string): Detailed explanation
        - correct_answer (string): The correct answer (if solution is wrong)
        - suggestions (list): Specific improvement suggestions
        """
        
        try:
            # Use the base agent's LLM integration
            response = await self.generate_response(
                prompt=prompt,
                system_prompt="You are a math expert that validates solutions to math problems.",
                max_tokens=500
            )
            
            # Parse the response
            try:
                result = json.loads(response)
                return result.get("is_correct", False), result.get("feedback", "No validation feedback")
            except json.JSONDecodeError:
                return False, "Could not validate solution: Invalid response format"
                
        except Exception as e:
            self.logger.error(f"Error in math validation: {str(e)}")
            return False, f"Error validating solution: {str(e)}"
        
    async def _check_grade_appropriateness(self, problem_text: str) -> Tuple[bool, str]:
        """
        Check if the problem is appropriate for the student's grade level.
        
        Args:
            problem_text: The problem text to check
            
        Returns:
            Tuple of (is_appropriate, feedback)
        """
        # First do basic checks
        problem_lower = problem_text.lower()
        
        # Check for advanced concepts in lower grades
        if self.grade_level < 8:
            advanced_topics = ["quadratic", "polynomial", "trigonometry", "calculus", "theorem", "algebra"]
            if any(topic in problem_lower for topic in advanced_topics):
                return False, f"Problem contains concepts too advanced for grade {self.grade_level}."
                
        # Check for too simple problems in higher grades
        if self.grade_level > 7:
            simple_indicators = ["what is 1+1", "basic addition", "counting"]
            if any(indicator in problem_lower for indicator in simple_indicators):
                return False, "Problem is too basic for this grade level."
        
        # Use AI for more nuanced evaluation
        prompt = f"""
        Evaluate if this math problem is appropriate for a {self.grade_level}th grade student.
        
        Problem: {problem_text}
        
        Consider:
        1. Mathematical concepts and their typical grade level
        2. Complexity of calculations
        3. Reading level and vocabulary
        4. Prior knowledge required
        
        Respond with a JSON object containing:
        - is_appropriate (boolean): If the problem is suitable for this grade
        - feedback (string): Detailed reasoning
        - difficulty (string): "too_easy", "appropriate", or "too_difficult"
        - suggestions (list): How to adjust difficulty if needed
        """
        
        try:
            # Use the base agent's LLM integration
            response = await self.generate_response(
                prompt=prompt,
                system_prompt="You are an expert in math curriculum development and grade-level appropriateness.",
                max_tokens=400
            )
            
            # Parse the response
            try:
                result = json.loads(response)
                return result.get("is_appropriate", False), result.get("feedback", "No feedback on grade level")
            except json.JSONDecodeError:
                self.logger.warning("Received invalid JSON from LLM in grade check")
                return True, "Grade level check inconclusive - proceeding with caution"
                
        except Exception as e:
            self.logger.error(f"Error in grade level check: {str(e)}")
            return True, f"Error checking grade level: {str(e)} - proceeding with caution"
    
    async def _check_explanation_quality(self, solution: str) -> Tuple[bool, str]:
        """
        Use AI to evaluate the quality of the solution explanation.
        
        Args:
            solution: The solution explanation to evaluate
            
        Returns:
            Tuple of (is_quality, feedback)
        """
        prompt = f"""
        Evaluate this math solution explanation for a {self.grade_level}th grade student.
        Check for:
        1. Clear step-by-step reasoning
        2. Correct mathematical operations
        3. Age-appropriate language
        4. Complete solution
        
        Solution: {solution}
        
        Respond with a JSON object containing:
        - is_quality (boolean): Whether the explanation meets quality standards
        - feedback (string): Detailed feedback
        - missing_elements (list): Any missing components
        - suggested_improvements (list): Specific suggestions
        """
        
        try:
            # Use the base agent's LLM integration
            response = await self.generate_response(
                prompt=prompt,
                system_prompt="You are a math education expert evaluating solution explanations.",
                max_tokens=500
            )
            
            # Parse the response
            try:
                result = json.loads(response)
                return result.get("is_quality", False), result.get("feedback", "No feedback provided")
            except json.JSONDecodeError:
                # Fallback if response isn't valid JSON
                return False, "Could not evaluate explanation quality: Invalid response format"
                
        except Exception as e:
            self.logger.error(f"Error in explanation validation: {str(e)}")
            return False, f"Error evaluating explanation: {str(e)}"
    
    def _handle_timeout(
        self,
        problem_id: str,
        problem_text: str,
        solution: str,
        iteration: int
    ) -> Dict[str, Any]:
        """Handle timeout during problem validation."""
        self.logger.warning(
            "Timeout during validation of problem: %s", 
            problem_id
        )
        
        # Record the timeout as a review
        review = ProblemReview(
            problem_text=problem_text,
            solution=solution,
            feedback="Validation timed out",
            is_valid=False,
            validation_result=ValidationResult.INVALID_FORMAT,
            iteration=iteration
        )
        
        if problem_id in self.reviews:
            self.reviews[problem_id].append(review)
        else:
            self.reviews[problem_id] = [review]
        
        return {
            "is_valid": False,
            "validation_result": ValidationResult.INVALID_FORMAT.value,
            "feedback": "Validation timed out. Please try again with a different problem.",
            "iteration": iteration,
            "timestamp": review.timestamp
        }
    
    def _finalize_review(
        self,
        problem_id: str,
        is_valid: bool,
        result: ValidationResult,
        feedback: str
    ) -> Dict[str, Any]:
        """Finalize a review with the given result."""
        review = ProblemReview(
            problem_text="",  # Will be filled by the caller
            solution="",      # Will be filled by the caller
            feedback=feedback,
            is_valid=is_valid,
            validation_result=result,
            iteration=self.max_iterations - 1
        )
        
        if problem_id in self.reviews and self.reviews[problem_id]:
            # Copy problem text and solution from the last review
            last_review = self.reviews[problem_id][-1]
            review.problem_text = last_review.problem_text
            review.solution = last_review.solution
            
        self.reviews[problem_id].append(review)
        
        return {
            "is_valid": is_valid,
            "validation_result": result.value,
            "feedback": feedback,
            "iteration": self.max_iterations - 1,
            "timestamp": review.timestamp
        }
    
    def get_review_history(self, problem_id: str) -> List[Dict[str, Any]]:
        """Get the review history for a specific problem."""
        if problem_id not in self.reviews:
            return []
        
        return [
            {
                "problem_text": r.problem_text,
                "solution": r.solution,
                "feedback": r.feedback,
                "is_valid": r.is_valid,
                "validation_result": r.validation_result.value,
                "iteration": r.iteration,
                "timestamp": r.timestamp
            }
            for r in self.reviews[problem_id]
        ]
    
    def clear_reviews(self) -> None:
        """Clear all review history."""
        self.reviews.clear()
        self.logger.info("Cleared all review history")
        
    async def generate_solution(self, problem_text: str) -> Dict[str, str]:
        """
        Generate a step-by-step solution for a math problem.
        
        Args:
            problem_text: The math problem to solve
            
        Returns:
            Dict containing 'steps' (list of solution steps), 'final_answer', and 'explanation'
        """
        # TODO: Implement actual solution generation using LLM
        # For now, return a placeholder solution
        return {
            'steps': [
                'Read and understand the problem',
                'Identify what is being asked',
                'Determine the appropriate mathematical operations',
                'Perform calculations step by step',
                'Verify the solution',
                'Present the final answer clearly'
            ],
            'final_answer': 'The final answer will be calculated based on the problem.',
            'explanation': 'This is a placeholder for a detailed explanation that would be generated by the LLM, written in a way that is understandable to a 7th grader.'
        }


# Example usage
async def example():
    """Example usage of the StudentAgent."""
    student = StudentAgent(grade_level=5)
    
    problem = "What is 2 + 2?"
    solution = "The answer is 4."
    
    result = await student.validate_problem(problem, solution)
    print(f"Validation result: {result}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(example())