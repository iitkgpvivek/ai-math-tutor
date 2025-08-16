import asyncio
import statistics
import time
from pathlib import Path
import sys

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent))

from agents.teacher_agent import TeacherAgent, ProblemVariation
from agents.student_agent import StudentAgent

# Configuration
LLM_CONFIG = {
    "llm_model": "mistral",
    "llm_temperature": 0.7
}

TEST_PROBLEMS = [
    {
        'problem': 'If 5x + 3 = 23, what is the value of x?',
        'solution': 'x = 4',
        'description': 'Simple linear equation'
    },
    {
        'problem': 'A train travels 300 km in 4 hours. What is its speed in km/h?',
        'solution': '75 km/h',
        'description': 'Basic speed calculation'
    },
    {
        'problem': 'What is the area of a rectangle with length 8 cm and width 5 cm?',
        'solution': '40 cm²',
        'description': 'Basic area calculation'
    }
]

async def test_student_validation(student: StudentAgent, problem: str, solution: str) -> float:
    """Test validation time for student agent."""
    start_time = time.time()
    try:
        is_valid, feedback = await student._validate_math_correctness(problem, solution)
        return time.time() - start_time, is_valid
    except Exception as e:
        return time.time() - start_time, False

async def test_teacher_validation(teacher: TeacherAgent, problem_data: dict) -> float:
    """Test validation time for teacher agent."""
    problem = ProblemVariation(
        original_question=problem_data['problem'],
        variation=problem_data['problem'],
        solution=problem_data['solution']
    )
    
    start_time = time.time()
    try:
        result = await teacher._validate_problem(
            problem,
            max_iterations=1,
            iteration_timeout=30,
            total_timeout=30
        )
        return time.time() - start_time, result.get('is_valid', False)
    except Exception as e:
        return time.time() - start_time, False

async def run_tests():
    """Run performance tests for both agents."""
    student = StudentAgent(grade_level=7, config=LLM_CONFIG)
    teacher = TeacherAgent(student_agent=student, config=LLM_CONFIG)
    
    print("\n=== Testing Student Agent ===")
    student_times = []
    for i, test in enumerate(TEST_PROBLEMS, 1):
        time_taken, is_valid = await test_student_validation(student, test['problem'], test['solution'])
        student_times.append(time_taken)
        print(f"{i}. {test['description']}: {time_taken:.2f}s (Valid: {is_valid})")
    
    print("\n=== Testing Teacher Agent ===")
    teacher_times = []
    for i, test in enumerate(TEST_PROBLEMS, 1):
        time_taken, is_valid = await test_teacher_validation(teacher, test)
        teacher_times.append(time_taken)
        print(f"{i}. {test['description']}: {time_taken:.2f}s (Valid: {is_valid})")
    
    # Print summary
    print("\n=== Summary ===")
    print(f"Student Agent - Avg: {statistics.mean(student_times):.2f}s, "
          f"Min: {min(student_times):.2f}s, "
          f"Max: {max(student_times):.2f}s")
    
    print(f"Teacher Agent - Avg: {statistics.mean(teacher_times):.2f}s, "
          f"Min: {min(teacher_times):.2f}s, "
          f"Max: {max(teacher_times):.2f}s")

if __name__ == "__main__":
    asyncio.run(run_tests())
