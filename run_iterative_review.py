import asyncio
import json
import logging
import os
import random
from typing import Any, Dict

from agents.teacher_agent import TeacherAgent, ProblemVariation
from agents.student_agent import StudentAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("IterativeReviewRunner")

PROBLEMS_DIR = os.path.join(os.path.dirname(__file__), 'data', 'problems')


def pick_random_problem_file() -> str:
    files = [f for f in os.listdir(PROBLEMS_DIR) if f.endswith('.json')]
    if not files:
        raise FileNotFoundError(f"No problem JSONs found in {PROBLEMS_DIR}")
    return os.path.join(PROBLEMS_DIR, random.choice(files))


def load_original_question(path: str) -> Dict[str, Any]:
    with open(path, 'r') as f:
        data = json.load(f)
    return {
        'id': data.get('id'),
        'original_question': data.get('original_question')
    }


async def main():
    # Pick and load a problem
    path = pick_random_problem_file()
    meta = load_original_question(path)
    logger.info(f"Picked problem file: {os.path.basename(path)} | id={meta['id']}")
    original_question = meta['original_question']
    if not original_question:
        raise ValueError("Selected problem file has no 'original_question' field")

    # Set up agents
    student = StudentAgent(grade_level=7)
    teacher = TeacherAgent(student_agent=student, problems_dir=PROBLEMS_DIR)
    # Tighten iterations to keep demo quick
    teacher.max_review_iterations = 2

    # Monkeypatch _revise_problem to avoid real LLM calls
    async def fake_revise(self, p: ProblemVariation, feedback: str) -> bool:
        # Simple heuristic: append a note to variation and a placeholder solution
        p.variation = f"{p.variation} (Revised based on feedback: {feedback})"
        if not p.solution or "Placeholder" in p.solution:
            p.solution = (
                "Step 1: Understand the problem. "
                "Step 2: Formulate an equation. "
                "Step 3: Solve for the variable. "
                "Step 4: Check the answer."
            )
        logger.info("Applied fake revision (no LLM)")
        return True

    # Bind method to instance
    import types
    teacher._revise_problem = types.MethodType(fake_revise, teacher)  # type: ignore

    # Build an initial variation using only the original_question (likely to trigger feedback)
    problem = ProblemVariation(
        original_question=original_question,
        variation=original_question,
        solution=""
    )

    logger.info("Starting iterative validation+revision...")
    try:
        result = await asyncio.wait_for(teacher._validate_problem(problem), timeout=60)
    except Exception:
        import traceback
        logger.error("Iterative validation failed with exception:\n%s", traceback.format_exc())
        return

    # Show results
    print("\n=== Iterative Review Result ===")
    print(json.dumps(result, indent=2))
    print("\n=== Final Problem State ===")
    print(f"status: {getattr(problem, 'status', None)}")
    print(f"final variation: {problem.variation[:200]}{'...' if len(problem.variation) > 200 else ''}")
    print(f"final solution: {problem.solution[:200]}{'...' if len(problem.solution) > 200 else ''}")

if __name__ == '__main__':
    asyncio.run(main())
