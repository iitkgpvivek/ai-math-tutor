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
            return False, ValidationResult.INCOMPLETE, "Problem or solution is empty"
            
        if len(solution.split()) < 3:  # Very basic check
            return False, ValidationResult.INCOMPLETE, "Solution is too brief"
        
        # Check grade appropriateness
        is_appropriate, appropriateness_feedback = await self._validate_grade_appropriateness(problem_text, original_question)
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
    
    async def _validate_grade_appropriateness(self, problem: str, original_question: Optional[str] = None) -> Tuple[bool, str]:
        """
        Check if the problem is appropriate for the student's grade level and maintains
        the same mathematical structure as the original problem.
        
        This method is designed for iterative review, providing increasingly specific
        feedback to help improve the problem with each iteration.
        
        Args:
            problem: The problem text to check
            original_question: The original question text for comparison
            
        Returns:
            Tuple of (is_appropriate, feedback)
        """
        # Basic validation - check for empty or invalid input
        if not problem or not problem.strip():
            return False, "Problem text cannot be empty"
            
        problem_lower = problem.lower()
        
        # Get the current iteration from the review history
        current_iteration = len(self.reviews.get(problem, []))
        
        # Check for advanced concepts in lower grades
        if self.grade_level < 8:
            advanced_concepts = [
                ("calculus", "Calculus concepts are typically introduced in higher grades"),
                ("derivative", "Derivatives are too advanced for this grade level"),
                ("integral", "Integrals are too advanced for this grade level"),
                ("matrix", "Matrices are typically introduced in higher grades"),
                ("vector", "Vectors are too advanced for this grade level"),
                ("trigonometry", "Trigonometry is usually introduced in higher grades"),
                ("polynomial", "Polynomials may be too complex for this grade level"),
                ("quadratic", "Quadratic equations are typically taught in higher grades")
            ]
            
            for concept, feedback in advanced_concepts:
                if concept in problem_lower:
                    return False, feedback
                    
        # Check for basic mathematical structure
        has_math_ops = any(op in problem for op in ['+', '-', '*', '/', '=', '>', '<'])
        if not has_math_ops and not any(word in problem_lower for word in ['how many', 'what is', 'find the', 'calculate']):
            return False, "Problem should contain clear mathematical operations or questions"
            
        # If we have an original question, check for structural consistency
        if original_question and len(original_question) > 10:
            # Count number of parts (i), (ii) etc.
            import re
            original_parts = re.findall(r'\([i]+\)', original_question)
            variation_parts = re.findall(r'\([i]+\)', problem)
            
            if len(original_parts) != len(variation_parts):
                return False, f"Original has {len(original_parts)} parts, but variation has {len(variation_parts)} parts"
                
            # Check for similar problem structure
            original_has_vars = bool(re.search(r'[a-zA-Z]', original_question))
            variation_has_vars = bool(re.search(r'[a-zA-Z]', problem))
            
            if original_has_vars != variation_has_vars:
                return False, "Variable usage should match the original problem"
        
        # Adjust validation strictness based on iteration
        if current_iteration == 0:
            # First iteration: Be more lenient, focus on major issues
            return True, "Initial validation passed - will refine in subsequent iterations"
        else:
            # Later iterations: Be more strict with details
            return await self._get_detailed_feedback(problem, original_question, current_iteration)
    
    async def _get_detailed_feedback(self, problem: str, original_question: Optional[str] = None, iteration: int = 0) -> Tuple[bool, str]:
        """
        Use AI to provide detailed feedback on the problem's grade appropriateness and mathematical structure.
        
        Args:
            problem: The problem text to evaluate
            original_question: The original question text for comparison
            iteration: The current iteration number
            
        Returns:
            Tuple of (is_appropriate, feedback)
        """
        prompt = f"""
        Evaluate the grade appropriateness and mathematical structure of this problem for a {self.grade_level}th-grade student.
        
        ORIGINAL PROBLEM:
        {original_question or ''}
        
        NEW VARIATION:
        {problem}
        
        REVIEW INSTRUCTIONS:
        Provide detailed, specific feedback to help improve the problem. Focus on both structure and educational value.
        
        VALIDATION CRITERIA:
        1. Mathematical Structure:
           - Same core problem type as original (e.g., rates, geometry, algebra)
           - Same number of steps to solve
           - Similar complexity in calculations
        
        2. Grade-Level Appropriateness:
           - Concepts align with {self.grade_level}th grade curriculum
           - Language complexity is age-appropriate
           - Problem context is relatable to students
        
        3. For rate and distance problems:
           - Must use the formula: distance = rate × time
           - Must handle negative values correctly (e.g., descending below ground level)
           - Must calculate total distance traveled correctly (final position - initial position)
           - Units must be consistent and appropriate
           
        4. For geometry problems:
           - Must use appropriate geometric principles
           - All necessary information must be provided
           - Diagrams (if any) should be clear and accurate
           
        5. For algebra problems:
           - Equations should be properly formatted
           - Variables should be clearly defined
           - Solution should follow logical steps
           
        FEEDBACK FORMAT:
        1. Start with an overall assessment
        2. List specific issues found
        3. Provide concrete suggestions for improvement
        4. If the problem is valid, explain why it's appropriate
        
        Respond with a JSON object containing:
        {{
            "is_appropriate": boolean,  # Overall assessment
            "maintains_structure": boolean,  # If the math structure matches original
            "difficulty_match": boolean,  # If difficulty matches original
            "feedback": string,  # Detailed explanation of your analysis
            "suggestions": [string]  # Specific improvement suggestions if needed
        }}
        """
        
        try:
            response = await self.generate_with_llm(
                prompt=prompt,
                system_prompt="""You are an expert math curriculum designer with deep knowledge of the 
                CBSE curriculum. Your role is to ensure math problems are grade-appropriate and maintain 
                educational value while allowing for creative variations.""",
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
                
                if not result.get("maintains_structure", False) and original_question:
                    return False, result.get("feedback", "Problem does not maintain the mathematical structure of the original.")
                    
                if not result.get("difficulty_match", False) and original_question:
                    return False, result.get("feedback", "Problem difficulty does not match the original.")
                
                if not result.get("is_appropriate", False):
                    return False, result.get("feedback", "Problem is not appropriate for the grade level.")
                    
                return True, result.get("feedback", "Problem is appropriate for the grade level and maintains the original's structure.")
                
            except json.JSONDecodeError as e:
                self.logger.warning(f"Invalid JSON from LLM in grade check: {e}\nContent: {content}")
                return False, "Could not validate problem: Invalid response format"
                
        except Exception as e:
            self.logger.error(f"Error in grade validation: {str(e)}")
            return False, f"Error validating problem: {str(e)}"
    
    async def _get_detailed_feedback(self, problem: str, original_question: Optional[str] = None, iteration: int = 0) -> Tuple[bool, str]:
        """
        Provide detailed feedback on a problem variation using AI analysis.
        
        Args:
            problem: The problem text to evaluate
            original_question: The original question for comparison (if any)
            iteration: Current iteration number (0-based)
            
        Returns:
            Tuple of (is_appropriate, feedback)
        """
        # Format the original question or use default
        original_display = original_question or 'Not provided'
        
        # Adjust strictness based on iteration
        if iteration == 0:
            strictness = "Be more lenient in the first iteration. Focus on major structural issues and grade-level appropriateness."
        else:
            strictness = "Provide detailed, specific feedback. Focus on both structure and educational value."
        
        # Use AI for comprehensive evaluation
        prompt = f"""
        You are an experienced math teacher reviewing a problem variation for a {self.grade_level}th grade student.
        
        ORIGINAL PROBLEM:
        {original_display}
        
        NEW VARIATION:
        {problem}
        
        REVIEW INSTRUCTIONS:
        {strictness}
        
        VALIDATION CRITERIA:
        1. Mathematical Structure:
           - Same core problem type as original (e.g., rates, geometry, algebra)
           - Same number of steps to solve
           - Similar complexity in calculations
        
        2. Grade-Level Appropriateness:
           - Concepts align with {self.grade_level}th grade curriculum
           - Language complexity is age-appropriate
           - Problem context is relatable to students
        
        3. For rate and distance problems:
           - Must use the formula: distance = rate × time
           - Must handle negative values correctly
           - Must calculate total distance traveled correctly
           - Units must be consistent and appropriate
           
        4. For geometry problems:
           - Must use appropriate geometric principles
           - All necessary information must be provided
           - Diagrams (if any) should be clear and accurate
           
        5. For algebra problems:
           - Equations should be properly formatted
           - Variables should be clearly defined
           - Solution should follow logical steps
        
        FEEDBACK FORMAT:
        1. Start with an overall assessment
        2. List specific issues found
        3. Provide concrete suggestions for improvement
        4. If the problem is valid, explain why it's appropriate
        
        Respond with a JSON object containing:
        {{
            "is_appropriate": boolean,
            "maintains_structure": boolean,
            "difficulty_match": boolean,
            "feedback": string,
            "suggestions": [string]
        }}
        """
        
        try:
            response = await self.generate_with_llm(
                prompt=prompt,
                system_prompt="""You are an expert math curriculum designer with deep knowledge of the 
                CBSE curriculum. Your role is to ensure math problems are grade-appropriate and maintain 
                educational value while allowing for creative variations.""",
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
                
                if not result.get("maintains_structure", False) and original_question:
                    return False, result.get("feedback", "Problem does not maintain the mathematical structure of the original.")
                    
                if not result.get("difficulty_match", False) and original_question:
                    return False, result.get("feedback", "Problem difficulty does not match the original.")
                
                if not result.get("is_appropriate", False):
                    return False, result.get("feedback", "Problem is not appropriate for the grade level.")
                    
                return True, result.get("feedback", "Problem is appropriate for the grade level and maintains the original's structure.")
                
            except json.JSONDecodeError as e:
                self.logger.warning(f"Invalid JSON from LLM in grade check: {e}\nContent: {content}")
                return False, "Could not validate problem: Invalid response format"
                
        except Exception as e:
            self.logger.error(f"Error in grade validation: {str(e)}")
            return False, f"Error validating problem: {str(e)}"
    
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
        You are an expert math validator. Carefully analyze this problem and solution:
        
        PROBLEM: {problem}
        
        STUDENT'S SOLUTION: {solution}
        
        INSTRUCTIONS:
        1. First, identify the type of problem (rate/distance, triangle angles, etc.)
        2. Verify the mathematical correctness step by step
        3. Pay special attention to:
           - Correct use of formulas
           - Proper handling of units
           - Logical flow of the solution
           - Correctness of calculations
        
        FOR RATE/DISTANCE PROBLEMS:
        - Verify the formula: distance = rate × time is used correctly
        - Check that direction (up/down, positive/negative) is handled properly
        - Ensure the final answer has appropriate units
        
        FOR TRIANGLE PROBLEMS:
        - Verify angle sum property (sum of angles = 180°)
        - Check that isosceles triangle properties are correctly applied
        - Ensure the solution follows logically from given information
        
        Respond with a JSON object containing:
        {{
            "is_correct": boolean,  # Whether the solution is mathematically correct
            "feedback": string,     # Detailed explanation of any issues found
            "correct_answer": string, # The correct answer (if solution is wrong)
            "error_type": string     # Type of error if any (e.g., "calculation", "formula", "units")
        }}
        
        If the solution is incorrect, provide detailed feedback on what's wrong and how to fix it.
        """
        
        try:
            # Use the base agent's LLM integration
            response = await self.generate_with_llm(
                prompt=prompt,
                system_prompt="You are a math expert that validates solutions to math problems.",
                json_mode=True
            )
            
            content = response.get("content", "")
            if not content:
                self.logger.warning("Empty response from LLM in math validation")
                return False, "Could not validate solution: Empty response"

            # Parse the response
            try:
                content = content.strip().strip('```json').strip('```').strip()
                result = json.loads(content)
                
                # Use the AI's judgment for all validation
                is_correct = result.get("is_correct", False)
                feedback = result.get("feedback", "No validation feedback")
                
                # If the AI detected context inappropriateness, trust that judgment
                if result.get("context_appropriate", True) is False:
                    return False, feedback or "The solution doesn't make sense in the given context."
                    
                # If the AI says it requires an integer but the answer isn't one
                if result.get("requires_integer", False) and "." in solution and any(word in solution.lower() for word in [".", "point"]):
                    return False, feedback or "The solution requires a whole number answer, but got a decimal."
                
                return is_correct, feedback
                
            except json.JSONDecodeError as e:
                self.logger.warning(f"Invalid JSON from LLM in math validation: {e}\nContent: {content}")
                return False, "Could not validate solution: Invalid response format"
                
        except Exception as e:
            self.logger.error(f"Error in math validation: {str(e)}")
            return False, f"Error validating solution: {str(e)}"
        
        current_iteration = len(self.reviews.get(problem, []))
        
        # Adjust validation strictness based on iteration
        if current_iteration == 0:
            # First iteration: Be more lenient, focus on major issues
            strictness = "Be more lenient in the first iteration. Focus on major structural issues and grade-level appropriateness."
        else:
            # Later iterations: Be more strict with details
            strictness = "Provide detailed, specific feedback to help improve the problem. Focus on both structure and educational value."
        
        # Use AI for comprehensive evaluation
        prompt = f"""
        You are an experienced math teacher reviewing a problem variation for a {self.grade_level}th grade student.
        
        ORIGINAL PROBLEM:
        {original_display}
        
        NEW VARIATION:
        {problem}
        
        REVIEW INSTRUCTIONS:
        {strictness}
        
        VALIDATION CRITERIA:
        1. Mathematical Structure:
           - Same core problem type as original (e.g., rates, geometry, algebra)
           - Same number of steps to solve
           - Similar complexity in calculations
        
        2. Grade-Level Appropriateness:
           - Concepts align with {self.grade_level}th grade curriculum
           - Language complexity is age-appropriate
           - Problem context is relatable to students
        
        3. For rate and distance problems:
           - Must use the formula: distance = rate × time
           - Must handle negative values correctly (e.g., descending below ground level)
           - Must calculate total distance traveled correctly (final position - initial position)
           - Units must be consistent and appropriate
           
        4. For geometry problems:
           - Must use appropriate geometric principles
           - All necessary information must be provided
           - Diagrams (if any) should be clear and accurate
           
        5. For algebra problems:
           - Equations should be properly formatted
           - Variables should be clearly defined
           - Solution should follow logical steps
           
        FEEDBACK FORMAT:
        1. Start with an overall assessment
        2. List specific issues found
        3. Provide concrete suggestions for improvement
        4. If the problem is valid, explain why it's appropriate
        
        3. For isosceles triangle problems:
           - If original gives vertex angle and asks for base angles, variation must do the same
           - If original gives base angles and asks for vertex angle, variation must do the same
           - The sum of angles must always be 180°
        
        4. Grade-level considerations:
           - Appropriate for {self.grade_level}th grade (CBSE)
           - Clear and unambiguous language
           - Reasonable number sizes and complexity
        
        Respond with a JSON object containing:
        {{
            "is_appropriate": boolean,  # Overall assessment
            "maintains_structure": boolean,  # If the math structure matches original
            "difficulty_match": boolean,  # If difficulty matches original
            "feedback": string,  # Detailed explanation of your analysis
            "suggestions": [string]  # Specific improvement suggestions if needed
        }}
        """
        
        try:
            response = await self.generate_with_llm(
                prompt=prompt,
                system_prompt="""You are an expert math curriculum designer with deep knowledge of the 
                CBSE curriculum. Your role is to ensure math problems are grade-appropriate and maintain 
                educational value while allowing for creative variations.""",
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
                
                if not result.get("maintains_structure", False) and original_question:
                    return False, result.get("feedback", "Problem does not maintain the mathematical structure of the original.")
                    
                if not result.get("difficulty_match", False) and original_question:
                    return False, result.get("feedback", "Problem difficulty does not match the original.")
                
                if not result.get("is_appropriate", False):
                    return False, result.get("feedback", "Problem is not appropriate for the grade level.")
                    
                return True, result.get("feedback", "Problem is appropriate for the grade level and maintains the original's structure.")
                
            except json.JSONDecodeError as e:
                self.logger.warning(f"Invalid JSON from LLM in grade check: {e}\nContent: {content}")
                return False, "Could not validate problem: Invalid response format"
                
        except Exception as e:
            self.logger.error(f"Error in grade validation: {str(e)}")
            return False, f"Error validating problem: {str(e)}"
    
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

