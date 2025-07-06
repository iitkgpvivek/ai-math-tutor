import random
from typing import Tuple, Dict, Any, Union
import math

class Grade7ProblemGenerator:
    def __init__(self):
        # Mapping of topics to their respective problem generators
        self.generators = {
            'Number System': {
                'Integers': self.generate_integer_problem,
                'Fractions and Decimals': self.generate_fraction_decimal_problem,
                'Rational Numbers': self.generate_fraction_decimal_problem
            },
            'Algebra': {
                'Simple Equations': self.generate_simple_equation,
                'Exponents and Powers': self.generate_exponent_problem
            },
            'Geometry': {
                'Lines and Angles': self.generate_lines_angles_problem,
                'Triangles': self.generate_triangle_problem,
                'Symmetry': self.generate_symmetry_problem
            },
            'Measurement': {
                'Perimeter and Area': self.generate_perimeter_area_problem
            },
            'Data Handling': {
                'Probability': self.generate_probability_problem
            }
        }
    
    def generate_problem(self, topic: str, subtopic: str, difficulty: str = 'medium') -> Tuple[str, Any]:
        """Generate a problem based on topic, subtopic, and difficulty."""
        print(f"DEBUG: Generating problem - Topic: {topic}, Subtopic: {subtopic}, Difficulty: {difficulty}")
        try:
            generator_func = self.generators[topic][subtopic]
            print(f"DEBUG: Found generator function: {generator_func.__name__}")
            result = generator_func(difficulty)
            print(f"DEBUG: Generator result: {result}")
            if result is None:
                print(f"ERROR: Generator function {generator_func.__name__} returned None")
            return result
        except KeyError as e:
            print(f"ERROR: Could not find generator for topic '{topic}' and subtopic '{subtopic}'")
            raise
    
    # Number System Problems
    def generate_integer_problem(self, difficulty: str) -> Tuple[str, Any]:
        """Generate integer problems with a strong focus on word problems from grade7_word_problems_clean."""
        # 70% chance of getting a word problem, 30% chance of other types
        if random.random() < 0.7:
            return self._generate_integer_word_problem(difficulty)
            
        # For the remaining 30%, distribute among other problem types
        problem_type = random.choices(
            ['basic_operation', 'number_line'],
            weights=[0.7, 0.3],
            k=1
        )[0]
        
        if problem_type == 'basic_operation':
            return self._generate_integer_operation(difficulty)
        else:  # number_line
            # If number line problems aren't implemented yet, default to word problem
            try:
                return self._generate_number_line_problem(difficulty)
            except (NotImplementedError, AttributeError):
                return self._generate_integer_word_problem(difficulty)
    
    def _generate_integer_word_problem(self, difficulty: str) -> Tuple[str, Union[int, str, float]]:
        """Generate word problems involving integers with appropriate difficulty."""
        # Import here to avoid circular imports
        from grade7_word_problems_clean import IntegerWordProblemGenerator
        
        # Create a new generator instance
        word_problem_generator = IntegerWordProblemGenerator()
        
        # Generate and return a problem
        return word_problem_generator.generate_problem(difficulty)
    
    # Other methods remain unchanged...
    # [Previous implementation of other methods...]
    
    def _generate_integer_operation(self, difficulty: str) -> Tuple[str, Any]:
        """Generate integer operation problems with varying difficulty.
        
        Args:
            difficulty: 'easy', 'medium', or 'hard'
            
        Returns:
            Tuple of (problem_statement, answer) or falls back to word problem
        """
        # Try to generate an operation problem, with multiple attempts
        for attempt in range(3):  # Try up to 3 times
            try:
                def get_operands(difficulty: str) -> Tuple[int, int]:
                    """Generate appropriate operands based on difficulty."""
                    if difficulty == 'easy':
                        return random.randint(1, 20), random.randint(1, 20)
                    elif difficulty == 'medium':
                        return random.randint(1, 50), random.randint(1, 20)
                    else:  # hard
                        return random.randint(-50, 50), random.randint(1, 50)
                
                def format_negative(num: int) -> str:
                    """Format negative numbers with parentheses."""
                    return f"({num})" if num < 0 else str(num)
                
                # Generate problem based on difficulty
                problem = ""
                answer = None
                
                if difficulty == 'easy':
                    ops = ['+', '-', '×']
                    op = random.choice(ops)
                    a, b = get_operands(difficulty)
                    
                    if op == '×':  # Avoid large products in easy mode
                        a, b = random.randint(1, 12), random.randint(1, 12)
                        
                    problem = f"Calculate: {a} {op} {b}"
                    
                elif difficulty == 'medium':
                    ops = ['+', '-', '×', '÷']
                    op = random.choice(ops)
                    a, b = get_operands(difficulty)
                    
                    # For division, ensure it's exact
                    if op == '÷':
                        b = random.randint(2, 12)
                        a = b * random.randint(1, 12)
                        
                    problem = f"Calculate: {a} {op} {b}"
                    
                else:  # hard
                    # 50% chance of mixed operations, 30% exponents, 20% division with remainder
                    choice = random.random()
                    
                    if choice < 0.5:  # Mixed operations
                        ops = ['+', '-', '×', '÷']
                        num_ops = random.randint(2, 3)
                        selected_ops = random.sample(ops, num_ops)
                        
                        # Generate numbers with appropriate ranges
                        nums = [random.randint(-20, 20) for _ in range(num_ops + 1)]
                        
                        # Build problem string
                        problem_parts = [f"{format_negative(nums[0])}"]
                        for i, op in enumerate(selected_ops):
                            problem_parts.append(f"{op} {format_negative(nums[i+1])}")
                            
                        problem = "Calculate: " + " ".join(problem_parts)
                        
                    elif choice < 0.8:  # Exponents
                        base = random.randint(-10, 10)
                        # Avoid very large numbers by limiting exponent
                        exp = random.randint(2, 4) if abs(base) > 5 else random.randint(2, 5)
                        problem = f"Calculate: {format_negative(base)}^{exp}"
                        
                    else:  # Division with remainder
                        b = random.randint(2, 20)
                        a = b * random.randint(2, 20) + random.randint(1, b-1)
                        problem = f"Calculate: {a} ÷ {b} (give quotient and remainder)"
                
                # If we don't have a problem, try again
                if not problem:
                    continue
                
                # Calculate answer
                try:
                    # Replace operators with Python equivalents
                    expr = problem.replace('Calculate: ', '')\
                                  .replace('×', '*')\
                                  .replace('÷', '//')
                                  
                    # Handle exponents
                    if '^' in expr:
                        base, exp = expr.split('^')
                        answer = eval(f"{base}**{exp}")
                    # Handle division with remainder
                    elif 'remainder' in problem:
                        a, b = [int(x) for x in expr.split('//')]
                        answer = f"quotient: {a//b}, remainder: {a%b}"
                    else:
                        answer = eval(expr)
                        
                    # If we have a valid problem and answer, return them
                    if problem and answer is not None:
                        return problem, answer
                        
                except Exception as e:
                    print(f"Error calculating answer for: {problem}")
                    print(f"Error: {e}")
                    continue
                    
            except Exception as e:
                print(f"Error generating integer operation: {e}")
                continue
        
        # If we've tried multiple times and still don't have a valid problem,
        # fall back to a word problem which is more reliable
        print("Falling back to word problem after operation generation failed")
        return self._generate_integer_word_problem(difficulty)
    
    def _generate_integer_property(self, difficulty: str) -> Tuple[str, Any]:
        """Generate questions about integer properties."""
        pass
    
    def _generate_number_line_problem(self, difficulty: str) -> Tuple[str, Any]:
        """Generate number line problems."""
        pass
    
    def _generate_integer_ordering(self, difficulty: str) -> Tuple[str, Any]:
        """Generate integer ordering problems."""
        pass
    
    def _generate_absolute_value_problem(self, difficulty: str) -> Tuple[str, Any]:
        """Generate absolute value problems."""
        pass
    
    def generate_fraction_decimal_problem(self, difficulty: str) -> Tuple[str, Any]:
        """Generate fraction and decimal problems."""
        problem_type = random.choice(['recipe', 'sharing'])
        
        if problem_type == 'recipe':
            return self._generate_recipe_problem(difficulty)
        else:  # sharing
            return self._generate_sharing_problem(difficulty)
    
    def _generate_recipe_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate recipe scaling problems."""
        ingredients = [
            ('sugar', 'cups'),
            ('flour', 'cups'),
            ('milk', 'cups'),
            ('butter', 'tablespoons'),
            ('eggs', '')
        ]
        ingredient, unit = random.choice(ingredients)
        
        if difficulty == 'easy':
            # Simple scaling with whole number multiples
            scale = random.randint(2, 4)
            amount = random.choice(['1/2', '1/3', '1/4', '1'])
            
            problem = f"A recipe calls for {amount} {unit} of {ingredient}. " \
                     f"How much {ingredient} is needed to make {scale} times the recipe?"
            
            # Calculate the answer using fractions for precision
            from fractions import Fraction
            if '/' in amount:
                num, den = map(int, amount.split('/'))
                frac = Fraction(num, den) * scale
            else:
                frac = Fraction(int(amount), 1) * scale
            
            if frac.denominator == 1:
                answer = f"{frac.numerator} {unit}" if unit else str(frac.numerator)
            else:
                answer = f"{frac.numerator}/{frac.denominator} {unit}".strip()
                
            return problem, answer
            
        elif difficulty == 'medium':
            # Scaling with mixed numbers
            whole = random.randint(1, 2)
            frac_part = random.choice(['1/2', '1/3', '1/4', '2/3', '3/4'])
            amount = f"{whole} {frac_part}"
            scale = random.randint(2, 3)
            
            problem = f"A recipe calls for {amount} {unit} of {ingredient}. " \
                     f"How much {ingredient} is needed to make {scale} times the recipe?"
            
            # Calculate using fractions
            from fractions import Fraction
            whole_num, frac = amount.split()
            num, den = map(int, frac.split('/'))
            total = (int(whole_num) + Fraction(num, den)) * scale
            
            # Convert to mixed number
            whole_part = total.numerator // total.denominator
            remainder = total.numerator % total.denominator
            
            if remainder == 0:
                answer = f"{whole_part} {unit}" if unit else str(whole_part)
            elif whole_part > 0:
                answer = f"{whole_part} {remainder}/{total.denominator} {unit}".strip()
            else:
                answer = f"{remainder}/{total.denominator} {unit}".strip()
                
            return problem, answer
            
        else:  # hard
            # Complex scaling with mixed number scaling factors
            whole = random.randint(1, 2)
            frac_part = random.choice(['1/2', '1/3', '2/3', '3/4'])
            amount = f"{whole} {frac_part}"
            
            scale_whole = random.randint(1, 2)
            scale_frac = random.choice(['1/2', '1/3', '2/3', '3/4'])
            
            problem = f"A recipe calls for {amount} {unit} of {ingredient}. " \
                     f"How much {ingredient} is needed to make {scale_whole} {scale_frac} times the recipe?"
            
            # Calculate using fractions
            from fractions import Fraction
            
            # Parse original amount
            whole_num, frac = amount.split()
            num, den = map(int, frac.split('/'))
            total_amount = (int(whole_num) + Fraction(num, den))
            
            # Parse scaling factor
            scale_num, scale_den = map(int, scale_frac.split('/'))
            scale = scale_whole + Fraction(scale_num, scale_den)
            
            # Calculate total
            result = total_amount * scale
            
            # Format answer
            whole_part = result.numerator // result.denominator
            remainder = result.numerator % result.denominator
            
            if remainder == 0:
                answer = f"{whole_part} {unit}" if unit else str(whole_part)
            elif whole_part > 0:
                answer = f"{whole_part} {remainder}/{result.denominator} {unit}".strip()
            else:
                answer = f"{remainder}/{result.denominator} {unit}".strip()
                
            return problem, answer

    def _generate_sharing_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate problems about sharing items fairly."""
        if difficulty == 'easy':
            # Simple sharing with whole numbers
            quantity = random.randint(10, 50)
            parts = random.choice([2, 4, 5, 10])
            problem = f"Divide {quantity} into {parts} equal parts. How many will each part have?"
            answer = f"{quantity // parts} (with {quantity % parts} remaining)" if quantity % parts != 0 else str(quantity // parts)
            return problem, answer
            
        elif difficulty == 'medium':
            # Fractional sharing with whole pizzas
            total = random.choice([1, 2, 3, 4, 5])
            people = random.choice([2, 3, 4, 5, 6])
            problem = f"If {total} pizzas are to be shared equally among {people} people, how much pizza will each person get?"
            
            # Simplify the fraction
            from fractions import Fraction
            frac = Fraction(total, people)
            
            if frac.denominator == 1:
                answer = f"{frac.numerator} whole pizza" + ("s" if frac.numerator > 1 else "")
            else:
                answer = f"{frac.numerator}/{frac.denominator} of a pizza"
                
            return problem, answer
            
        else:  # hard
            # Fractional sharing with different portions
            total = random.choice([3, 4, 5, 6])
            people = random.randint(4, 8)
            extra = random.randint(1, min(3, people - 1))  # At least 1 person gets double
            
            problem = f"{total} pizzas are shared among {people} people. If {extra} people get double portions, " \
                     f"how much will each of the remaining people get?"
            
            # Calculate portions
            total_portions = (people - extra) + (extra * 2)
            from fractions import Fraction
            portion = Fraction(total, total_portions)
            
            if portion.denominator == 1:
                answer = f"{portion.numerator} pizza" + ("s" if portion.numerator > 1 else "")
            else:
                answer = f"{portion.numerator}/{portion.denominator} of a pizza"
                
            return problem, answer
    
    def generate_simple_equation(self, difficulty: str) -> Tuple[str, Any]:
        """Generate simple equation problems."""
        pass
    
    def generate_exponent_problem(self, difficulty: str) -> Tuple[str, Any]:
        """Generate exponent problems."""
        pass
    
    def generate_lines_angles_problem(self, difficulty: str) -> Tuple[str, Any]:
        """Generate lines and angles problems."""
        pass
    
    def generate_triangle_problem(self, difficulty: str) -> Tuple[str, Any]:
        """Generate triangle problems."""
        pass
    
    def generate_symmetry_problem(self, difficulty: str) -> Tuple[str, Any]:
        """Generate symmetry problems."""
        pass
    
    def generate_perimeter_area_problem(self, difficulty: str) -> Tuple[str, Any]:
        """Generate perimeter and area problems."""
        pass
    
    def generate_probability_problem(self, difficulty: str) -> Tuple[str, Any]:
        """Generate probability problems."""
        pass
