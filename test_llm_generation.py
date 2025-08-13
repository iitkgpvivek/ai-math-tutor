import signal
import sys
from custom_worksheet_creator import generate_llm_problems

def handler(signum, frame):
    print("\nTest timed out after 60 seconds")
    sys.exit(1)

# Set the signal handler
signal.signal(signal.SIGALRM, handler)
signal.alarm(60)  # 60 second timeout

try:
    print("Testing problem generation with 60 second timeout...")
    problems = generate_llm_problems('integer', 1, 'medium')
    if problems:
        print("\n✅ Success! Generated problem:")
        print(f"\nProblem:\n{problems[0]['problem']}")
        print(f"\nSolution:\n{problems[0]['solution']}")
    else:
        print("\n❌ No problems were generated")
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
finally:
    signal.alarm(0)  # Disable the alarm
