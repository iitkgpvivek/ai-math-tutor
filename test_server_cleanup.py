#!/usr/bin/env python3
"""
Test script to verify LLM server cleanup.
"""
import time
import psutil
from problem_importer import ProblemImporter

def check_ollama_running():
    """Check if any Ollama process is running."""
    for proc in psutil.process_iter(['name']):
        try:
            if 'ollama' in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def test_server_cleanup():
    """Test that the LLM server is properly cleaned up."""
    print("=== Starting Server Cleanup Test ===\n")
    
    # Check initial state
    print("Checking initial server state...")
    was_running = check_ollama_running()
    print(f"Ollama server was {'already running' if was_running else 'not running'}")
    
    # Create a problem importer (should start the server if needed)
    print("\nCreating ProblemImporter...")
    importer = ProblemImporter()
    
    # Check if server is now running
    print("\nChecking server after ProblemImporter creation...")
    is_running = check_ollama_running()
    print(f"Ollama server is now {'running' if is_running else 'not running'}")
    
    if not is_running:
        print("⚠️ Server did not start as expected!")
        return
    
    # Generate some variations (this should use the LLM)
    print("\nGenerating variations...")
    problem = "A train travels 300 km in 5 hours. What is its speed in km/h?"
    variations = importer.generate_variations(problem, "Speed", num_variations=1)
    print(f"Generated {len(variations)} variations")
    
    # Delete the importer to trigger cleanup
    print("\nDeleting ProblemImporter to trigger cleanup...")
    del importer
    
    # Give it a moment to clean up
    time.sleep(2)
    
    # Check if server is still running
    print("\nChecking server after cleanup...")
    still_running = check_ollama_server()
    print(f"Ollama server is {'still running' if still_running else 'stopped'}")
    
    if still_running and not was_running:
        print("⚠️ Server was not properly cleaned up!")
    elif not still_running and was_running:
        print("✅ Server was stopped correctly (was already running at start)")
    elif not still_running:
        print("✅ Server was started and stopped correctly")
    else:
        print("ℹ️ Server was already running and left running")

def check_ollama_server():
    """Check if Ollama server is responding."""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    test_server_cleanup()
