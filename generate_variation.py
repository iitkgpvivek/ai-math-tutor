import asyncio
import json
import logging
import os
import random
from typing import Any, Dict

from agents import TeacherAgent, StudentAgent

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROBLEMS_DIR = os.path.join(ROOT_DIR, 'data', 'problems')

def pick_random_problem_file() -> str:
    """Pick a random problem file from the problems directory."""
    problem_files = [f for f in os.listdir(PROBLEMS_DIR) if f.endswith('.json')]
    if not problem_files:
        raise FileNotFoundError(f"No problem files found in {PROBLEMS_DIR}")
    random_file = random.choice(problem_files)
    return os.path.join(PROBLEMS_DIR, random_file)

def load_original_question(path: str) -> str:
    """Load the original question from a JSON file."""
    with open(path, 'r') as f:
        data = json.load(f)
    question = data.get('original_question')
    if not question:
        raise ValueError(f"File {path} has no 'original_question' field")
    return question

async def main():
    """
    Main function to generate a problem variation from a real problem.
    """
    logger.info("Starting problem variation generation...")

    try:
        path = pick_random_problem_file()
        logger.info(f"Picked problem file: {os.path.basename(path)}")
        original_question = load_original_question(path)
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"Failed to load a problem: {e}")
        return

    # The TeacherAgent requires a StudentAgent for its validation loop,
    # so we provide one.
    student = StudentAgent(grade_level=7)
    teacher = TeacherAgent(student_agent=student, problems_dir=PROBLEMS_DIR)

    logger.info("Generating and validating a problem variation... (This may take a moment)")
    try:
        problem = await teacher.generate_problem_variation(original_question)

        if problem and problem.status == 'approved':
            logger.info("Successfully generated and validated a problem variation.")
            print("\n" + "="*20 + " APPROVED VARIATION " + "="*20)
            print(f"\nOriginal Question:\n{problem.original_question}\n")
            print(f"Generated Variation:\n{problem.variation}\n")
            print(f"Generated Solution:\n{problem.solution}\n")
            print("="*62)
        else:
            logger.error("Failed to generate an approved problem variation.")
            if problem:
                logger.warning(f"The last attempt was rejected. Status: {problem.status}")
                print("\n" + "="*20 + " REJECTED VARIATION " + "="*20)
                print(f"\nOriginal Question:\n{problem.original_question}\n")
                print(f"Generated Variation:\n{problem.variation}\n")
                print(f"Generated Solution:\n{problem.solution}\n")
                if problem.reviews:
                    last_review = problem.reviews[-1]
                    print(f"\nRejection Reason: {last_review.feedback}")
                    print(f"Validation Result: {last_review.validation_result.value}")
                print("="*62)
            else:
                logger.error("The generation process returned no result at all.")

    except Exception:
        import traceback
        logger.error(f"An exception occurred during variation generation:\n{traceback.format_exc()}")

if __name__ == '__main__':
    asyncio.run(main())
