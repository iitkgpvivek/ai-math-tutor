import os
import subprocess
import requests
import json
import signal
import time
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import atexit
import sys

# Global variable to track if we started the server
_ollama_process = None

def ensure_ollama_server() -> Tuple[bool, bool]:
    """Ensure Ollama server is running. Start it if not running.
    
    Returns:
        Tuple of (is_running, did_start) where:
        - is_running: Whether server is now running
        - did_start: Whether we started the server
    """
    global _ollama_process
    
    # Check if server is already running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            return True, False  # Server is running, we didn't start it
    except (requests.exceptions.RequestException, requests.exceptions.Timeout):
        pass  # Server is not running or not responding
    
    # Try to start the server
    try:
        # Check if Ollama is installed
        if os.name == 'nt':  # Windows
            ollama_cmd = 'ollama'
        else:  # Unix-like
            ollama_cmd = 'ollama'
            
        # Start the server in the background
        _ollama_process = subprocess.Popen(
            [ollama_cmd, 'serve'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True
        )
        
        # Wait for server to start (up to 30 seconds)
        for _ in range(30):
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=1)
                if response.status_code == 200:
                    # Register cleanup on exit
                    atexit.register(stop_ollama_server)
                    return True, True
            except (requests.exceptions.RequestException, requests.exceptions.Timeout):
                pass
            time.sleep(1)
        
        # If we get here, server didn't start properly
        return False, False
        
    except Exception as e:
        print(f"Error starting Ollama server: {e}", file=sys.stderr)
        return False, False

def stop_ollama_server():
    """Stop the Ollama server if we started it."""
    global _ollama_process
    
    if _ollama_process:
        try:
            # Try to terminate gracefully first
            _ollama_process.terminate()
            try:
                _ollama_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if not terminating
                _ollama_process.kill()
                _ollama_process.wait()
        except Exception as e:
            print(f"Error stopping Ollama server: {e}", file=sys.stderr)
        finally:
            _ollama_process = None

