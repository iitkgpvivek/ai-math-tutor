"""
Fraction Word Problem Generators for Grade 7 Math Worksheets

This module provides a comprehensive set of fraction word problem generators
that can be used to create math worksheets with varying difficulty levels.
"""

import random
import math
from fractions import Fraction
from typing import Tuple, Union, List, Dict, Any

class FractionWordProblemGenerator:
    """
    A class to generate fraction word problems with varying difficulty levels.
    """
    
    def __init__(self):
        """Initialize the fraction word problem generator."""
        self.ingredients = [
            ('sugar', 'cups'),
            ('flour', 'cups'),
            ('milk', 'cups'),
            ('butter', 'tablespoons'),
            ('eggs', '')
        ]
        
        self.food_items = [
            'pizza', 'cake', 'sandwich', 'soup', 'salad',
            'pasta', 'stew', 'casserole', 'smoothie', 'juice'
        ]
        
        self.measurements = [
            ('cup', 'cups'),
            ('tablespoon', 'tablespoons'),
            ('teaspoon', 'teaspoons'),
            ('pound', 'pounds'),
            ('ounce', 'ounces'),
            ('liter', 'liters'),
            ('milliliter', 'milliliters'),
            ('gram', 'grams'),
            ('kilogram', 'kilograms')
        ]
    
    def generate_problem(self, problem_type: str = None, difficulty: str = 'medium') -> Tuple[str, Union[str, int, float]]:
        """
        Generate a fraction word problem.
        
        Args:
            problem_type: Type of problem to generate. If None, a random type is selected.
            difficulty: Difficulty level ('easy', 'medium', 'hard').
            
        Returns:
            A tuple containing (problem_text, answer)
        """
        if problem_type is None:
            problem_type = random.choice([
                'recipe_scaling',
                'sharing',
                'addition',
                'subtraction',
                'multiplication',
                'division',
                'comparison',
                'conversion',
                'mixed_operations',
                'measurement'
            ])
        
        if problem_type == 'recipe_scaling':
            return self._generate_recipe_problem(difficulty)
        elif problem_type == 'sharing':
            return self._generate_sharing_problem(difficulty)
        elif problem_type == 'addition':
            return self._generate_addition_problem(difficulty)
        elif problem_type == 'subtraction':
            return self._generate_subtraction_problem(difficulty)
        elif problem_type == 'multiplication':
            return self._generate_multiplication_problem(difficulty)
        elif problem_type == 'division':
            return self._generate_division_problem(difficulty)
        elif problem_type == 'comparison':
            return self._generate_comparison_problem(difficulty)
        elif problem_type == 'conversion':
            return self._generate_conversion_problem(difficulty)
        elif problem_type == 'mixed_operations':
            return self._generate_mixed_operations_problem(difficulty)
        elif problem_type == 'measurement':
            return self._generate_measurement_problem(difficulty)
        else:
            raise ValueError(f"Unknown problem type: {problem_type}")
    
    def _generate_fraction(self, max_denominator: int = 12, allow_mixed: bool = False) -> str:
        """Generate a random fraction or mixed number."""
        denominator = random.randint(2, max_denominator)
        numerator = random.randint(1, denominator - 1)
        
        if not allow_mixed or random.random() < 0.7:  # 70% chance of simple fraction
            return f"{numerator}/{denominator}"
        else:
            whole = random.randint(1, 5)
            return f"{whole} {numerator}/{denominator}"
    
    def _generate_recipe_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate recipe scaling problems."""
        ingredient, unit = random.choice(self.ingredients)
        
        if difficulty == 'easy':
            # Simple scaling with whole number multiples
            scale = random.randint(2, 4)
            amount = random.choice(['1/2', '1/3', '1/4', '1'])
            
            problem = f"A recipe calls for {amount} {unit} of {ingredient}. " \
                     f"If you want to make {scale} times the recipe, how much {ingredient} do you need?"
            
            # Calculate answer
            if '/' in amount:
                num, denom = map(int, amount.split('/'))
                total = Fraction(num, denom) * scale
            else:
                total = Fraction(int(amount)) * scale
            
            answer = f"{total.numerator // total.denominator}" if total.denominator == 1 else f"{total.numerator}/{total.denominator}"
            answer += f" {unit}" if unit else ""
            
            return problem, answer
            
        elif difficulty == 'medium':
            # Scaling with mixed numbers
            scale_whole = random.randint(1, 3)
            scale_frac = random.choice(['1/2', '1/3', '1/4', '2/3', '3/4'])
            amount = self._generate_fraction(allow_mixed=True)
            
            problem = f"A recipe requires {amount} {unit} of {ingredient}. " \
                     f"If you want to make {scale_whole} {scale_frac} times the recipe, how much {ingredient} do you need?"
            
            # Parse amount
            if ' ' in amount:
                whole, frac = amount.split()
                whole = int(whole)
                num, denom = map(int, frac.split('/'))
                amount_frac = whole + Fraction(num, denom)
            else:
                num, denom = map(int, amount.split('/'))
                amount_frac = Fraction(num, denom)
            
            # Parse scale
            scale_num, scale_den = map(int, scale_frac.split('/'))
            scale = scale_whole + Fraction(scale_num, scale_den)
            
            # Calculate total
            total = amount_frac * scale
            
            # Format answer
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
            # Complex recipe with multiple ingredients and scaling
            num_ingredients = random.randint(2, 4)
            selected_ingredients = random.sample(self.ingredients, num_ingredients)
            
            # Original amounts
            original_amounts = {}
            for ing, unit in selected_ingredients:
                if random.random() < 0.5:  # 50% chance for simple fraction
                    amount = self._generate_fraction()
                else:  # 50% chance for mixed number
                    amount = f"{random.randint(1, 3)} {self._generate_fraction()}"
                original_amounts[(ing, unit)] = amount
            
            # Scaling factor
            scale_whole = random.randint(2, 5)
            scale_frac = random.choice(['1/2', '1/3', '2/3', '3/4'])
            scale_num, scale_den = map(int, scale_frac.split('/'))
            scale = scale_whole + Fraction(scale_num, scale_den)
            
            # Build problem
            problem = "A recipe has the following ingredients:\n"
            for (ing, unit), amount in original_amounts.items():
                problem += f"- {amount} {unit} {ing}\n"
            problem += f"\nIf you want to make {scale_whole} {scale_frac} times the recipe, "
            problem += "how much of each ingredient will you need?"
            
            # Calculate answers
            answers = []
            for (ing, unit), amount in original_amounts.items():
                # Parse original amount
                if ' ' in amount:
                    whole, frac = amount.split()
                    whole = int(whole)
                    num, denom = map(int, frac.split('/'))
                    amount_frac = whole + Fraction(num, denom)
                else:
                    num, denom = map(int, amount.split('/'))
                    amount_frac = Fraction(num, denom)
                
                # Calculate scaled amount
                total = amount_frac * scale
                
                # Format answer
                whole_part = total.numerator // total.denominator
                remainder = total.numerator % total.denominator
                
                if remainder == 0:
                    answer = f"{whole_part} {unit} {ing}" if unit else f"{whole_part} {ing}"
                elif whole_part > 0:
                    answer = f"{whole_part} {remainder}/{total.denominator} {unit} {ing}".strip()
                else:
                    answer = f"{remainder}/{total.denominator} {unit} {ing}".strip()
                
                answers.append(answer)
            
            return problem, "\n".join(answers)
    
    def _generate_sharing_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate problems about sharing items fairly."""
        if difficulty == 'easy':
            # Simple sharing with whole numbers
            quantity = random.randint(10, 50)
            parts = random.choice([2, 4, 5, 10])
            problem = f"Divide {quantity} {random.choice(self.food_items)} equally among {parts} people. " \
                     f"How much will each person get?"
            answer = f"{quantity // parts} (with {quantity % parts} remaining)" if quantity % parts != 0 else str(quantity // parts)
            return problem, answer
            
        elif difficulty == 'medium':
            # Fractional sharing with whole pizzas
            total = random.choice([1, 2, 3, 4, 5])
            people = random.choice([3, 4, 6, 8])
            
            problem = f"Share {total} {random.choice(self.food_items)} equally among {people} people. " \
                     f"How much will each person get?"
            
            # Calculate answer
            from fractions import Fraction
            portion = Fraction(total, people)
            
            if portion.denominator == 1:
                answer = f"{portion.numerator} {self.food_items[0]}"
            else:
                answer = f"{portion.numerator}/{portion.denominator} of a {self.food_items[0]}"
                
            return problem, answer
            
        else:  # hard
            # Unequal sharing with mixed numbers
            total = random.choice([2, 3, 4, 5])
            people = random.choice([3, 4, 5, 6])
            extra = random.randint(1, people-1)
            
            problem = f"{total} {random.choice(self.food_items)} are shared among {people} people. " \
                     f"If {extra} people get double portions, how much will each of the remaining people get?"
            
            # Calculate portions
            total_portions = (people - extra) + (extra * 2)
            from fractions import Fraction
            portion = Fraction(total, total_portions)
            
            if portion.denominator == 1:
                answer = f"{portion.numerator} {self.food_items[0]}s"
            else:
                answer = f"{portion.numerator}/{portion.denominator} of a {self.food_items[0]}"
                
            return problem, answer
    
    def _generate_addition_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate fraction addition problems."""
        if difficulty == 'easy':
            # Simple addition with like denominators
            denom = random.randint(2, 12)
            num1 = random.randint(1, denom-1)
            num2 = random.randint(1, denom-1)
            
            problem = f"Add: {num1}/{denom} + {num2}/{denom}"
            result = Fraction(num1 + num2, denom)
            answer = self._format_fraction(result)
            return problem, answer
            
        elif difficulty == 'medium':
            # Addition with unlike denominators (one needs conversion)
            denom1 = random.choice([2, 3, 4, 6, 8, 12])
            denom2 = denom1 * random.choice([2, 3, 4])
            num1 = random.randint(1, denom1-1)
            num2 = random.randint(1, denom2-1)
            
            problem = f"Add: {num1}/{denom1} + {num2}/{denom2}"
            result = Fraction(num1, denom1) + Fraction(num2, denom2)
            answer = self._format_fraction(result)
            return problem, answer
            
        else:  # hard
            # Mixed numbers with unlike denominators
            whole1 = random.randint(1, 3)
            whole2 = random.randint(1, 3)
            denom1 = random.choice([3, 4, 5, 6, 8, 12])
            denom2 = random.choice([3, 4, 5, 6, 8, 12])
            num1 = random.randint(1, denom1-1)
            num2 = random.randint(1, denom2-1)
            
            problem = f"Add: {whole1} {num1}/{denom1} + {whole2} {num2}/{denom2}"
            result = (whole1 + whole2) + Fraction(num1, denom1) + Fraction(num2, denom2)
            answer = self._format_fraction(result, mixed=True)
            return problem, answer
    
    def _generate_subtraction_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate fraction subtraction problems."""
        if difficulty == 'easy':
            # Simple subtraction with like denominators (first fraction larger)
            denom = random.randint(2, 12)
            num1 = random.randint(2, denom-1)
            num2 = random.randint(1, num1-1)
            
            problem = f"Subtract: {num1}/{denom} - {num2}/{denom}"
            result = Fraction(num1 - num2, denom)
            answer = self._format_fraction(result)
            return problem, answer
            
        elif difficulty == 'medium':
            # Subtraction with unlike denominators (no borrowing)
            denom1 = random.choice([2, 3, 4, 6, 8, 12])
            denom2 = denom1 * random.choice([2, 3, 4])
            num1 = random.randint(1, denom1-1)
            num2 = random.randint(1, denom2-1)
            
            # Ensure first fraction is larger
            if Fraction(num1, denom1) <= Fraction(num2, denom2):
                num1, num2 = num2, num1
                denom1, denom2 = denom2, denom1
            
            problem = f"Subtract: {num1}/{denom1} - {num2}/{denom2}"
            result = Fraction(num1, denom1) - Fraction(num2, denom2)
            answer = self._format_fraction(result)
            return problem, answer
            
        else:  # hard
            # Mixed numbers with borrowing
            whole1 = random.randint(2, 5)
            whole2 = random.randint(1, whole1-1)
            denom1 = random.choice([3, 4, 5, 6, 8, 12])
            denom2 = random.choice([3, 4, 5, 6, 8, 12])
            num1 = random.randint(1, denom1-1)
            num2 = random.randint(1, denom2-1)
            
            # Ensure first number is larger
            first = whole1 + Fraction(num1, denom1)
            second = whole2 + Fraction(num2, denom2)
            if first <= second:
                whole1, whole2 = whole2, whole1
                denom1, denom2 = denom2, denom1
                num1, num2 = num2, num1
            
            problem = f"Subtract: {whole1} {num1}/{denom1} - {whole2} {num2}/{denom2}"
            result = (whole1 - whole2) + Fraction(num1, denom1) - Fraction(num2, denom2)
            answer = self._format_fraction(result, mixed=True)
            return problem, answer
    
    def _generate_multiplication_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate fraction multiplication problems."""
        if difficulty == 'easy':
            # Simple multiplication of two proper fractions
            denom1 = random.randint(2, 12)
            denom2 = random.randint(2, 12)
            num1 = random.randint(1, denom1-1)
            num2 = random.randint(1, denom2-1)
            
            problem = f"Multiply: {num1}/{denom1} × {num2}/{denom2}"
            result = Fraction(num1 * num2, denom1 * denom2)
            answer = self._format_fraction(result)
            return problem, answer
            
        elif difficulty == 'medium':
            # Multiplication with mixed numbers
            whole1 = random.randint(1, 3)
            whole2 = random.randint(1, 3)
            denom1 = random.randint(2, 12)
            denom2 = random.randint(2, 12)
            num1 = random.randint(1, denom1-1)
            num2 = random.randint(1, denom2-1)
            
            problem = f"Multiply: {whole1} {num1}/{denom1} × {whole2} {num2}/{denom2}"
            frac1 = whole1 + Fraction(num1, denom1)
            frac2 = whole2 + Fraction(num2, denom2)
            result = frac1 * frac2
            answer = self._format_fraction(result, mixed=True)
            return problem, answer
            
        else:  # hard
            # Multiplication with simplification
            # Create fractions that will simplify nicely
            factors = [2, 2, 2, 3, 3, 5, 7, 11]
            random.shuffle(factors)
            
            # Split factors into four groups for cross-canceling
            num1_factors = factors[:2]
            denom1_factors = factors[2:4]
            num2_factors = factors[4:6]
            denom2_factors = factors[6:]
            
            num1 = math.prod(num1_factors)
            denom1 = math.prod(denom1_factors)
            num2 = math.prod(num2_factors)
            denom2 = math.prod(denom2_factors)
            
            problem = f"Multiply and simplify: {num1}/{denom1} × {num2}/{denom2}"
            result = Fraction(num1 * num2, denom1 * denom2)
            answer = self._format_fraction(result, mixed=True)
            return problem, answer
    
    def _generate_division_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate fraction division problems."""
        if difficulty == 'easy':
            # Simple division of two proper fractions
            denom1 = random.randint(2, 12)
            denom2 = random.randint(2, 12)
            num1 = random.randint(1, denom1-1)
            num2 = random.randint(1, denom2-1)
            
            problem = f"Divide: {num1}/{denom1} ÷ {num2}/{denom2}"
            result = Fraction(num1 * denom2, denom1 * num2)
            answer = self._format_fraction(result)
            return problem, answer
            
        elif difficulty == 'medium':
            # Division with mixed numbers
            whole1 = random.randint(1, 3)
            whole2 = random.randint(1, 3)
            denom1 = random.randint(2, 12)
            denom2 = random.randint(2, 12)
            num1 = random.randint(1, denom1-1)
            num2 = random.randint(1, denom2-1)
            
            problem = f"Divide: {whole1} {num1}/{denom1} ÷ {whole2} {num2}/{denom2}"
            frac1 = whole1 + Fraction(num1, denom1)
            frac2 = whole2 + Fraction(num2, denom2)
            result = frac1 / frac2
            answer = self._format_fraction(result, mixed=True)
            return problem, answer
            
        else:  # hard
            # Division with simplification
            # Create fractions that will simplify nicely
            factors = [2, 2, 2, 3, 3, 5, 7, 11]
            random.shuffle(factors)
            
            # Split factors for cross-canceling in division
            num1_factors = factors[:2]
            denom1_factors = factors[2:4]
            num2_factors = factors[4:6]
            denom2_factors = factors[6:]
            
            num1 = math.prod(num1_factors)
            denom1 = math.prod(denom1_factors)
            num2 = math.prod(num2_factors)
            denom2 = math.prod(denom2_factors)
            
            problem = f"Divide and simplify: ({num1}/{denom1}) ÷ ({num2}/{denom2})"
            result = Fraction(num1 * denom2, denom1 * num2)
            answer = self._format_fraction(result, mixed=True)
            return problem, answer
    
    def _format_fraction(self, fraction: Fraction, mixed: bool = False) -> str:
        """Format a fraction as a string, optionally as a mixed number."""
        if fraction.numerator == 0:
            return "0"
            
        if not mixed:
            if fraction.denominator == 1:
                return str(fraction.numerator)
            return f"{fraction.numerator}/{fraction.denominator}"
        
        # Convert to mixed number
        whole = fraction.numerator // fraction.denominator
        remainder = fraction.numerator % fraction.denominator
        
        if whole == 0:
            if remainder == 0:
                return "0"
            return f"{remainder}/{fraction.denominator}"
        elif remainder == 0:
            return str(whole)
        else:
            return f"{whole} {remainder}/{fraction.denominator}"
    
    def _generate_comparison_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate fraction comparison problems."""
        if difficulty == 'easy':
            # Compare two fractions with common denominators
            denom = random.randint(2, 12)
            num1 = random.randint(1, denom-1)
            num2 = random.randint(1, denom-1)
            
            # Ensure they're different
            while num1 == num2:
                num2 = random.randint(1, denom-1)
            
            problem = f"Compare: {num1}/{denom} __ {num2}/{denom} (use <, >, or =)"
            if num1 > num2:
                answer = ">"
            else:
                answer = "<"
                
            return problem, answer
            
        elif difficulty == 'medium':
            # Compare fractions with different denominators
            denom1 = random.choice([2, 3, 4, 6, 8, 12])
            denom2 = denom1 * random.choice([2, 3, 4])
            num1 = random.randint(1, denom1-1)
            num2 = random.randint(1, denom2-1)
            
            # Calculate cross products to determine relationship
            cross1 = num1 * denom2
            cross2 = num2 * denom1
            
            problem = f"Compare: {num1}/{denom1} __ {num2}/{denom2} (use <, >, or =)"
            if cross1 > cross2:
                answer = ">"
            elif cross1 < cross2:
                answer = "<"
            else:
                answer = "="
                
            return problem, answer
            
        else:  # hard
            # Compare mixed numbers and improper fractions
            whole = random.randint(1, 3)
            denom1 = random.choice([3, 4, 5, 6, 8, 12])
            denom2 = random.choice([3, 4, 5, 6, 8, 12])
            num1 = random.randint(1, denom1-1)
            num2 = random.randint(denom2, denom2*2)  # Make it improper
            
            # Calculate decimal values for comparison
            value1 = whole + (num1 / denom1)
            value2 = num2 / denom2
            
            problem = f"Compare: {whole} {num1}/{denom1} __ {num2}/{denom2} (use <, >, or =)"
            if abs(value1 - value2) < 0.0001:  # Account for floating point precision
                answer = "="
            elif value1 > value2:
                answer = ">"
            else:
                answer = "<"
                
            return problem, answer
    
    def _generate_conversion_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate problems involving fraction/decimal/percentage conversions."""
        if difficulty == 'easy':
            # Simple fraction to decimal
            denom = random.choice([2, 4, 5, 10, 20, 25, 50, 100])
            num = random.randint(1, denom-1)
            
            problem = f"Convert {num}/{denom} to a decimal."
            answer = f"{num/denom:.2f}".rstrip('0').rstrip('.')
            return problem, answer
            
        elif difficulty == 'medium':
            # Mixed number to decimal or percentage
            if random.random() < 0.5:
                # Mixed to decimal
                whole = random.randint(1, 5)
                denom = random.choice([2, 4, 5, 8, 10, 20, 25, 50])
                num = random.randint(1, denom-1)
                
                problem = f"Convert {whole} {num}/{denom} to a decimal."
                decimal = whole + (num / denom)
                answer = f"{decimal:.3f}".rstrip('0').rstrip('.')
                return problem, answer
            else:
                # Fraction to percentage
                denom = random.choice([2, 4, 5, 10, 20, 25, 50, 100])
                num = random.randint(1, denom-1)
                
                problem = f"Convert {num}/{denom} to a percentage."
                percentage = (num / denom) * 100
                if percentage == int(percentage):
                    answer = f"{int(percentage)}%"
                else:
                    answer = f"{percentage:.1f}%".replace(".0", "")
                return problem, answer
                
        else:  # hard
            # Complex conversions between all forms
            problem_type = random.choice(['fraction_to_decimal', 'decimal_to_fraction', 'percentage_to_fraction'])
            
            if problem_type == 'fraction_to_decimal':
                # Complex fraction to decimal (repeating)
                denom = random.choice([3, 6, 7, 9, 11, 12, 13, 15])
                num = random.randint(1, denom-1)
                
                problem = f"Convert {num}/{denom} to a decimal. Use a bar to show repeating decimals."
                
                # Calculate decimal representation with repeating pattern
                decimal = num / denom
                if num % denom == 0:
                    answer = str(int(decimal))
                else:
                    # Find repeating pattern
                    remainder = num % denom
                    seen = {}
                    decimal_part = []
                    i = 0
                    
                    while remainder != 0 and remainder not in seen:
                        seen[remainder] = i
                        quotient, remainder = divmod(remainder * 10, denom)
                        decimal_part.append(str(quotient))
                        i += 1
                        
                        # Prevent infinite loops
                        if len(decimal_part) > 100:
                            break
                    
                    if remainder == 0:
                        answer = f"{num//denom}." + "".join(decimal_part) if num > denom else "0." + "".join(decimal_part)
                    else:
                        # We have a repeating pattern
                        idx = seen[remainder]
                        non_repeating = decimal_part[:idx]
                        repeating = decimal_part[idx:]
                        
                        decimal_str = f"{num//denom}." if num > denom else "0."
                        if non_repeating:
                            decimal_str += "".join(non_repeating)
                        decimal_str += "(" + "".join(repeating) + ")"
                        answer = decimal_str
                
                return problem, answer
                
            elif problem_type == 'decimal_to_fraction':
                # Terminating decimal to fraction
                decimal = round(random.uniform(0.1, 0.95), 2)
                while decimal * 100 != int(decimal * 100):  # Ensure exact decimal
                    decimal = round(random.uniform(0.1, 0.95), 2)
                
                problem = f"Convert {decimal} to a fraction in simplest form."
                
                # Convert to fraction
                numerator = int(decimal * 100)
                denominator = 100
                frac = Fraction(numerator, denominator)
                answer = self._format_fraction(frac)
                
                return problem, answer
                
            else:  # percentage_to_fraction
                # Percentage to fraction in simplest form
                percentage = random.choice([12.5, 33.33, 37.5, 62.5, 66.67, 83.33, 87.5])
                
                problem = f"Convert {percentage}% to a fraction in simplest form."
                
                # Convert to fraction
                frac = Fraction(str(percentage)) / 100
                answer = self._format_fraction(frac)
                
                return problem, answer
    
    def _generate_mixed_operations_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate problems with mixed operations on fractions."""
        if difficulty == 'easy':
            # Two operations with like denominators
            denom = random.randint(2, 12)
            nums = [random.randint(1, denom-1) for _ in range(3)]
            ops = random.sample(['+', '-', '×'], 2)
            
            # Ensure positive results for subtraction
            if ops[0] == '-' and nums[0] < nums[1]:
                nums[0], nums[1] = nums[1], nums[0]
            
            problem = f"Calculate: {nums[0]}/{denom} {ops[0]} {nums[1]}/{denom} {ops[1]} {nums[2]}/{denom}"
            
            # Evaluate step by step
            if ops[0] == '+':
                step1 = Fraction(nums[0] + nums[1], denom)
            elif ops[0] == '-':
                step1 = Fraction(nums[0] - nums[1], denom)
            else:  # ×
                step1 = Fraction(nums[0] * nums[1], denom * denom)
                
            if ops[1] == '+':
                result = step1 + Fraction(nums[2], denom)
            elif ops[1] == '-':
                result = step1 - Fraction(nums[2], denom)
            else:  # ×
                result = step1 * Fraction(nums[2], denom)
            
            answer = self._format_fraction(result)
            return problem, answer
            
        elif difficulty == 'medium':
            # Two operations with unlike denominators (no mixed numbers)
            denoms = [random.randint(2, 12) for _ in range(3)]
            nums = [random.randint(1, d-1) for d in denoms]
            ops = random.sample(['+', '-', '×', '÷'], 2)
            
            problem = f"Calculate: ({nums[0]}/{denoms[0]} {ops[0]} {nums[1]}/{denoms[1]}) {ops[1]} {nums[2]}/{denoms[2]}"
            
            # Evaluate first operation
            frac1 = Fraction(nums[0], denoms[0])
            frac2 = Fraction(nums[1], denoms[1])
            
            if ops[0] == '+':
                step1 = frac1 + frac2
            elif ops[0] == '-':
                step1 = frac1 - frac2
            elif ops[0] == '×':
                step1 = frac1 * frac2
            else:  # ÷
                step1 = frac1 / frac2
            
            # Evaluate second operation
            frac3 = Fraction(nums[2], denoms[2])
            
            if ops[1] == '+':
                result = step1 + frac3
            elif ops[1] == '-':
                result = step1 - frac3
            elif ops[1] == '×':
                result = step1 * frac3
            else:  # ÷
                result = step1 / frac3
            
            answer = self._format_fraction(result, mixed=True)
            return problem, answer
            
        else:  # hard
            # Three operations with mixed numbers and all operations
            # Generate three mixed numbers
            wholes = [random.randint(1, 3) for _ in range(3)]
            denoms = [random.choice([3, 4, 5, 6, 8, 12]) for _ in range(3)]
            nums = [random.randint(1, d-1) for d in denoms]
            
            # Ensure we have at least one of each operation
            ops = random.sample(['+', '-', '×', '÷'], 3)
            
            # Build the problem string
            problem_parts = []
            for i in range(3):
                problem_parts.append(f"{wholes[i]} {nums[i]}/{denoms[i]}")
                if i < 2:
                    problem_parts.append(ops[i])
            
            problem = f"Calculate: {' '.join(problem_parts)}"
            
            # Convert to improper fractions
            fracs = [Fraction(w * d + n, d) for w, n, d in zip(wholes, nums, denoms)]
            
            # Evaluate with proper order of operations (PEMDAS)
            # First do multiplications and divisions left to right
            values = [fracs[0]]
            current_ops = []
            
            for i in range(2):
                if ops[i] in ['×', '÷']:
                    left = values.pop()
                    right = fracs[i+1]
                    if ops[i] == '×':
                        values.append(left * right)
                    else:  # ÷
                        values.append(left / right)
                else:
                    values.append(fracs[i+1])
                    current_ops.append(ops[i])
            
            # Then do additions and subtractions left to right
            result = values[0]
            for i in range(len(current_ops)):
                if current_ops[i] == '+':
                    result += values[i+1]
                else:  # '-'
                    result -= values[i+1]
            
            answer = self._format_fraction(result, mixed=True)
            return problem, answer
    
    def _generate_measurement_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate measurement problems involving fractions."""
        if difficulty == 'easy':
            # Simple addition/subtraction of measurements with fractions
            unit = random.choice(['inches', 'feet', 'pounds', 'cups', 'gallons'])
            denom = random.choice([2, 4, 8])
            num1 = random.randint(1, denom-1)
            num2 = random.randint(1, denom-1)
            
            problem = f"A piece of wood is 3 {num1}/{denom} {unit} long. " \
                     f"If you cut off 1 {num2}/{denom} {unit}, how much is left?"
            
            total = Fraction(3 * denom + num1, denom)
            cut = Fraction(denom + num2, denom)
            result = total - cut
            
            whole = result.numerator // result.denominator
            remainder = result.numerator % result.denominator
            
            if remainder == 0:
                answer = f"{whole} {unit}"
            else:
                answer = f"{whole} {remainder}/{result.denominator} {unit}"
                
            return problem, answer
            
        elif difficulty == 'medium':
            # Area/volume with fractions
            shape = random.choice(['rectangle', 'box'])
            
            if shape == 'rectangle':
                # Area of rectangle
                len_whole = random.randint(2, 5)
                wid_whole = random.randint(1, len_whole-1)
                len_num, len_den = random.choice([(1,2), (1,3), (1,4), (3,4)])
                wid_num, wid_den = random.choice([(1,2), (1,3), (2,3), (3,4)])
                
                problem = f"Find the area of a rectangle with length {len_whole} {len_num}/{len_den} feet and width {wid_whole} {wid_num}/{wid_den} feet."
                
                len_frac = len_whole + Fraction(len_num, len_den)
                wid_frac = wid_whole + Fraction(wid_num, wid_den)
                area = len_frac * wid_frac
                
                answer = self._format_fraction(area, mixed=True) + " square feet"
                return problem, answer
                
            else:  # box
                # Volume of rectangular prism
                l_whole = random.randint(1, 3)
                w_whole = random.randint(1, 3)
                h_whole = random.randint(1, 3)
                
                l_frac = random.choice(['1/2', '1/3', '2/3', '1/4', '3/4'])
                w_frac = random.choice(['1/2', '1/3', '2/3', '1/4', '3/4'])
                h_frac = random.choice(['1/2', '1/3', '2/3', '1/4', '3/4'])
                
                problem = f"Find the volume of a box with dimensions {l_whole} {l_frac} ft × {w_whole} {w_frac} ft × {h_whole} {h_frac} ft."
                
                # Parse fractions
                def parse_mixed(mixed):
                    if ' ' in mixed:
                        whole, frac = mixed.split()
                        return int(whole) + Fraction(frac)
                    return Fraction(mixed)
                
                length = parse_mixed(f"{l_whole} {l_frac}")
                width = parse_mixed(f"{w_whole} {w_frac}")
                height = parse_mixed(f"{h_whole} {h_frac}")
                
                volume = length * width * height
                answer = self._format_fraction(volume, mixed=True) + " cubic feet"
                return problem, answer
                
        else:  # hard
            # Multi-step measurement problem
            problem_type = random.choice(['recipe', 'construction', 'fabric'])
            
            if problem_type == 'recipe':
                # Recipe scaling with multiple ingredients
                num_ingredients = random.randint(2, 4)
                ingredients = random.sample([
                    ('flour', 'cups'),
                    ('sugar', 'cups'),
                    ('milk', 'cups'),
                    ('butter', 'tablespoons'),
                    ('eggs', '')
                ], num_ingredients)
                
                # Original amounts (as fractions)
                original = {}
                for ing, unit in ingredients:
                    denom = random.choice([2, 3, 4, 6, 8])
                    num = random.randint(1, denom-1)
                    original[(ing, unit)] = Fraction(num, denom)
                
                # Scaling factor
                scale_whole = random.randint(2, 4)
                scale_frac = random.choice(['1/2', '1/3', '2/3', '3/4'])
                scale = scale_whole + Fraction(scale_frac)
                
                # Build problem
                problem = "A recipe calls for the following ingredients:\n"
                for (ing, unit), amount in original.items():
                    if amount.denominator == 1:
                        problem += f"- {amount.numerator} {unit} {ing}\n"
                    else:
                        problem += f"- {amount.numerator}/{amount.denominator} {unit} {ing}\n"
                
                problem += f"\nYou want to make {scale_whole} {scale_frac} times the recipe. How much of each ingredient will you need?"
                
                # Calculate answers
                answers = []
                for (ing, unit), amount in original.items():
                    total = amount * scale
                    
                    # Format as mixed number
                    whole = total.numerator // total.denominator
                    remainder = total.numerator % total.denominator
                    
                    if whole == 0:
                        if remainder == 0:
                            amount_str = "0"
                        else:
                            amount_str = f"{remainder}/{total.denominator}"
                    else:
                        if remainder == 0:
                            amount_str = str(whole)
                        else:
                            amount_str = f"{whole} {remainder}/{total.denominator}"
                    
                    unit_str = f" {unit}" if unit else ""
                    answers.append(f"- {amount_str}{unit_str} {ing}")
                
                return problem, "\n".join(answers)
                
            elif problem_type == 'construction':
                # Construction problem with leftover materials
                material = random.choice(['wood', 'pipe', 'wire', 'fabric'])
                unit = random.choice(['feet', 'yards', 'meters'])
                
                # Board lengths as mixed numbers
                board1 = f"{random.randint(4, 8)} {random.choice(['1/2', '1/3', '2/3', '1/4', '3/4'])}"
                board2 = f"{random.randint(4, 8)} {random.choice(['1/2', '1/3', '2/3', '1/4', '3/4'])}"
                
                # Parse to fractions
                def parse_mixed(mixed):
                    parts = mixed.split()
                    if len(parts) == 1:
                        return Fraction(parts[0])
                    whole, frac = parts
                    return int(whole) + Fraction(frac)
                
                b1 = parse_mixed(board1)
                b2 = parse_mixed(board2)
                
                # Calculate total
                total = b1 + b2
                
                # How much to cut off (random fraction between 1/4 and 3/4 of the smallest board)
                cut_frac = Fraction(random.randint(1, 3), 4)
                cut_amount = min(b1, b2) * cut_frac
                
                problem = f"You have two pieces of {material}: one is {board1} {unit} and the other is {board2} {unit}. " \
                         f"If you cut off {self._format_fraction(cut_frac)} of the shorter piece, how much {material} will you have in total?"
                
                remaining = total - cut_amount
                answer = f"{self._format_fraction(remaining, mixed=True)} {unit}"
                
                return problem, answer
                
            else:  # fabric
                # Fabric problem with unit conversion
                yards = random.randint(1, 3)
                inches = random.choice([0, 6, 9, 12, 18])
                
                cut_pieces = []
                total_inches = yards * 36 + inches
                
                # Generate random pieces that add up to less than total
                remaining = total_inches
                while remaining > 12:  # Minimum piece size of 1 foot
                    piece = random.randint(12, min(36, remaining))
                    cut_pieces.append(piece)
                    remaining -= piece
                
                # Calculate remaining fabric
                total_used = sum(cut_pieces)
                remaining_inches = total_inches - total_used
                
                # Convert remaining to yards, feet, inches
                yards_remain = remaining_inches // 36
                feet_remain = (remaining_inches % 36) // 12
                inches_remain = (remaining_inches % 36) % 12
                
                # Build problem
                pieces_str = ", ".join([f"{p//12} feet {p%12} inches" for p in cut_pieces])
                
                problem = f"You have a piece of fabric that is {yards} yards {inches} inches long. " \
                         f"You cut the following pieces: {pieces_str}. " \
                         f"How much fabric is left? Give your answer in yards, feet, and inches."
                
                # Build answer
                answer_parts = []
                if yards_remain > 0:
                    answer_parts.append(f"{yards_remain} yard{'s' if yards_remain > 1 else ''}")
                if feet_remain > 0:
                    answer_parts.append(f"{feet_remain} foot{'s' if feet_remain > 1 else ''}")
                if inches_remain > 0 or not answer_parts:
                    answer_parts.append(f"{inches_remain} inch{'es' if inches_remain != 1 else ''}")
                
                answer = " ".join(answer_parts)
                return problem, answer

# Example usage
if __name__ == "__main__":
    generator = FractionWordProblemGenerator()
    
    print("=== Fraction Word Problem Generator ===\n")
    
    # Test different problem types
    for difficulty in ['easy', 'medium', 'hard']:
        print(f"\n--- {difficulty.upper()} PROBLEMS ---")
        
        # Recipe problem
        problem, answer = generator._generate_recipe_problem(difficulty)
        print("\nRecipe Problem:")
        print(f"Q: {problem}")
        print(f"A: {answer}")
        
        # Sharing problem
        problem, answer = generator._generate_sharing_problem(difficulty)
        print("\nSharing Problem:")
        print(f"Q: {problem}")
        print(f"A: {answer}")
        
        # Addition problem
        problem, answer = generator._generate_addition_problem(difficulty)
        print("\nAddition Problem:")
        print(f"Q: {problem}")
        print(f"A: {answer}")
        
        # Subtraction problem
        problem, answer = generator._generate_subtraction_problem(difficulty)
        print("\nSubtraction Problem:")
        print(f"Q: {problem}")
        print(f"A: {answer}")
        
        # Multiplication problem
        problem, answer = generator._generate_multiplication_problem(difficulty)
        print("\nMultiplication Problem:")
        print(f"Q: {problem}")
        print(f"A: {answer}")
        
        # Division problem
        problem, answer = generator._generate_division_problem(difficulty)
        print("\nDivision Problem:")
        print(f"Q: {problem}")
        print(f"A: {answer}")
        
        # Comparison problem
        problem, answer = generator._generate_comparison_problem(difficulty)
        print("\nComparison Problem:")
        print(f"Q: {problem}")
        print(f"A: {answer}")
        
        # Conversion problem
        problem, answer = generator._generate_conversion_problem(difficulty)
        print("\nConversion Problem:")
        print(f"Q: {problem}")
        print(f"A: {answer}")
        
        # Mixed operations problem
        problem, answer = generator._generate_mixed_operations_problem(difficulty)
        print("\nMixed Operations Problem:")
        print(f"Q: {problem}")
        print(f"A: {answer}")
        
        # Measurement problem
        problem, answer = generator._generate_measurement_problem(difficulty)
        print("\nMeasurement Problem:")
        print(f"Q: {problem}")
        print(f"A: {answer}")
