from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')
CORS(app)

# Ensure data directory exists
DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)

# Import problem generator
from grade7_problems import Grade7ProblemGenerator
problem_generator = Grade7ProblemGenerator()

@app.route('/')
def home():
    """Render the main web interface."""
    return render_template('index.html')

@app.route('/api/problem', methods=['GET'])
def get_problem():
    """API endpoint to get a new math problem."""
    topic = request.args.get('topic', 'fractions')
    difficulty = request.args.get('difficulty', 'medium')
    
    try:
        # Map frontend topic names to generator methods
        if topic == 'fractions':
            problem, answer = problem_generator.generate_fraction_decimal_problem(difficulty)
        elif topic == 'rational':
            problem, answer = problem_generator.generate_rational_number_problem(difficulty)
        else:
            # Default to fractions if unknown topic
            problem, answer = problem_generator.generate_fraction_decimal_problem(difficulty)
            
        return jsonify({
            'success': True,
            'problem': problem,
            'answer': str(answer),
            'topic': topic,
            'difficulty': difficulty
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def parse_fraction(frac_str):
    """Parse a fraction string into numerator and denominator."""
    if '/' in frac_str:
        try:
            num, denom = frac_str.split('/')
            return int(num.strip()), int(denom.strip())
        except (ValueError, AttributeError):
            return None
    return None

def compare_fractions(frac1, frac2):
    """Compare two fraction strings by cross-multiplying."""
    if frac1 == frac2:
        return True
        
    # Try to parse as fractions
    f1 = parse_fraction(frac1)
    f2 = parse_fraction(frac2)
    
    if f1 and f2:
        # Cross-multiply to compare fractions without floating point
        return f1[0] * f2[1] == f1[1] * f2[0]
        
    return False

@app.route('/api/submit', methods=['POST'])
def submit_answer():
    data = request.json
    problem = data.get('problem')
    user_answer = data.get('userAnswer', '').strip()
    correct_answer = data.get('correctAnswer')
    topic = data.get('topic')
    difficulty = data.get('difficulty')
    
    print(f"Received submission - Problem: {problem}, User answer: '{user_answer}', Correct answer: '{correct_answer}'")
    
    def are_answers_equivalent(user_ans, correct_ans):
        """Check if the user's answer is equivalent to the correct answer."""
        # Normalize both answers to strings and remove any whitespace
        user_ans = str(user_ans).strip().replace(' ', '')
        correct_ans = str(correct_ans).strip().replace(' ', '')
        
        # 1. Check exact match first (including equivalent fraction forms)
        if user_ans == correct_ans:
            return True
            
        # 2. Try to parse as fractions and compare
        user_frac = parse_fraction(user_ans)
        correct_frac = parse_fraction(correct_ans)
        
        if user_frac is not None and correct_frac is not None:
            # Cross-multiply to check fraction equivalence: a/b = c/d if a*d = b*c
            a, b = user_frac
            c, d = correct_frac
            if a * d == b * c:
                return True
        
        # 3. Try to parse as decimals and compare with tolerance
        user_dec = parse_decimal(user_ans)
        correct_dec = parse_decimal(correct_ans)
        
        if user_dec is not None and correct_dec is not None:
            # Calculate relative error
            if correct_dec == 0:
                is_close = abs(user_dec) < 0.01  # Special case for zero
            else:
                # Use relative tolerance for larger numbers, absolute for small numbers
                rel_tolerance = 0.01  # 1% relative error allowed
                abs_tolerance = 0.01  # Absolute error for small numbers
                diff = abs(user_dec - correct_dec)
                is_close = (diff <= abs_tolerance or 
                           diff / abs(correct_dec) <= rel_tolerance)
            
            if is_close:
                return True
        
        # 4. Compare fraction to decimal
        if user_frac is not None and correct_dec is not None:
            user_dec_from_frac = user_frac[0] / user_frac[1]
            if abs(user_dec_from_frac - correct_dec) < 0.01:
                return True
                
        if correct_frac is not None and user_dec is not None:
            correct_dec_from_frac = correct_frac[0] / correct_frac[1]
            if abs(correct_dec_from_frac - user_dec) < 0.01:
                return True
                
        return False
    
    def parse_fraction(s):
        """Parse a string into a fraction (numerator, denominator) or return None if not a fraction."""
        try:
            # Handle mixed numbers like '1 1/2' or '-1 1/2'
            parts = s.replace('+', '').replace('-', ' -').strip().split()
            if len(parts) == 2 and '/' in parts[1]:
                # Mixed number like '1 1/2' or '-1 1/2'
                whole = int(parts[0])
                num, denom = map(int, parts[1].split('/'))
                if whole < 0:
                    num = whole * denom - num
                else:
                    num = whole * denom + num
                return (num, denom) if denom > 0 else None
            
            # Handle simple fractions like '1/2' or '-3/4'
            if '/' in s:
                num, denom = map(int, s.split('/'))
                return (num, denom) if denom != 0 else None
                
            return None
        except (ValueError, IndexError):
            return None
    
    def parse_decimal(s):
        """Parse a string into a float or return None if not a valid decimal."""
        try:
            # Handle decimal points and commas, with or without leading zero
            s = s.replace(',', '.').lstrip('+').replace(' ', '')
            if s.startswith('.'):
                s = '0' + s
            if s.endswith('.'):
                s = s + '0'
            return float(s)
        except (ValueError, AttributeError):
            return None
    
    try:
        # Check if answers are equivalent using our comparison function
        if are_answers_equivalent(user_answer, correct_answer):
            return jsonify({
                'success': True,
                'is_correct': True,
                'correct_answer': str(correct_answer)
            })
        
        # If we get here, the answer is incorrect
        return jsonify({
            'success': True,
            'is_correct': False,
            'correct_answer': str(correct_answer)
        })
        
    except Exception as e:
        print(f"Error checking answer: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'An error occurred while checking the answer: {str(e)}'
        }), 500

def log_attempt(attempt_data):
    """Log a problem attempt to a JSON file."""
    log_file = DATA_DIR / 'attempts.json'
    
    # Load existing attempts or create new list
    if log_file.exists():
        with open(log_file, 'r') as f:
            try:
                attempts = json.load(f)
            except json.JSONDecodeError:
                attempts = []
    else:
        attempts = []
    
    # Add new attempt
    attempts.append(attempt_data)
    
    # Save back to file
    with open(log_file, 'w') as f:
        json.dump(attempts, f, indent=2)

# Serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
