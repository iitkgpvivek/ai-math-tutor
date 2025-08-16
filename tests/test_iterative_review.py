import asyncio
import logging
import sys
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
        'should_pass': True,
        'description': 'Basic algebra problem that should pass validation'
    },
    {
        'name': 'Advanced Concept',
        'problem': 'Find the derivative of f(x) = x²',
        'should_pass': True,
        'description': 'Contains calculus concept not suitable for grade 7'
    },
    {
        'name': 'Multi-part Problem',
        'problem': "(i) Find the perimeter of a rectangle with length 5cm and width 3cm.\n(ii) Find its area.",
        'should_pass': False,
        'description': 'Multi-part geometry problem'
    },
    {
        'name': 'Incomplete Problem',
        'problem': 'Calculate the area of a circle',
        'should_pass': True,
        'description': 'Missing required information (radius)'
    },
    {
        'name': 'Word Problem',
        'problem': 'A train travels at 60 km/h. How far will it travel in 3 hours?',
        'should_pass': True,
        'description': 'A simple word problem involving distance, speed, and time.'
    }
]

async def test_validation(teacher: TeacherAgent, student: StudentAgent, max_attempts: int = 3):
    """Test the iterative validation process with the given agents."""
    for test_case in TEST_CASES:
        logger.info(f"\n{'='*80}")
        logger.info(f"TEST CASE: {test_case['name']}")
        logger.info(f"Description: {test_case['description']}")
        logger.info(f"Problem: {test_case['problem']}")
        
        # Create a problem variation
        problem = ProblemVariation(
            original_question=test_case['problem'],
            variation=test_case['problem'],
            solution='Test solution'
        )
        
        # Test validation
        result = await teacher._validate_problem(problem, max_iterations=max_attempts)
        is_valid = result.get("is_valid", False)

        logger.info(f"Final validation result: {'VALID' if is_valid else 'INVALID'}")
        logger.info(f"Final Feedback: {result.get('feedback')}")
        logger.info(f"Iterations: {result.get('iterations')}")
        
        # Verify the result
        if test_case['should_pass'] and not is_valid:
            logger.error(f"❌ Test failed: Expected to pass but failed with feedback: {result.get('feedback')}")
        elif not test_case['should_pass'] and is_valid:
            logger.error(f"❌ Test failed: Expected to fail but passed with feedback: {result.get('feedback')}")
        else:
            logger.info(f"✅ Test passed as expected")

async def main():
    try:
        # LLM Configuration
        llm_config = {
            "llm_model": "mistral",
            "llm_temperature": 0.7
        }

        # Initialize agents
        student = StudentAgent(
            grade_level=7,
            config=llm_config
        )
        
        teacher = TeacherAgent(
            student_agent=student,
            config=llm_config
        )
        
        # Run the tests
        logger.info("Starting iterative review tests...")
        await test_validation(teacher, student, max_attempts=3)
        logger.info("All tests completed!")

    except Exception as e:
        logger.error("An error occurred during the test run.", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main())
