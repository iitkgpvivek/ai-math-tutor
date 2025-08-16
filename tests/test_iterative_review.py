import asyncio
import logging
import sys
import pytest
from pathlib import Path

# Add the parent directory to the path so we can import the agents
sys.path.append(str(Path(__file__).parent.parent))

from agents.teacher_agent import TeacherAgent
from agents.student_agent import StudentAgent
from agents.teacher_agent import ProblemVariation

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('test_iterative_review.log')
    ]
)
logger = logging.getLogger(__name__)

# Test cases
TEST_CASES = [
    {
        'name': 'Simple Algebra',
        'problem': 'Solve for x: 2x + 3 = 7',
        'solution': 'Subtract 3 from both sides: 2x = 4. Then divide both sides by 2: x = 2',
        'should_pass': True,
        'description': 'Basic algebra problem that should pass validation'
    },
    {
        'name': 'Advanced Concept',
        'problem': 'Find the derivative of f(x) = x² with respect to x. Show all steps of differentiation.',
        'solution': 'Using the power rule, the derivative of x² is 2x. Therefore, f\'(x) = 2x',
        'should_pass': False,
        'description': 'Contains calculus concept (derivatives) not suitable for grade 7',
        'expected_feedback': 'derivative',  # Check for any mention of derivative/calculus
        'required_keywords': ['calculus', 'derivative', 'advanced', 'grade level']
    },
    {
        'name': 'Multi-part Problem',
        'problem': "(i) Find the perimeter of a rectangle with length 5cm and width 3cm.\n(ii) Find its area.",
        'solution': "(i) Perimeter = 2 × (5cm + 3cm) = 16cm\n(ii) Area = 5cm × 3cm = 15cm²",
        'should_pass': True,  # This is actually a valid 7th grade problem
        'description': 'Multi-part geometry problem with perimeter and area',
        'expected_feedback': ''
    },
    {
        'name': 'Incomplete Problem',
        'problem': 'Calculate the area of a circle',
        'solution': 'The area of a circle is πr² where r is the radius. Since the radius is not provided, we cannot calculate the area.',
        'should_pass': False,
        'description': 'Missing required information (radius)',
        'expected_feedback': 'incomplete',
        'required_keywords': ['incomplete', 'missing', 'radius']
    },
    {
        'name': 'Word Problem',
        'problem': 'A train travels at 60 km/h. How far will it travel in 3 hours?',
        'solution': 'Using the formula distance = speed × time, the train will travel 60 km/h × 3 h = 180 kilometers.',
        'should_pass': True,
        'description': 'A simple word problem involving distance, speed, and time.'
    }
]

# LLM Configuration
llm_config = {
    "llm_model": "mistral",
    "llm_temperature": 0.7
}

@pytest.fixture
def student_agent():
    """Fixture for creating a StudentAgent."""
    logger.info("Creating StudentAgent fixture...")
    student = StudentAgent(
        grade_level=7,
        config=llm_config
    )
    logger.info("StudentAgent fixture created.")
    return student

@pytest.fixture
def teacher_agent(student_agent):
    """Fixture for creating a TeacherAgent."""
    logger.info("Creating TeacherAgent fixture...")
    teacher = TeacherAgent(
        student_agent=student_agent,
        config=llm_config
    )
    logger.info("TeacherAgent fixture created.")
    return teacher

@pytest.mark.parametrize("test_case", TEST_CASES)
@pytest.mark.asyncio
async def test_validation(teacher_agent: TeacherAgent, test_case: dict, max_attempts: int = 3):
    """Test the iterative validation process for a single test case."""
    logger.info(f"\n{'='*80}")
    logger.info(f"TEST CASE: {test_case['name']}")
    logger.info(f"Description: {test_case['description']}")
    logger.info(f"Problem: {test_case['problem']}")
    
    problem = ProblemVariation(
        original_question=test_case['problem'],
        variation=test_case['problem'],
        solution=test_case.get('solution', 'Test solution')
    )
    
    result = await teacher_agent._validate_problem(problem, max_iterations=max_attempts)
    is_valid = result.get("is_valid", False)
    feedback = result.get("feedback", "").lower()

    logger.info(f"Final validation result: {'VALID' if is_valid else 'INVALID'}")
    logger.info(f"Final Feedback: {feedback}")
    logger.info(f"Iterations: {result.get('iterations')}")
    
    # Check if the problem should pass validation
    if test_case['should_pass']:
        assert is_valid, f"Expected problem to pass validation but it failed with feedback: {feedback}"
    else:
        # For problems that should fail, check if the feedback indicates the expected issue
        expected_feedback = test_case.get('expected_feedback', '').lower()
        required_keywords = test_case.get('required_keywords', [])
        
        if expected_feedback:
            assert expected_feedback in feedback, f"Expected feedback to contain '{expected_feedback}' but got: {feedback}"
        
        # Check for any of the required keywords in the feedback
        if required_keywords:
            keyword_found = any(keyword in feedback.lower() for keyword in required_keywords)
            assert keyword_found, f"Expected feedback to contain one of {required_keywords} but got: {feedback}"
        
        assert not is_valid, f"Expected problem to fail validation but it passed with feedback: {feedback}"