class LocalLLMGenerator:
    def __init__(self, model_name: str = "phi3", auto_start_server: bool = True, cache_dir: str = None):
        """Initialize the LLM generator.
        
        Args:
            model_name: Name of the model to use (must be pulled with Ollama)
            auto_start_server: Whether to automatically start the Ollama server if not running
            cache_dir: Optional custom directory for cache files (defaults to 'data/llm_cache')
        """
        self.base_url = "http://localhost:11434/api"
        self.model_name = model_name
        self.cache_dir = Path(cache_dir) if cache_dir else Path("data") / "llm_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.auto_start_server = auto_start_server
        self._server_started = False
        
        if auto_start_server:
            self.ensure_server()
    
    def ensure_server(self) -> bool:
        """Ensure the Ollama server is running."""
        is_running, did_start = ensure_ollama_server()
        self._server_started = did_start
        return is_running
    
    def __del__(self):
        """Cleanup when the generator is destroyed."""
        if self._server_started:
            stop_ollama_server()
    
    def _check_server(self) -> bool:
        """Check if Ollama server is running and model is available."""
        try:
            # First check if server is responding
            response = requests.get(f"{self.base_url}/tags", timeout=5)
            if response.status_code != 200:
                return False
                
            # Check if model is available
            models = response.json().get('models', [])
            return any(model['name'].startswith(f"{self.model_name}:") for model in models)
            
        except (requests.exceptions.RequestException, json.JSONDecodeError):
            return False
        
    def _get_cache_path(self, problem_hash: str) -> Path:
        """Get path to cache file for a given problem"""
        # Ensure the cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        return self.cache_dir / f"{problem_hash}.json"

    def _check_server(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/tags")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def _generate_with_llm(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate response using local LLM with enhanced mathematical reasoning
        
        Args:
            prompt: The prompt to send to the LLM
            temperature: Controls randomness (0.0 to 1.0, higher is more random)
            
        Returns:
            str: The raw text response from the LLM
        """
        try:
            response = requests.post(
                f"{self.base_url}/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "format": "json",
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "top_p": 0.9,
                        "num_ctx": 4096,  # Larger context window
                        "repeat_penalty": 1.1,  # Slightly penalize repetition
                        "top_k": 40,  # Consider more tokens
                        "seed": int(time.time())  # Add some randomness
                    }
                },
                timeout=300  # 5 minute timeout for complex problems
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except Exception as e:
            print(f"Error generating variation: {str(e)}")
            return ""

    def _clean_json_response(self, text: str) -> Dict[str, Any]:
        """Clean and parse JSON response from LLM, handling common formatting issues."""
        try:
            # Try to parse directly first
            return json.loads(text)
        except json.JSONDecodeError:
            # Common fix: Look for JSON between triple backticks
            import re
            match = re.search(r'```(?:json)?\n(.*?)\n```', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # If that fails, try to extract JSON object from the text
            try:
                # Look for the start of a JSON object
                start = text.find('{')
                end = text.rfind('}') + 1
                if start >= 0 and end > start:
                    return json.loads(text[start:end])
            except:
                pass
            
            raise ValueError("Failed to parse JSON response from LLM")

    def generate_math_variation(self, problem: str, variation_index: int = 0) -> Dict[str, Any]:
        """Generate a variation of a math problem while maintaining mathematical relationships
        
        Args:
            problem: The original problem text to generate a variation of
            variation_index: Index of the variation (for caching different variations)
            
        Returns:
            Dict with 'variation' (str) and 'explanation' (str)
        """
        # Create a unique cache key that includes the variation index
        problem_hash = f"{hash(problem)}_{variation_index}"
        cache_file = self._get_cache_path(problem_hash)
        
        # Check cache first - but only if we're not generating a new variation
        if variation_index == 0 and cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)

        # Check if this is a multi-part question
        is_multi_part = any(part.strip().startswith(('(i)', '(ii)', '(iii)', '(iv)', '(a)', '(b)', '1.', '2.', '3.')) 
                          for part in problem.split('\n') if part.strip())
        
        # Add some randomness to the prompt to encourage different variations
        import random
        temp_variations = [
            "Use different names and numbers while keeping the problem structure the same.",
            "Change the context slightly (e.g., different objects or scenario) but keep the math the same.",
            "Modify the numbers to make the problem slightly easier or harder, but still appropriate for grade 7.",
            "Use a different real-world context that would require the same mathematical operations to solve.",
            "Adjust the numbers to create a problem with a different but related mathematical relationship."
        ]
        random_instruction = random.choice(temp_variations)
        
        # Prepare instructions based on question type
        if is_multi_part:
            part_instruction = f"""
For this multi-part question:
1. Maintain the exact same structure and number of parts as the original
2. Keep the same labels (i, ii, etc.) for each part
3. Ensure all parts are mathematically consistent with each other
4. Each part should be solvable independently
5. {random_instruction}
"""
        else:
            part_instruction = f"The question has a single part. Make sure the variation is self-contained and complete. {random_instruction}"

        prompt = f"""You are an expert math teacher creating practice problems for 7th grade students. 
Create a variation of the following math problem that:
1. Has the same structure and requires the same mathematical concepts
2. Uses different numbers that maintain the same mathematical relationships
3. Is clear, concise, and appropriate for 7th grade students
4. Has a single, unambiguous answer for each part
5. Does not include any explanation or reasoning in the problem text
6. Is written in a way that would be appropriate to include directly in a worksheet

{part_instruction}

Original problem:
{problem}

Return a JSON object with:
- "variation": The new problem text (must be a single string with line breaks)
- "explanation": A brief explanation of the changes made (this is for teacher reference only)

Example 1 (Single part):
Original: "A car travels 450 km on 30 liters of petrol. How far will it travel on 50 liters?"
{{
  "variation": "A car travels 280 km on 20 liters of petrol. How far will it travel on 35 liters?",
  "explanation": "Maintained the direct proportion between distance and fuel with different numbers."
}}

Example 2 (Multi-part):
Original: "A test has 10 questions. Each correct answer scores 3 points, each wrong answer loses 1 point.\n(i) If a student gets 7 correct answers, what is their score?\n(ii) If another student scores 18 points, how many answers did they get correct?"
{{
  "variation": "A quiz has 15 questions. Each correct answer scores 4 points, each wrong answer loses 2 points.\n(i) If a student gets 10 correct answers, what is their score?\n(ii) If another student scores 30 points, how many answers did they get correct?",
  "explanation": "Maintained the scoring system structure with different numbers and point values."
}}

Now create a variation for this problem:
"""

        # Add the problem at the end to avoid confusing the model
        prompt += f'Original problem:\n{problem}\n\nVariation:'
        
        # Add temperature to increase randomness
        temperature = 0.8  # Higher temperature for more creative variations
        
        # Check if server is running
        if not self._check_server():
            print("❌ Ollama server not running. Please start it with:")
            print("   ollama serve")
            return {"variation": problem, "explanation": "Server not available"}

        # Try up to 3 times
        for attempt in range(3):
            try:
                # Add more context to ensure variations are different
                variation_context = (
                    f"Generate a UNIQUE variation #{variation_index + 1}. "
                    f"This should be different from any previous variations.\n"
                    f"{random_instruction}\n"
                    f"Be creative with the context and numbers while maintaining the same mathematical structure.\n"
                )
                
                randomized_prompt = f"{prompt}\n{variation_context}\n(Attempt {attempt + 1})\n\n"
                
                # Increase temperature for more diverse variations
                response = self._generate_with_llm(randomized_prompt, temperature=0.9)
                if not response:
                    raise ValueError("Empty response from LLM")
                    
                # Clean and validate the response
                cleaned_result = self._clean_json_response(response)
                
                # Validate required fields and basic quality
                if ("variation" in cleaned_result and 
                    "explanation" in cleaned_result and
                    len(cleaned_result["variation"].strip()) > 10 and  # Basic length check
                    any(c.isdigit() for c in cleaned_result["variation"])  # Should contain numbers
                ):
                    # Ensure variation is a string and clean it up
                    variation = str(cleaned_result["variation"]).strip()
                    
                    # Basic cleanup
                    variation = variation.replace('"', '').replace('\n', '\n').strip()
                    
                    # Cache the result
                    result = {
                        "variation": variation,
                        "explanation": str(cleaned_result["explanation"])
                    }
                    
                    with open(cache_file, 'w') as f:
                        json.dump(result, f, indent=2)
                    return result
                    
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                time.sleep(1)  # Wait before retry

        # Fallback: Return the original problem if all attempts fail
        return {
            "variation": problem, 
            "explanation": "Failed to generate valid variation after multiple attempts. Using original problem."
        }

        # Check if server is running
        if not self._check_server():
            print("❌ Ollama server not running. Please start it with:")
            print("   ollama serve")
            return {"variation": problem, "explanation": "Server not available"}

        # Try up to 3 times
        for attempt in range(3):
            try:
                result = self._generate_with_llm(prompt)
                # Clean and validate the response
                cleaned_result = self._clean_json_response(result)
                # Validate required fields
                if "variation" in cleaned_result and "explanation" in cleaned_result:
                    # Ensure variation is a string
                    if not isinstance(cleaned_result["variation"], str):
                        cleaned_result["variation"] = str(cleaned_result["variation"])
                    # Cache the result
                    with open(cache_file, 'w') as f:
                        json.dump(cleaned_result, f, indent=2)
                    return cleaned_result
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                time.sleep(1)  # Wait before retry

        # Fallback: Return the original problem if all attempts fail
        return {
            "variation": problem, 
            "explanation": "Failed to generate valid variation after multiple attempts. Using original problem."
        }

def test_math_variation():
    """Test the LLM integration with a sample math problem"""
    llm = LocalLLMGenerator()
    
    test_problems = [
        "A car travels 450 km on 30 liters of petrol. How far will it travel on 50 liters?",
        "If 5 workers can complete a project in 12 days, how many days will it take for 8 workers?",
        "A rectangle has a length to width ratio of 3:2. If the perimeter is 40 cm, what are its dimensions?"
    ]
    
    for problem in test_problems:
        print("\n" + "="*80)
        print("Original problem:")
        print(problem)
        
        variation = llm.generate_math_variation(problem)
        
        print("\nVariation:")
        print(variation["variation"])
        print("\nExplanation:")
        print(variation["explanation"])
        print("="*80 + "\n")

if __name__ == "__main__":
    test_math_variation()
