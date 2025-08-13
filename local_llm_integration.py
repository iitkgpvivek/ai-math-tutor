import os
import re
import subprocess
import requests
import json
import time
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
    def __init__(self, model_name: str = "mistral", auto_start_server: bool = True, cache_dir: str = None):
        """Initialize the LLM generator.
        
        Args:
            model_name: Name of the model to use (must be pulled with Ollama, default is 'mistral')
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

    def _generate_with_llm(self, prompt: str, temperature: float = 0.7, timeout: int = 30) -> str:
        """Generate response using local LLM with enhanced mathematical reasoning
        
        Args:
            prompt: The prompt to send to the LLM
            temperature: Controls randomness (0.0 to 1.0, higher is more random)
            timeout: Maximum time in seconds to wait for the response
            
        Returns:
            str: The raw text response from the LLM
            
        Raises:
            TimeoutError: If the request takes longer than the specified timeout
            Exception: For other request/response errors
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
                timeout=timeout  # Use the specified timeout
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except requests.Timeout:
            raise TimeoutError(f"LLM request timed out after {timeout} seconds")
        except requests.RequestException as e:
            raise Exception(f"Error communicating with LLM: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error in LLM generation: {str(e)}")

    def _clean_json_response(self, text: str) -> Dict[str, Any]:
        """Clean and parse JSON response from LLM, handling various formatting issues.
        
        Args:
            text: Raw text response from the LLM
            
        Returns:
            Parsed JSON as a dictionary with 'variation' and 'explanation' keys
            
        Raises:
            ValueError: If the response cannot be parsed into valid JSON or is missing required fields
        """
        # Debug: Save the raw response for inspection
        debug_dir = os.path.join('debug', 'llm_responses')
        os.makedirs(debug_dir, exist_ok=True)
        timestamp = int(time.time())
        debug_prefix = os.path.join(debug_dir, f'llm_debug_{timestamp}')
        
        # Write raw response to file
        with open(f'{debug_prefix}_raw.txt', 'w', encoding='utf-8') as f:
            f.write(text)
            
        if not text or not text.strip() or text.strip() == '{}':
            with open(f'{debug_prefix}_error.txt', 'w', encoding='utf-8') as f:
                f.write("Empty or invalid response from LLM\n\n")
                f.write(f"Text length: {len(text) if text else 0}\n")
                if text:
                    f.write(f"Text content: {text}")
            raise ValueError("Empty or invalid response from LLM")
            
        # If we get an empty JSON object, raise an error
        text = text.strip()
        if text == '{}':
            with open(f'{debug_prefix}_error.txt', 'w', encoding='utf-8') as f:
                f.write("Empty JSON object received from LLM\n")
            raise ValueError("Empty JSON object received from LLM")
        
        original_text = text
        text = text.strip()
        
        def try_parse_json(json_str: str) -> Optional[Dict[str, Any]]:
            """Attempt to parse JSON with various cleaning strategies."""
            try:
                # First try direct parse
                result = json.loads(json_str)
                with open(f'{debug_prefix}_parse_success.txt', 'w', encoding='utf-8') as f:
                    f.write(f"Successfully parsed JSON:\n{json.dumps(result, indent=2)}\n")
                return result
            except json.JSONDecodeError:
                try:
                    # Try fixing common issues
                    cleaned = json_str
                    
                    # 1. Remove any text before the first {
                    cleaned = re.sub(r'^[^{]*', '', cleaned, 1, re.DOTALL)
                    
                    # 2. Remove any text after the last }
                    cleaned = re.sub(r'[^}]*$', '', cleaned, 0, re.DOTALL) + '}'
                    
                    # 3. Fix trailing commas in objects and arrays
                    cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)
                    
                    # 4. Fix missing quotes around keys
                    cleaned = re.sub(r'([{,}\s]\s*)([a-zA-Z0-9_]+)\s*:', 
                                  lambda m: f'{m.group(1)}"{m.group(2)}":', 
                                  cleaned)
                    
                    # 5. Fix single quotes to double quotes
                    cleaned = re.sub(r"'", '"', cleaned)
                    
                    # 6. Fix unescaped newlines in strings
                    cleaned = re.sub(r'(?<!\\)"\s*\n\s*"', '\\n', cleaned)
                    
                    # 7. Fix unescaped quotes in strings
                    cleaned = re.sub(r'(?<!\\)"(.*?)(?<!\\)"', 
                                  lambda m: f'"{m.group(1).replace("\"", "\\\"")}"', 
                                  cleaned)
                    
                    # 8. Fix boolean values
                    cleaned = re.sub(r':\s*true\b', ': true', cleaned, flags=re.IGNORECASE)
                    cleaned = re.sub(r':\s*false\b', ': false', cleaned, flags=re.IGNORECASE)
                    cleaned = re.sub(r':\s*null\b', ': null', cleaned, flags=re.IGNORECASE)
                    
                    # Try parsing the cleaned JSON
                    result = json.loads(cleaned)
                    with open(f'{debug_prefix}_parse_cleaned_success.txt', 'w', encoding='utf-8') as f:
                        f.write(f"Successfully parsed cleaned JSON:\n{json.dumps(result, indent=2)}\n")
                    return result
                    
                except (json.JSONDecodeError, Exception) as e:
                    with open(f'{debug_prefix}_parse_error.txt', 'w', encoding='utf-8') as f:
                        f.write(f"Error parsing JSON: {str(e)}\n")
                        f.write(f"JSON string that failed to parse:\n{cleaned}\n")
                    return None
        
        # Try different extraction patterns in order of preference
        extraction_patterns = [
            # 1. JSON in code blocks (```json or ```)
            r'```(?:json)?\s*\n({.*?})\s*```',
            # 2. JSON object with potential leading/trailing text
            r'({[\s\S]*?})\s*(?=\n\s*\{|$)',
            # 3. Any JSON-like structure with potential issues
            r'({[\s\S]*})',
        ]
        
        # Log extraction attempts
        with open(f'{debug_prefix}_extraction_attempts.txt', 'w', encoding='utf-8') as f:
            f.write(f"Original text length: {len(text)}\n")
            f.write("---\n")
            f.write(f"Text: {text}\n")
            f.write("---\n")
            f.write("Trying extraction patterns...\n")
        
        for i, pattern in enumerate(extraction_patterns, 1):
            with open(f'{debug_prefix}_extraction_attempts.txt', 'a', encoding='utf-8') as f:
                f.write(f"\n--- Pattern {i} ---\n")
                f.write(f"Pattern: {pattern}\n")
                
            match = re.search(pattern, text, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                with open(f'{debug_prefix}_extraction_attempts.txt', 'a', encoding='utf-8') as f:
                    f.write(f"Match found! Length: {len(json_str)}\n")
                    f.write(f"Matched text: {json_str[:200]}...\n" if len(json_str) > 200 else f"Matched text: {json_str}\n")
                
                result = try_parse_json(json_str)
                with open(f'{debug_prefix}_extraction_attempts.txt', 'a', encoding='utf-8') as f:
                    f.write(f"Parse result: {'Success' if result else 'Failed'}\n")
                    if result:
                        f.write(f"Result keys: {list(result.keys())}\n")
                if result:
                    # Validate required fields
                    if not isinstance(result, dict):
                        continue
                    
                    # Handle simple format with 'variation' and 'explanation' keys
                    if 'variation' in result and 'explanation' in result:
                        return {
                            'variation': str(result['variation']).strip(),
                            'explanation': str(result['explanation']).strip()
                        }
                    # Handle different response formats
                    elif 'problem' in result and 'solution' in result:
                        # Format: {"problem": {"expression": "...", "explanation": "..."}, "solution": {...}}
                        problem_text = result['problem'].get('expression', str(result['problem']))
                        explanation = result['solution'].get('explanation', 'No explanation provided')
                        return {
                            'variation': str(problem_text).strip(),
                            'explanation': str(explanation).strip()
                        }
                    # Try to find variation in nested structure
                    elif 'variation' not in result:
                        for key in ['variation', 'problem', 'question', 'text']:
                            if key in result:
                                result['variation'] = result[key]
                                break
                    
                    if 'explanation' not in result:
                        # Try to find explanation in nested structure
                        for key in ['explanation', 'reasoning', 'solution', 'hint']:
                            if key in result:
                                result['explanation'] = result[key]
                                break
                        else:
                            result['explanation'] = 'No explanation provided.'
                    
                    if 'variation' in result and 'explanation' in result:
                        return result
        
        # Try to parse the response as a structured problem
        try:
            # Try to parse as JSON again with more flexible handling
            try:
                data = json.loads(text)
                
                # Handle different response formats
                if isinstance(data, dict):
                    # Format 1: Direct variation/explanation
                    if 'variation' in data and 'explanation' in data:
                        return {
                            'variation': str(data['variation']).strip(),
                            'explanation': str(data.get('explanation', '')).strip()
                        }
                    # Format 2: Nested problem structure
                    elif 'problem' in data and isinstance(data['problem'], dict):
                        problem = data['problem']
                        variation = problem.get('question') or problem.get('problem') or problem.get('text', '')
                        explanation = problem.get('explanation') or problem.get('hint', 'No explanation provided')
                        return {
                            'variation': str(variation).strip(),
                            'explanation': str(explanation).strip()
                        }
                    # Format 3: Math problem with expression and explanation
                    elif 'math_problem' in data and isinstance(data['math_problem'], dict):
                        math_prob = data['math_problem']
                        expression = math_prob.get('expression', '')
                        explanation = math_prob.get('explanation', '')
                        if expression and explanation:
                            return {
                                'variation': f"Calculate: {expression}",
                                'explanation': explanation
                            }
                    # Format 4: Problem with nested explanation object
                    elif 'explanation' in data and isinstance(data.get('explanation'), dict):
                        explanation_obj = data['explanation']
                        if 'steps' in explanation_obj and isinstance(explanation_obj['steps'], list):
                            explanation = "\n".join(explanation_obj['steps'])
                            question = data.get('question', data.get('problem', 'Solve the following problem'))
                            return {
                                'variation': question,
                                'explanation': explanation
                            }
                    # Format 5: Equation with explanation
                    elif 'expression' in data and 'explanation' in data:
                        expression = data['expression']
                        explanation = data['explanation']
                        if '=' in expression:
                            left, right = expression.split('=', 1)
                            return {
                                'variation': f"Simplify and solve for the variables in: {expression}",
                                'explanation': f"Given the equation {expression}, here's how to solve it:\n\n{explanation}"
                            }
                        return {
                            'variation': f"Simplify: {expression}",
                            'explanation': explanation
                        }
                    # Format 6: Quadratic equation problem with detailed explanation
                    elif 'math_problem' in data and 'explanation' in data.get('math_problem', {}):
                        math_prob = data['math_problem']
                        problem = math_prob.get('problem', 'Solve the following equation')
                        explanation_data = math_prob.get('explanation', {})
                        
                        def format_explanation(explanation_dict, indent=0):
                            """Recursively format explanation dictionary into readable text."""
                            lines = []
                            for key, value in explanation_dict.items():
                                if key.startswith('step_') or key == 'quadratic_formula':
                                    if isinstance(value, dict):
                                        lines.append(f"{value.get('title', key).capitalize()}:")
                                        lines.extend(format_explanation(value, indent + 2))
                                    else:
                                        lines.append(' ' * indent + f"- {value}")
                                elif isinstance(value, dict):
                                    lines.append(' ' * indent + f"{key}:")
                                    lines.extend(format_explanation(value, indent + 2))
                                else:
                                    lines.append(' ' * indent + f"{key}: {value}")
                            return lines
                        
                        # Format the explanation
                        explanation_lines = format_explanation(explanation_data)
                        
                        return {
                            'variation': problem,
                            'explanation': '\n'.join(explanation_lines) or 'No explanation provided'
                        }
                    # Format 7: Geometry problem with formula and explanation
                    elif 'math_problem' in data and 'formula' in str(data.get('explanation', '')):
                        problem = data['math_problem'].get('problem', 'Solve the geometry problem')
                        explanation = data['math_problem'].get('explanation', 'No explanation provided')
                        
                        # Format the explanation to be more readable
                        if isinstance(explanation, str):
                            # Clean up the explanation text
                            explanation = '\n'.join(line.strip() for line in explanation.split('\n') if line.strip())
                        
                        return {
                            'variation': problem,
                            'explanation': f"Formula and Solution:\n{explanation}"
                        }
                    # Format 8: Arithmetic problem with operands and steps
                    elif 'problem' in data and 'operands' in data.get('problem', {}) and 'operation' in data.get('problem', {}):
                        problem_data = data['problem']
                        operands = problem_data['operands']
                        operation = problem_data['operation']
                        
                        # Create a human-readable problem
                        if operation == '+':
                            variation = f"What is {' + '.join(map(str, operands))}?"
                            op_name = 'addition'
                        elif operation == '-':
                            variation = f"What is {' - '.join(map(str, operands))}?"
                            op_name = 'subtraction'
                        elif operation == '*':
                            variation = f"What is {' × '.join(map(str, operands))}?"
                            op_name = 'multiplication'
                        elif operation == '/':
                            variation = f"What is {' ÷ '.join(map(str, operands))}?"
                            op_name = 'division'
                        else:
                            variation = f"Calculate: {' '.join(f"{op} {operation} " for op in operands).strip()}"
                            op_name = 'calculation'
                        
                        # Format the explanation
                        explanation = []
                        if 'explanation' in data and isinstance(data['explanation'], dict):
                            for step_num, step_text in sorted(data['explanation'].items()):
                                if step_num.startswith('step'):
                                    explanation.append(f"{step_num.capitalize()}: {step_text}")
                        
                        if not explanation:
                            explanation = [f"Perform {op_name} on the given numbers."]
                        
                        return {
                            'variation': variation,
                            'explanation': '\n'.join(explanation)
                        }
                    # Format 9: Addition problem with operation1 and operation2
                    elif 'problem' in data and 'operation1' in data.get('problem', {}) and 'operation2' in data.get('problem', {}):
                        problem_data = data['problem']
                        op1 = problem_data['operation1']
                        op2 = problem_data['operation2']
                        op_type = problem_data.get('type', 'addition').lower()
                        
                        # Create a human-readable problem
                        if 'add' in op_type.lower() or op_type.lower() == 'addition':
                            variation = f"What is {op1} + {op2}?"
                            op_symbol = '+'
                        elif 'subtract' in op_type.lower() or 'sub' in op_type.lower():
                            variation = f"What is {op1} - {op2}?"
                            op_symbol = '-'
                        elif 'multiply' in op_type.lower() or 'multiplication' in op_type.lower():
                            variation = f"What is {op1} × {op2}?"
                            op_symbol = '×'
                        elif 'divide' in op_type.lower() or 'division' in op_type.lower():
                            variation = f"What is {op1} ÷ {op2}?"
                            op_symbol = '÷'
                        else:
                            variation = f"Calculate: {op1} ? {op2}"
                            op_symbol = '?'
                        
                        # Format the explanation
                        explanation = []
                        if 'explanation' in data and isinstance(data['explanation'], dict):
                            for step_num, step_text in sorted(data['explanation'].items()):
                                if step_num.startswith('step_'):
                                    explanation.append(f"Step {step_num[5:]}: {step_text}")
                        
                        if not explanation and 'answer' in problem_data:
                            explanation = [f"The answer is {problem_data['answer']}."]
                        
                        return {
                            'variation': variation,
                            'explanation': '\n'.join(explanation) if explanation else f"Perform {op_type}: {op1} {op_symbol} {op2}"
                        }
                    # Format 10: Arithmetic problem with numbers and operation (legacy format)
                    elif all(key in data for key in ['num1', 'num2', 'operation']):
                        num1 = data['num1']
                        num2 = data['num2']
                        operation = data['operation'].lower()
                        explanation = data.get('explanation', '')
                        
                        # Create a human-readable problem
                        if operation == 'addition':
                            variation = f"What is {num1} + {num2}?"
                        elif operation == 'subtraction':
                            variation = f"What is {num1} - {num2}?"
                        elif operation == 'multiplication':
                            variation = f"What is {num1} × {num2}?"
                        elif operation == 'division':
                            variation = f"What is {num1} ÷ {num2}?"
                        else:
                            variation = f"Calculate: {num1} {operation} {num2}"
                        
                        return {
                            'variation': variation,
                            'explanation': explanation or f"To solve this {operation} problem, {num1} {operation} {num2} = {data.get('answer', '?')}"
                        }
                    # Format 3: Try to find any text that looks like a problem
                    else:
                        for key, value in data.items():
                            if isinstance(value, str) and ('?' in value or 'what' in value.lower() or 'how' in value.lower()):
                                return {
                                    'variation': str(value).strip(),
                                    'explanation': f'Extracted from {key} field (format may vary)'
                                }
            except json.JSONDecodeError:
                pass
                
            # Fallback to regex extraction if JSON parsing fails
            variation = None
            explanation = None
            
            # Look for common patterns in the response
            variation_match = re.search(r'(?i)(?:variation|problem|question)[\s:]*[\"\']?([^\{\}\n]+)', text)
            explanation_match = re.search(r'(?i)(?:explanation|hint|solution)[\s:]*[\"\']?([^\{\}\n]+)', text)
            
            if variation_match:
                variation = variation_match.group(1).strip('\"\' :')
            if explanation_match:
                explanation = explanation_match.group(1).strip('\"\' :')
            
            # If we found both, return them
            if variation and explanation:
                return {
                    'variation': variation,
                    'explanation': explanation
                }
            # If we only found the variation, use a default explanation
            elif variation:
                return {
                    'variation': variation,
                    'explanation': "Generated variation (no explanation provided)"
                }
                
        except Exception as e:
            # If extraction fails, continue to fallback
            pass
        
        # If all else fails, try to extract just the problem text
        try:
            # Look for anything that looks like a math problem
            problem_match = re.search(r'([A-Z].*\?[^\n]*)', text, re.DOTALL)
            if problem_match:
                return {
                    'variation': problem_match.group(1).strip(),
                    'explanation': 'Extracted problem from response (format may not be perfect)'
                }
        except:
            pass
            
        # If we get here, we couldn't parse the response
        error_msg = f"Could not parse LLM response. Response: {text[:200]}..."
        with open(f'{debug_prefix}_error.txt', 'w', encoding='utf-8') as f:
            f.write(error_msg + "\n")
            f.write("\n--- Full Response ---\n")
            f.write(text)
            f.write("\n--- End Response ---\n")
        raise ValueError(error_msg)
        raise ValueError("Could not parse LLM response. The response may not be in the expected format.")

    def _generate_math_variation_prompt(self, problem: str) -> str:
        """Generate the prompt for creating a math problem variation.
        
        Args:
            problem: The original problem text to generate a variation of
            
        Returns:
            Formatted prompt string
        """
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

        prompt = f"""You are an expert math teacher creating practice problems for 7th grade students following the CBSE curriculum.

INSTRUCTIONS:
1. Create a variation of the given math problem that maintains the same mathematical structure and concepts
2. Use different numbers while preserving the mathematical relationships
3. Ensure the problem is clear, concise, and appropriate for 7th grade students
4. Include all necessary information to solve the problem
5. Make sure the problem ends with a clear question mark
6. Follow the exact JSON format specified below

{part_instruction}

REQUIRED FORMAT (STRICT JSON):
{{
  "variation": "The new problem text with line breaks as needed",
  "explanation": "Brief explanation of the changes made"
}}

RULES:
- The response MUST be valid JSON
- Escape all special characters in strings (e.g., newlines as \\n, quotes as \")
- Do not include any text outside the JSON object
- The variation must be a complete, self-contained problem
- The explanation should be brief and focus on the mathematical changes

EXAMPLES:

Single-part problem:
Original: "A car travels 450 km on 30 liters of petrol. How far will it travel on 50 liters?"
{{
  "variation": "A car travels 280 km on 20 liters of petrol. How far will it travel on 35 liters?",
  "explanation": "Maintained the direct proportion between distance and fuel (14 km/L). Changed values while keeping the same mathematical relationship."
}}

Multi-part problem:
Original: "A test has 10 questions. Each correct answer scores 3 points, each wrong answer loses 1 point.\n(i) If a student gets 7 correct answers, what is their score?\n(ii) If another student scores 18 points, how many answers did they get correct?"
{{
  "variation": "A quiz has 15 questions. Each correct answer scores 4 points, each wrong answer loses 2 points.\n(i) If a student gets 10 correct answers, what is their score?\n(ii) If another student scores 30 points, how many answers did they get correct?",
  "explanation": "Maintained the scoring system structure. Changed point values and question counts while keeping the same problem-solving approach."
}}

Now create a variation for this problem:
"""
        # Add the problem at the end to avoid confusing the model
        prompt += f'Original problem:\n{problem}\n\nVariation:'
        return prompt

    def generate_math_variation(self, problem: str, variation_index: int = 0, max_attempts: int = 3, timeout_per_attempt: int = 30) -> Dict[str, Any]:
        """Generate a variation of a math problem while maintaining mathematical relationships
        
        Args:
            problem: The original problem text to generate a variation of
            variation_index: Index of the variation (for caching different variations)
            max_attempts: Maximum number of generation attempts
            timeout_per_attempt: Timeout in seconds for each LLM request
            
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

        prompt = f"""You are an expert math teacher creating practice problems for 7th grade students following the CBSE curriculum.

INSTRUCTIONS:
1. Create a variation of the given math problem that maintains the same mathematical structure and concepts
2. Use different numbers while preserving the mathematical relationships
3. Ensure the problem is clear, concise, and appropriate for 7th grade students
4. Include all necessary information to solve the problem
5. Make sure the problem ends with a clear question mark
6. Follow the exact JSON format specified below

{part_instruction}

REQUIRED FORMAT (STRICT JSON):
{{
  "variation": "The new problem text with line breaks as needed",
  "explanation": "Brief explanation of the changes made"
}}

RULES:
- The response MUST be valid JSON
- Escape all special characters in strings (e.g., newlines as \\n, quotes as \")
- Do not include any text outside the JSON object
- The variation must be a complete, self-contained problem
- The explanation should be brief and focus on the mathematical changes

EXAMPLES:

Single-part problem:
Original: "A car travels 450 km on 30 liters of petrol. How far will it travel on 50 liters?"
{{
  "variation": "A car travels 280 km on 20 liters of petrol. How far will it travel on 35 liters?",
  "explanation": "Maintained the direct proportion between distance and fuel (14 km/L). Changed values while keeping the same mathematical relationship."
}}

Multi-part problem:
Original: "A test has 10 questions. Each correct answer scores 3 points, each wrong answer loses 1 point.\n(i) If a student gets 7 correct answers, what is their score?\n(ii) If another student scores 18 points, how many answers did they get correct?"
{{
  "variation": "A quiz has 15 questions. Each correct answer scores 4 points, each wrong answer loses 2 points.\n(i) If a student gets 10 correct answers, what is their score?\n(ii) If another student scores 30 points, how many answers did they get correct?",
  "explanation": "Maintained the scoring system structure. Changed point values and question counts while keeping the same problem-solving approach."
}}

Now create a variation for this problem:
"""

        # Add the problem at the end to avoid confusing the model
        prompt += f'Original problem:\n{problem}\n\nVariation:'
        
        # Check if server is running
        if not self._check_server():
            print("❌ Ollama server not running. Please start it with:")
            print("   ollama serve")
            return {"variation": problem, "explanation": "Server not available"}

        # Try up to max_attempts times
        for attempt in range(max_attempts):
            start_time = time.time()
            try:
                # Add more context to ensure variations are different
                variation_context = (
                    f"Generate a UNIQUE variation #{variation_index + 1}. "
                    f"This should be different from any previous variations.\n"
                    f"{random_instruction}\n"
                    f"Be creative with the context and numbers while maintaining the same mathematical structure.\n"
                )
                
                randomized_prompt = f"{prompt}\n{variation_context}\n(Attempt {attempt + 1}/{max_attempts})\n\n"
                
                # Calculate remaining time for this attempt
                elapsed = time.time() - start_time
                remaining_time = max(5, timeout_per_attempt - elapsed)  # Minimum 5 seconds
                
                # Generate with LLM
                response = self._generate_with_llm(
                    randomized_prompt, 
                    temperature=0.8,
                    timeout=remaining_time
                )
                
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
                    
            except TimeoutError as te:
                print(f"⏱️  Attempt {attempt + 1} timed out after {timeout_per_attempt} seconds")
                if attempt == max_attempts - 1:
                    print("Maximum attempts reached. Using fallback variation.")
            except Exception as e:
                print(f"⚠️  Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_attempts - 1:
                    print("Maximum attempts reached. Using fallback variation.")
            
            # Small delay before next attempt
            time.sleep(1)

        # Fallback: Return the original problem if all attempts fail
        return {
            "variation": problem, 
            "explanation": f"Failed to generate valid variation after {max_attempts} attempts. Using original problem."
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
        
        # Get the prompt that would be sent to the LLM
        prompt = llm._generate_math_variation_prompt(problem)
        print("\nPrompt sent to LLM:")
        print("-"*40)
        print(prompt)
        print("-"*40)
        
        # Get the raw response from the LLM
        try:
            raw_response = llm._generate_with_llm(prompt, temperature=0.7, timeout=30)
            print("\nRaw LLM response:")
            print("-"*40)
            print(raw_response)
            print("-"*40)
            
            # Try to parse the response
            try:
                parsed = json.loads(raw_response)
                print("\nParsed JSON response:")
                print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError as e:
                print(f"\n⚠️ Failed to parse JSON: {e}")
                
        except Exception as e:
            print(f"\n⚠️ Error getting LLM response: {e}")
            continue
        
        variation = llm.generate_math_variation(problem)
        
        print("\nVariation:")
        print(variation["variation"])
        print("\nExplanation:")
        print(variation["explanation"])
        print("="*80 + "\n")

if __name__ == "__main__":
    test_math_variation()
