import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from agents.teacher_agent import TeacherAgent, ProblemVariation
from agents.student_agent import StudentAgent, ValidationResult

class TestTeacherAgent(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        """Set up for the test cases."""
        self.mock_student_agent = MagicMock(spec=StudentAgent)
        self.mock_student_agent.validate_problem = AsyncMock()
        self.teacher_agent = TeacherAgent(student_agent=self.mock_student_agent)
        self.teacher_agent.logger = MagicMock()

    @patch('agents.teacher_agent.TeacherAgent._revise_problem', new_callable=AsyncMock)
    async def test_revision_loop_success(self, mock_revise_problem):
        """Test the revision loop where a problem is initially invalid, then revised and becomes valid."""
        # Arrange
        problem = ProblemVariation(
            original_question="2+2=?",
            variation="What is two plus two?",
            solution="4"
        )

        # Mock the student agent to first reject, then approve
        self.mock_student_agent.validate_problem.side_effect = [
            {
                "is_valid": False, 
                "feedback": "Needs more detail", 
                "validation_result": ValidationResult.INCOMPLETE.value
            },
            {
                "is_valid": True, 
                "feedback": "Approved", 
                "validation_result": ValidationResult.VALID.value
            }
        ]

        mock_revise_problem.return_value = True

        # Act
        result = await self.teacher_agent._validate_problem(problem)

        # Assert
        self.assertTrue(result['is_valid'])
        self.assertEqual(result['iterations'], 2)
        self.assertEqual(self.mock_student_agent.validate_problem.call_count, 2)
        mock_revise_problem.assert_called_once()
        self.assertEqual(problem.status, "approved")

    @patch('agents.teacher_agent.TeacherAgent._revise_problem', new_callable=AsyncMock)
    async def test_revision_loop_failure_after_retries(self, mock_revise_problem):
        """Test that the revision loop terminates after max retries."""
        # Arrange
        problem = ProblemVariation(
            original_question="3*x=12",
            variation="3x=12",
            solution="x=4"
        )
        self.teacher_agent.max_review_iterations = 2

        # Mock the student agent to always reject
        def mock_validate(problem, solution, problem_id=None):
            # This will be called twice due to max_review_iterations=2
            return {
                "is_valid": False, 
                "feedback": "Too simple", 
                "validation_result": ValidationResult.TOO_EASY.value
            }
            
        self.mock_student_agent.validate_problem.side_effect = mock_validate
        mock_revise_problem.return_value = True

        # Act
        result = await self.teacher_agent._validate_problem(problem)

        # Assert
        self.assertFalse(result['is_valid'])
        self.assertEqual(result['iterations'], 3)  # Initial validation + max_review_iterations
        self.assertEqual(self.mock_student_agent.validate_problem.call_count, 3)  # Called 3 times
        self.assertEqual(mock_revise_problem.call_count, 2)  # Called twice - once after each failed validation
        self.assertEqual(problem.status, "rejected")  # Status should be 'rejected' after max retries

if __name__ == '__main__':
    unittest.main()
