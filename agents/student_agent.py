"""
Student Agent for the AI Math Tutor system.

This module implements the StudentAgent class that validates math problems,
provides feedback, and participates in the iterative review process with the TeacherAgent.
"""

import asyncio
import time
import json
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
        problem_id: Optional[str] = None,
        original_question: Optional[str] = None
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
        
        # If this is the first time seeing this problem, initialize its review history.
        if problem_id not in self.reviews:
            self.reviews[problem_id] = []
        
        # Determine the current iteration number from the review history.
        iteration = len(self.reviews.get(problem_id, []))

        # Start or continue the review for the current iteration.
        return await self._start_review(
            problem_text,
            solution,
            problem_id,
            iteration=iteration,
            original_question=original_question
        )
    
    async def _start_review(
        self,
        problem_text: str,
        solution: str,
        problem_id: str,
        iteration: int = 0,
        original_question: Optional[str] = None
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
                self._validate_problem(problem_text, solution, iteration, original_question),
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
        iteration: int,
        original_question: Optional[str] = None
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
            return False, ValidationResult.INCOMPLETE, "Problem is incomplete: problem or solution is empty"
            
        if len(solution.split()) < 3:  # Very basic check
            return False, ValidationResult.INCOMPLETE, "Solution is incomplete: explanation is too brief"
        
        # If the solution itself declares missing information, treat as incomplete.
        # This is solution-driven (not rule-based parsing of the problem) and ensures required keywords.
        sol_lower = solution.lower()
        if any(phrase in sol_lower for phrase in [
            'not provided', 'not given', 'cannot calculate', 'insufficient information',
            'not enough information', 'missing'
        ]):
            missing_items: List[str] = []
            text_combo = f"{problem_text.lower()}\n{sol_lower}"
            for term in ['radius', 'length', 'width', 'height', 'value', 'numbers', 'unit', 'data']:
                if term in text_combo:
                    missing_items.append(term)
            missing_str = ", ".join(sorted(set(missing_items))) if missing_items else "required information"
            return False, ValidationResult.INCOMPLETE, f"Problem is incomplete: missing {missing_str}. Please include the needed values."
        
        # Check grade appropriateness
        is_appropriate, appropriateness_feedback = await self._validate_grade_appropriateness(
            problem_text, original_question, iteration
        )
        if not is_appropriate:
            return False, ValidationResult.TOO_HARD if "too complex" in appropriateness_feedback.lower() else ValidationResult.INVALID_FORMAT, appropriateness_feedback
            
        # Check math correctness
        is_math_correct, math_feedback = await self._validate_math_correctness(problem_text, solution)
        if not is_math_correct:
            return False, ValidationResult.INVALID_FORMAT, math_feedback
        
        # Check explanation quality
        explanation_ok, explanation_feedback = await self._check_explanation_quality(solution)
        if not explanation_ok:
            return False, ValidationResult.INCOMPLETE, explanation_feedback
            
        return True, ValidationResult.VALID, "Problem is valid"
    
    async def _validate_grade_appropriateness(self, problem: str, original_question: Optional[str] = None, current_iteration: int = 0) -> Tuple[bool, str]:
        """
        Check if the problem is appropriate for the student's grade level and maintains
        the same mathematical structure as the original problem.
        
        This method uses AI-powered validation to assess the problem's appropriateness
        based on the student's grade level and the original problem's structure.
        
        Args:
            problem: The problem text to check
            original_question: The original question text for comparison
            
        Returns:
            Tuple of (is_appropriate, feedback)
        """
        # Basic validation - check for empty or invalid input
        if not problem or not problem.strip():
            return False, "Problem text cannot be empty"
        
        # Delegate all detailed checks (advanced concepts, completeness, clarity) to the LLM pathway
        return await self._get_detailed_feedback(problem, original_question, current_iteration)
    
    async def _get_detailed_feedback(self, problem: str, original_question: Optional[str] = None, iteration: int = 0) -> Tuple[bool, str]:
        """
        Get detailed feedback on whether a problem is appropriate for the student's grade level.
        
        Args:
            problem: The problem text to evaluate
            original_question: The original question (if this is a variation)
            iteration: The current iteration number for validation
            
        Returns:
            Tuple of (is_appropriate, feedback)
        """
        # Helper pre-check: detect clearly advanced topics to avoid unnecessary LLM calls
        # Note: kept minimal to avoid overfitting; the main judgment remains LLM-based.
        # This function is also used within this method, so it must exist.
        
        
        # First, check for advanced concepts using direct pattern matching
        has_advanced, reason = self._contains_advanced_math(problem)
        if has_advanced:
            # Log the advanced math detection for debugging
            self.logger.info(f"Advanced math detected in problem: {reason}")
            return False, reason
            
        # Also check the original question if provided
        if original_question and original_question != problem:
            has_advanced_in_original, original_reason = self._contains_advanced_math(original_question)
            if has_advanced_in_original:
                self.logger.info(f"Advanced math detected in original question: {original_reason}")
                return False, f"Original question contains advanced concepts: {original_reason}"
            
        # If no advanced concepts found, use AI for comprehensive evaluation
        prompt = f"""
        You are an experienced math teacher reviewing a problem for a {self.grade_level}th grade student.
        Your task is to determine if this problem is appropriate for a {self.grade_level}th grade level.
        
        PROBLEM TO REVIEW:
        {problem}
        
        INSTRUCTIONS:
        1. This is for a {self.grade_level}th grade student (CBSE curriculum).
        2. The problem MUST be appropriate for this grade level.
        3. Focus on the mathematical concepts and language complexity.
        4. If the problem is missing required information (e.g., values, definitions, units) or is ambiguous such that it cannot be solved as written, treat it as incomplete. In that case:
           - Set "is_appropriate": false
           - In "feedback", explicitly include the word "incomplete" and clearly name what is missing (e.g., "missing radius", "missing numbers", "missing unit").
           - Provide one or two concise suggestions to make it complete.
        
        GRADE {self.grade_level} CURRICULUM INCLUDES:
        - Basic arithmetic (addition, subtraction, multiplication, division)
        - Fractions, decimals, percentages
        - Basic algebra (simple equations, expressions)
        - Basic geometry (area, perimeter, angles of basic shapes)
        - Data handling (mean, median, mode, basic graphs)
        
        GRADE {self.grade_level} CURRICULUM DOES NOT INCLUDE:
        - Calculus (derivatives, integrals)
        - Trigonometry (sine, cosine, tangent, etc.)
        - Advanced algebra (matrices, complex numbers, etc.)
        - Advanced geometry (proofs, theorems)
        
        RESPOND WITH JSON:
        {{
            "is_appropriate": boolean,  # True only if appropriate for grade {self.grade_level}
            "feedback": string,  # Detailed explanation of your assessment
            "issues_found": [string],  # List any issues found (empty if none)
            "suggestions": [string]  # Suggestions for improvement (if any)
        }}
        """
        
        try:
            response = await self.generate_with_llm(
                prompt=prompt,
                system_prompt="""You are an expert math curriculum designer with deep knowledge of the 
                CBSE curriculum. Your role is to ensure math problems are grade-appropriate and maintain 
                educational value while allowing for creative variations. Be strict about rejecting any 
                problems with advanced mathematical concepts not in the grade level curriculum.""",
                json_mode=True
            )
            
            content = response.get("content", "")
            if not content:
                self.logger.warning("Empty response from LLM in grade check")
                return False, "Could not validate problem: Empty response"

            # Parse the response
            try:
                content = content.strip().strip('```json').strip('```').strip()
                result = json.loads(content)
                
                # Check for explicit rejection due to advanced concepts
                if not result.get("is_appropriate", False):
                    feedback = result.get("feedback", "")
                    if not feedback:
                        feedback = "Problem is not appropriate for the grade level."
                    
                    # Check if the feedback mentions any advanced concepts
                    advanced_terms = [
                        'calculus', 'derivative', 'integral', 'trigonometry', 'sine', 'cosine', 'tangent',
                        'matrix', 'matrices', 'complex', 'imaginary', 'polynomial', 'theorem', 'proof',
                        'advanced', 'beyond grade level', 'too difficult', 'too complex'
                    ]
                    
                    # If feedback mentions advanced concepts, return it as is
                    if any(term in feedback.lower() for term in advanced_terms):
                        return False, feedback
                    
                    # Otherwise, add a general message about grade level
                    return False, f"{feedback} This problem is not appropriate for grade {self.grade_level}."
                    
                # If we get here and it's appropriate, return success
                return True, result.get("feedback", "Problem is appropriate for grade level.")
                
            except json.JSONDecodeError as e:
                self.logger.warning(f"Invalid JSON from LLM in grade check: {e}\nContent: {content}")
                # Fall back to basic validation if JSON parsing fails
                has_advanced, reason = self._contains_advanced_math(problem)
                if has_advanced:
                    return False, reason
                return False, "Could not validate problem: Invalid response format"
                
        except Exception as e:
            self.logger.error(f"Error in grade validation: {str(e)}")
            # Fall back to basic validation on error
            has_advanced, reason = self._contains_advanced_math(problem)
            if has_advanced:
                return False, reason
            return False, f"Error validating problem: {str(e)}"

    def _contains_advanced_math(self, problem: str) -> Tuple[bool, str]:
        """
        Lightweight heuristic to catch clearly advanced topics (e.g., derivatives) not suitable for Grade 7.
        Returns (True, reason) if advanced terms are detected; otherwise (False, "").
        """
        advanced_terms = [
            # Calculus
            'derivative', 'integral', 'calculus', 'differentiate', 'antiderivative', 'd/dx', '∫', '∂', 'limit',
            # Trigonometry
            'trigonometry', 'sine', 'cosine', 'tangent', 'cotangent', 'secant', 'cosecant', 'sin(', 'cos(', 'tan(',
            # Advanced algebra / linear algebra
            'matrix', 'matrices', 'determinant', 'eigenvalue', 'eigenvector', 'vector space', 'tensor',
            'complex number', 'imaginary', 'polynomial long division',
            # Advanced geometry / proofs
            'theorem', 'proof', 'lemma', 'corollary', 'non-euclidean', 'manifold', 'topology',
            # Analysis / differential equations
            'real analysis', 'complex analysis', 'functional analysis', 'measure theory',
            'differential equation', 'partial differential', 'pde', 'ode',
            # Higher combinatorics
            'permutation', 'combination', 'factorial', 'binomial theorem',
            # Transcendentals / logs (beyond basic grade-7 treatment)
            'logarithm', 'ln(', 'log(' 
        ]
        text = problem.lower()
        found = [t for t in advanced_terms if t in text]
        if found:
            # Show a concise subset of terms
            shown = ", ".join(f"'{t}'" for t in found[:5]) + (f" and {len(found)-5} more" if len(found) > 5 else "")
            return True, (
                f"Problem contains advanced mathematical concepts not suitable for grade {self.grade_level}: {shown}. "
                f"Please use only grade-appropriate concepts."
            )
        return False, ""
    
    async def _validate_math_correctness(self, problem: str, solution: str) -> Tuple[bool, str]:
        """
        Use AI to validate that the solution correctly solves the problem.
        Uses a streamlined prompt focused on quick validation.
        """
        prompt = f"""
        [SYSTEM]
        You are a math validator. Quickly check if the solution is correct.
        Respond ONLY with JSON in this format:
        {{
            "is_correct": boolean,
            "feedback": "Brief explanation if incorrect, else 'Correct'"
        }}
        
        [PROBLEM]
        {problem}
        
        [SOLUTION]
        {solution}
        
        [RULES]
        1. If the solution is correct, respond with {{"is_correct": true, "feedback": "Correct"}}
        2. If incorrect, provide a brief 1-2 sentence explanation
        3. Focus on major errors only (wrong operations, incorrect logic, wrong final answer)
        4. Be strict with units and final answers
        5. Ignore minor formatting issues
        """
        
        try:
            # Use a shorter timeout for validation
            response = await asyncio.wait_for(
                self.generate_with_llm(
                    prompt=prompt,
                    system_prompt="You are a math validator. Be concise and accurate.",
                    json_mode=True,
                    temperature=0.1  # Lower temperature for more deterministic responses
                ),
                timeout=15  # 15 second timeout
            )
            
            content = response.get("content", "").strip()
            if not content:
                return False, "Validation failed: Empty response"

            # Clean and parse the response
            try:
                content = content.strip('```json').strip('```').strip()
                result = json.loads(content)
                
                is_correct = result.get("is_correct", False)
                feedback = result.get("feedback", "No feedback provided")
                
                if not is_correct and feedback == "Correct":
                    feedback = "Incorrect solution"
                    
                return is_correct, feedback
                
            except json.JSONDecodeError:
                # If JSON parsing fails, fall back to a quick LLM check
                return await self._fallback_validation(problem, solution)
                
        except asyncio.TimeoutError:
            return False, "Validation timed out"
        except Exception as e:
            self.logger.error(f"Validation error: {str(e)}")
            return False, f"Validation error: {str(e)}"
        
    
    async def _fallback_validation(self, problem: str, solution: str) -> Tuple[bool, str]:
        """
        Fallback validation when primary validation fails.
        Uses a simpler, more direct prompt for reliability.
        """
        prompt = f"""
        Is this solution correct? Answer only YES or NO.
        
        Problem: {problem}
        Solution: {solution}
        """
        
        try:
            response = await self.generate_with_llm(
                prompt=prompt,
                system_prompt="You are a math validator. Answer only YES or NO.",
                temperature=0.0,
                max_tokens=5
            )
            
            is_correct = response.get("content", "").strip().upper().startswith("YES")
            return is_correct, "Validated (fallback)"
            
        except Exception as e:
            self.logger.error(f"Fallback validation failed: {str(e)}")
            return False, "Validation failed"
    
    async def _check_explanation_quality(self, solution: str) -> Tuple[bool, str]:
        """
        Use AI to validate the quality of the solution's explanation.
        
        Args:
            solution: The solution explanation to evaluate

        Returns:
            Tuple of (is_quality, feedback)
        """
        prompt = f"""
        Evaluate the quality of this solution's explanation for a {self.grade_level}th-grade student.

        Solution: {solution}

        Check for:
        1. Clarity and simplicity of language
        2. Step-by-step breakdown
        3. Completeness of the explanation

        Respond with a JSON object containing:
        - is_quality (boolean): True if the explanation is high quality
        - feedback (string): Specific suggestions for improvement
        """

        try:
            response = await self.generate_with_llm(
                prompt=prompt,
                system_prompt="You are an expert math teacher evaluating solution explanations.",
                json_mode=True
            )

            content = response.get("content", "")
            if not content:
                self.logger.warning("Empty response from LLM in explanation quality check")
                return True, "Explanation quality check inconclusive - empty response"

            # Parse the response
            try:
                content = content.strip().strip('```json').strip('```').strip()
                result = json.loads(content)
                return result.get("is_quality", False), result.get("feedback", "No feedback provided")
            except json.JSONDecodeError as e:
                self.logger.warning(f"Invalid JSON from LLM in explanation quality check: {e}\nContent: {content}")
                return True, "Could not evaluate explanation quality: Invalid response format"

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

