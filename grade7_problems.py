import random
from typing import Tuple, Dict, Any, Union
import math

class Grade7ProblemGenerator:
    def __init__(self):
        self.generators = {
            'Number System': {
                'Integers': self.generate_integer_problem,
                'Fractions and Decimals': self.generate_fraction_decimal_problem,
                'Rational Numbers': self.generate_rational_number_problem
            },
            'Algebra': {
                'Algebraic Expressions': self.generate_algebraic_expression,
                'Simple Equations': self.generate_simple_equation,
                'Exponents and Powers': self.generate_exponent_problem
            },
            'Geometry': {
                'Lines and Angles': self.generate_lines_angles_problem,
                'Triangles': self.generate_triangle_problem,
                'Congruence': self.generate_congruence_problem,
                'Symmetry': self.generate_symmetry_problem
            },
            'Mensuration': {
                'Perimeter and Area': self.generate_perimeter_area_problem,
                'Visualizing Solid Shapes': self.generate_solid_shapes_problem
            },
            'Data Handling': {
                'Probability': self.generate_probability_problem,
                'Chance and Probability': self.generate_chance_probability_problem
            }
        }
    
    def generate_problem(self, topic: str, subtopic: str, difficulty: str = 'medium') -> Tuple[str, Any]:
        """Generate a problem based on topic, subtopic, and difficulty."""
        return self.generators[topic][subtopic](difficulty)
    
    # Number System Problems
    def generate_integer_problem(self, difficulty: str) -> Tuple[str, Any]:
        """Generate integer problems including operations, properties, and word problems."""
        problem_type = random.choices(
            ['basic_operation', 'property', 'word_problem', 'ordering', 'absolute_value'],
            weights=[0.4, 0.2, 0.25, 0.1, 0.05],
            k=1
        )[0]
        
        if problem_type == 'basic_operation':
            return self._generate_integer_operation(difficulty)
        elif problem_type == 'property':
            return self._generate_integer_property(difficulty)
        elif problem_type == 'word_problem':
            return self._generate_integer_word_problem(difficulty)
        elif problem_type == 'ordering':
            return self._generate_integer_ordering(difficulty)
        else:  # absolute_value
            return self._generate_absolute_value_problem(difficulty)
    
    def _generate_integer_operation(self, difficulty: str) -> Tuple[str, Union[int, str]]:
        """Generate basic integer operation problems."""
        if difficulty == 'easy':
            a = random.randint(-20, 20)
            b = random.randint(1, 20)
            op = random.choice(['+', '-', '×', '÷'])
        elif difficulty == 'medium':
            a = random.randint(-50, 50)
            b = random.randint(1, 50)
            op = random.choice(['+', '-', '×', '÷', '**'])
        else:  # hard
            a = random.randint(-100, 100)
            b = random.randint(1, 100)
            op = random.choice(['+', '-', '×', '÷', '**'])
        
        if op == '+':
            return f"{a} + {b} = ?", a + b
        elif op == '-':
            return f"{a} - {b} = ?", a - b
        elif op == '×':
            return f"{a} × {b} = ?", a * b
        elif op == '÷':
            if b == 0:  # Avoid division by zero
                b = random.randint(1, 20)
            return f"{a} ÷ {b} = ? (Round to 2 decimal places if needed)", round(a / b, 2)
        else:  # **
            exp = random.choice([2, 3])
            return f"{a}^{exp} = ?", a ** exp
    
    def _generate_integer_property(self, difficulty: str) -> Tuple[str, str]:
        """Generate questions about integer properties."""
        properties = [
            ("commutative", "addition"),
            ("associative", "addition"),
            ("distributive", "multiplication over addition"),
            ("additive identity", "0"),
            ("multiplicative identity", "1"),
            ("additive inverse", "a + (-a) = 0"),
            ("multiplicative inverse", "a × (1/a) = 1 for a ≠ 0")
        ]
        
        if difficulty == 'easy':
            prop, answer = random.choice(properties[:4])
            return f"What is the {prop} property of integers? (hint: it's related to {answer if isinstance(answer, str) else ''})", prop
        else:
            prop, answer = random.choice(properties)
            question = random.choice([
                f"Which property is demonstrated by: {self._get_property_example(prop)}",
                f"Name the property: {self._get_property_example(prop)}",
                f"What is the name of the property that states: {self._get_property_definition(prop)}?"
            ])
            return question, prop
    
    def _get_property_example(self, prop_name: str) -> str:
        """Return an example of a property."""
        examples = {
            'commutative': '3 + 5 = 5 + 3',
            'associative': '(2 + 3) + 4 = 2 + (3 + 4)',
            'distributive': '3 × (4 + 5) = 3×4 + 3×5',
            'additive identity': '7 + 0 = 7',
            'multiplicative identity': '9 × 1 = 9',
            'additive inverse': '5 + (-5) = 0',
            'multiplicative inverse': '4 × (1/4) = 1'
        }
        return examples.get(prop_name, 'This property has no example.')
    
    def _get_property_definition(self, prop_name: str) -> str:
        """Return a definition of a property."""
        definitions = {
            'commutative': 'the order of numbers does not change the result',
            'associative': 'the grouping of numbers does not change the result',
            'distributive': 'multiplying a sum by a number gives the same result as multiplying each addend by the number and then adding the products',
            'additive identity': 'adding zero to any number leaves it unchanged',
            'multiplicative identity': 'multiplying any number by one leaves it unchanged',
            'additive inverse': 'the sum of a number and its negative is zero',
            'multiplicative inverse': 'the product of a number and its reciprocal is one'
        }
        return definitions.get(prop_name, 'No definition available.')
    
    def _generate_integer_word_problem(self, difficulty: str) -> Tuple[str, Union[int, str]]:
        """Generate word problems involving integers."""
        problem_types = [
            self._generate_quiz_scoring_problem,  # Add the new problem type
            self._generate_temperature_problem,
            self._generate_elevation_problem,
            self._generate_money_problem,
            self._generate_sequence_problem,
            self._generate_average_problem
        ]
        # Make quiz scoring problems more likely for hard difficulty
        if difficulty == 'hard':
            problem_types.extend([self._generate_quiz_scoring_problem] * 2)
        return random.choice(problem_types)(difficulty)
        
    def _generate_quiz_scoring_problem(self, difficulty: str) -> Tuple[str, Union[int, str]]:
        """Generate quiz scoring problems with positive and negative marking."""
        if difficulty == 'easy':
            correct = random.randint(5, 15)
            incorrect = random.randint(1, 10)
            points_per_correct = random.choice([3, 4, 5])
            points_per_incorrect = random.choice([1, 2])
            
            problem = (
                f"In a quiz, {points_per_correct} marks are awarded for each correct answer, "
                f"and {points_per_incorrect} marks are deducted for each incorrect answer. "
                f"If a student answers {correct} questions correctly and {incorrect} questions incorrectly, "
                "how many marks will they score?"
            )
            score = (correct * points_per_correct) - (incorrect * points_per_incorrect)
            return problem, score
            
        else:  # hard difficulty - multi-step problems
            problem_type = random.choice([
                'find_attempted',
                'find_correct',
                'find_incorrect',
                'passing_grade'
            ])
            
            if problem_type == 'find_attempted':
                total_questions = random.randint(15, 30)
                correct = random.randint(5, total_questions - 5)
                points_per_correct = random.choice([3, 4, 5])
                points_per_incorrect = random.choice([1, 2])
                total_score = (correct * points_per_correct) - ((total_questions - correct) * points_per_incorrect)
                
                problem = (
                    f"In a test with {total_questions} questions, {points_per_correct} marks are given for each correct answer "
                    f"and {points_per_incorrect} marks are deducted for each wrong answer. "
                    f"A student scored {total_score} marks. How many questions did they attempt correctly?"
                )
                return problem, correct
                
            elif problem_type == 'find_correct':
                total_questions = random.randint(15, 30)
                points_per_correct = random.choice([3, 4, 5])
                points_per_incorrect = random.choice([1, 2])
                total_score = random.randint(20, 100)
                
                # Ensure the problem has a valid solution
                max_possible = total_questions * points_per_correct
                total_score = min(total_score, max_possible - 5)  # Ensure it's solvable
                
                problem = (
                    f"A test has {total_questions} questions. {points_per_correct} marks are given for each correct answer, "
                    f"and {points_per_incorrect} marks are deducted for each wrong answer. "
                    f"If a student scored {total_score} marks, how many questions did they get right?"
                )
                
                # Calculate correct answers (solving: c*pc - (t-c)*pi = score)
                # c = (score + t*pi)/(pc + pi)
                correct = (total_score + (total_questions * points_per_incorrect)) // (points_per_correct + points_per_incorrect)
                return problem, correct
                
            elif problem_type == 'find_incorrect':
                total_questions = random.randint(15, 30)
                correct = random.randint(5, total_questions - 5)
                points_per_correct = random.choice([3, 4, 5])
                points_per_incorrect = random.choice([1, 2])
                total_score = (correct * points_per_correct) - ((total_questions - correct) * points_per_incorrect)
                
                problem = (
                    f"In an exam with {total_questions} questions, {points_per_correct} marks are awarded for each correct answer, "
                    f"and {points_per_incorrect} marks are deducted for each wrong answer. "
                    f"A student who answered all questions scored {total_score}. "
                    "How many questions did they answer incorrectly?"
                )
                return problem, total_questions - correct
                
            else:  # passing_grade
                total_questions = random.randint(15, 30)
                passing_score = random.randint(50, 70)
                points_per_correct = random.choice([3, 4, 5])
                points_per_incorrect = random.choice([1, 2])
                
                problem = (
                    f"An exam has {total_questions} questions. {points_per_correct} marks are given for each correct answer, "
                    f"and {points_per_incorrect} marks are deducted for each wrong answer. "
                    f"To pass, a student needs to score at least {passing_score} marks. "
                    f"What is the minimum number of questions they need to answer correctly to pass?"
                )
                
                # Solve for c: c*pc - (t-c)*pi >= passing_score
                # c >= (passing_score + t*pi)/(pc + pi)
                min_correct = (passing_score + (total_questions * points_per_incorrect) + 
                              (points_per_correct + points_per_incorrect - 1)) // (points_per_correct + points_per_incorrect)
                return problem, min_correct
    
    def _generate_temperature_problem(self, difficulty: str) -> Tuple[str, int]:
        """Generate temperature change problems."""
        if difficulty == 'easy':
            temp1 = random.randint(-10, 30)
            change = random.randint(5, 15)
            direction = random.choice(['increased', 'decreased'])
            if direction == 'increased':
                return f"If the temperature is {temp1}°C and it increases by {change}°C, what is the new temperature?", temp1 + change
            else:
                return f"If the temperature is {temp1}°C and it decreases by {change}°C, what is the new temperature?", temp1 - change
        else:
            temp1 = random.randint(-20, 40)
            change1 = random.randint(5, 20)
            change2 = random.randint(5, 20)
            return (
                f"The temperature was {temp1}°C. It rose by {change1}°C in the morning and then fell by {change2}°C in the evening. "
                f"What was the final temperature?",
                temp1 + change1 - change2
            )
    
    def _generate_elevation_problem(self, difficulty: str) -> Tuple[str, int]:
        """Generate elevation/altitude problems."""
        if difficulty == 'easy':
            elevation = random.randint(100, 500)
            descent = random.randint(50, 150)
            return f"A submarine is at {elevation}m below sea level. If it descends {descent}m, what is its new position?", -(elevation + descent)
        else:
            peak1 = random.randint(1000, 3000)
            peak2 = random.randint(1000, 3000)
            return (
                f"Mountain A is {peak1}m above sea level. Mountain B is {peak2}m above sea level. "
                f"What is the difference in their elevations?",
                abs(peak1 - peak2)
            )
    
    def _generate_money_problem(self, difficulty: str) -> Tuple[str, Union[int, str]]:
        """Generate money-related word problems."""
        if difficulty == 'easy':
            amount = random.randint(100, 1000)
            spent = random.randint(50, amount-50)
            return f"If you have ₹{amount} and you spend ₹{spent}, how much money do you have left?", amount - spent
        else:
            transactions = [
                (random.choice(['deposited', 'withdrew']), random.randint(100, 1000))
                for _ in range(3)
            ]
            problem = "A bank account has a balance of ₹2000. "
            balance = 2000
            
            for action, amount in transactions:
                if action == 'deposited':
                    balance += amount
                else:
                    balance -= amount
                    problem += f" Then, ₹{amount} was {action}."
            
            problem += " What is the final balance?"
            return problem, balance
    
    def _generate_sequence_problem(self, difficulty: str) -> Tuple[str, Union[int, float]]:
        """Generate number sequence problems."""
        if difficulty == 'easy':
            # Simple arithmetic sequences
            start = random.randint(-20, 20)
            step = random.choice([-3, -2, 2, 3, 4, 5])
            sequence = [start + i*step for i in range(5)]  # Generate 5 elements
            sequence_str = ", ".join(map(str, sequence[:4])) + ", ..."
            return f"What is the next number in the sequence: {sequence_str}?", sequence[4]
        else:
            # More complex patterns with guaranteed length
            patterns = [
                ('alternating', [1, -2, 3, -4, 5, -6]),
                ('squares', [1, 4, 9, 16, 25, 36]),
                ('cubes', [1, 8, 27, 64, 125]),
                ('primes', [2, 3, 5, 7, 11, 13]),
                ('fibonacci', [1, 1, 2, 3, 5, 8, 13]),
                ('powers_of_2', [2, 4, 8, 16, 32, 64]),
                ('triangular', [1, 3, 6, 10, 15, 21]),
                ('factorial', [1, 2, 6, 24, 120])
            ]
            
            # Select a pattern and ensure it has enough elements
            pattern_name, sequence = random.choice(patterns)
            while len(sequence) < 5:  # Ensure we have enough elements
                pattern_name, sequence = random.choice(patterns)
                
            # Show all but the last element in the problem
            sequence_str = ", ".join(map(str, sequence[:-1])) + "..."
            return f"Identify the pattern and find the next number: {sequence_str}", sequence[-1]
    
    def _generate_average_problem(self, difficulty: str) -> Tuple[str, Union[int, float]]:
        """Generate average/mean problems."""
        if difficulty == 'easy':
            numbers = [random.randint(1, 20) for _ in range(4)]
            avg = sum(numbers) / len(numbers)
            return f"Find the average of {', '.join(map(str, numbers))}.", round(avg, 2)
        else:
            count = random.randint(5, 8)
            numbers = [random.randint(1, 100) for _ in range(count)]
            avg = sum(numbers) / count
            numbers_str = ", ".join(map(str, numbers))
            return f"Calculate the mean of: {numbers_str}", round(avg, 2)
    
    def _generate_integer_ordering(self, difficulty: str) -> Tuple[str, str]:
        """Generate problems about ordering integers."""
        if difficulty == 'easy':
            numbers = sorted([random.randint(-10, 10) for _ in range(4)], reverse=random.choice([True, False]))
            order = random.choice(['ascending', 'descending'])
            if order == 'ascending':
                answer = sorted(numbers)
            else:
                answer = sorted(numbers, reverse=True)
            
            return f"Arrange in {order} order: {', '.join(map(str, numbers))}", ", ".join(map(str, answer))
        else:
            # Compare integers with absolute values
            a = random.randint(-50, 50)
            b = random.randint(-50, 50)
            op = random.choice(['<', '>', '==', '!='])
            
            # Calculate the result
            if op == '<':
                result = a < b
            elif op == '>':
                result = a > b
            elif op == '==':
                result = a == b
            else:  # !=
                result = a != b
            
            return f"Is {a} {op} {b}? (True/False)", str(result)
    
    def _generate_absolute_value_problem(self, difficulty: str) -> Tuple[str, int]:
        """Generate problems about absolute values."""
        if difficulty == 'easy':
            num = random.randint(-20, 20)
            return f"What is the absolute value of {num}?", abs(num)
        else:
            a = random.randint(-50, 50)
            b = random.randint(-50, 50)
            return f"Evaluate: |{a} - {b}| + |{b} - {a}|", 2 * abs(a - b)
    
    def generate_fraction_decimal_problem(self, difficulty: str) -> Tuple[str, Union[float, str]]:
        problem_types = [
            self._generate_simple_fraction_op,
            self._generate_mixed_number_op,
            self._generate_fraction_decimal_conversion,
            self._generate_fraction_word_problem
        ]
        
        # For easy difficulty, only use simple operations
        if difficulty == 'easy':
            problem_func = random.choice(problem_types[:2])
        else:
            problem_func = random.choice(problem_types)
            
        return problem_func(difficulty)
    
    def _generate_simple_fraction_op(self, difficulty: str) -> Tuple[str, Union[float, str]]:
        # Choose denominators and numerators
        denom1 = random.choice([2, 3, 4, 5, 6, 8, 10, 12])
        denom2 = denom1 if random.choice([True, False]) else random.choice([2, 3, 4, 5, 6, 8, 10, 12])
        
        num1 = random.randint(1, denom1-1)
        num2 = random.randint(1, denom2-1)
        
        # Choose operation
        op = random.choice(['+', '-', '×', '÷'])
        
        # Format the problem
        problem = f"{num1}/{denom1} {op} {num2}/{denom2} = "
        
        # Calculate the result
        if op == '+':
            res_num = num1 * denom2 + num2 * denom1
            res_den = denom1 * denom2
        elif op == '-':
            res_num = num1 * denom2 - num2 * denom1
            res_den = denom1 * denom2
        elif op == '×':
            res_num = num1 * num2
            res_den = denom1 * denom2
        else:  # ÷
            res_num = num1 * denom2
            res_den = denom1 * num2
        
        # Simplify the result
        gcd = math.gcd(res_num, res_den)
        res_num //= gcd
        res_den //= gcd
        
        # Format the answer
        if res_den == 1:
            ans = str(res_num)
        else:
            ans = f"{res_num}/{res_den}"
            
        return problem, ans
    
    def _generate_mixed_number_op(self, difficulty: str) -> Tuple[str, Union[float, str]]:
        # Generate mixed numbers: a b/c op d e/f
        b = random.randint(1, 4)
        c = random.choice([2, 3, 4, 5, 8])
        e = random.randint(1, 4)
        f = random.choice([2, 3, 4, 5, 8])
        
        # Ensure proper fractions
        a = random.randint(0, 3) if difficulty == 'easy' else random.randint(0, 5)
        d = random.randint(0, 3) if difficulty == 'easy' else random.randint(0, 5)
        
        op = random.choice(['+', '-', '×', '÷'])
        
        # Convert to improper fractions
        num1 = a * c + b
        num2 = d * f + e
        
        # Format problem
        problem = f"{a} {b}/{c} {op} {d} {e}/{f} = ?"
        
        # Calculate result
        if op == '+':
            res_num = num1 * f + num2 * c
            res_den = c * f
        elif op == '-':
            res_num = num1 * f - num2 * c
            res_den = c * f
        elif op == '×':
            res_num = num1 * num2
            res_den = c * f
        else:  # ÷
            res_num = num1 * f
            res_den = c * num2
        
        # Simplify result
        gcd = math.gcd(res_num, res_den)
        res_num //= gcd
        res_den //= gcd
        
        # Format answer
        if res_den == 1:
            ans = str(res_num)
        else:
            whole = res_num // res_den
            remainder = res_num % res_den
            if whole > 0 and remainder > 0:
                ans = f"{whole} {remainder}/{res_den}"
            else:
                ans = f"{remainder if remainder != 0 else whole}/{res_den}"
                
        return problem, ans
    
    def _generate_fraction_decimal_conversion(self, difficulty: str) -> Tuple[str, Union[float, str]]:
        if random.choice([True, False]):
            # Fraction to decimal
            den = random.choice([2, 4, 5, 8, 10, 20, 25, 50, 100])
            num = random.randint(1, den-1)
            problem = f"Convert {num}/{den} to a decimal."
            ans = round(num / den, 3)
            if ans == int(ans):
                ans = int(ans)
            return problem, ans
        else:
            # Decimal to fraction
            decimal = round(random.uniform(0.1, 0.9), 2)
            # Convert decimal to fraction
            den = 100 if decimal * 100 == int(decimal * 100) else 1000
            num = int(decimal * den)
            gcd = math.gcd(num, den)
            problem = f"Convert {decimal} to a fraction in simplest form."
            ans = f"{num//gcd}/{den//gcd}"
            return problem, ans
    
    def _generate_fraction_word_problem(self, difficulty: str) -> Tuple[str, Union[float, str]]:
        problem_type = random.choice(['recipe', 'ribbon', 'class', 'tank'])
        
        if problem_type == 'recipe':
            # Recipe problem: adding two fractions
            d1, d2 = random.choice([(2,4), (3,6), (4,8), (3,4), (5,10)])
            n1 = random.randint(1, d1-1)
            n2 = random.randint(1, d2-1)
            ingredients = ['flour', 'sugar', 'milk', 'butter', 'water']
            problem = f"A recipe needs {n1}/{d1} cups of {random.choice(ingredients)} and {n2}/{d2} cups of {random.choice(ingredients)}. How much total dry ingredients are needed?"
            
            # Calculate total
            total = n1/d1 + n2/d2
            ans = round(total, 2) if not total.is_integer() else int(total)
            
        elif problem_type == 'ribbon':
            # Ribbon cutting problem: division
            length = random.randint(2, 5)
            d = random.choice([2, 3, 4, 5, 6])
            n = random.randint(1, d-1)
            problem = f"A {length} meter long ribbon is cut into pieces of {n}/{d} meters each. How many pieces can be made?"
            
            # Calculate pieces
            pieces = (length * d) / n
            ans = int(pieces) if pieces.is_integer() else round(pieces, 2)
            
        elif problem_type == 'class':
            # Class fraction problem: multiplication of fractions
            d1, d2 = random.choice([(3,4), (2,3), (4,5), (5,6)])
            n1 = random.randint(1, d1-1)
            n2 = random.randint(1, d2-1)
            
            problem = f"If {n1}/{d1} of the class are boys and {n2}/{d2} of the boys wear glasses, " \
                     f"what fraction of the class are boys who wear glasses?"
            
            # Calculate fraction
            total_boys = n1/d1
            boys_with_glasses = total_boys * (n2/d2)
            
            # Convert to fraction
            from fractions import Fraction
            ans = str(Fraction(boys_with_glasses).limit_denominator())
            
        else:  # tank problem
            # Tank filling problem: solving for whole
            d1, d2 = random.choice([(3,4), (2,3), (3,5), (4,5)])
            n1 = 1  # initial fraction
            n2 = 1  # added fraction
            added_liters = random.randint(2, 10)
            
            problem = f"A tank is {n1}/{d1} full. After adding {added_liters} liters, it becomes {n2}/{d2} full. What is the capacity of the tank?"
            
            # Calculate capacity: (added_liters) / (n2/d2 - n1/d1)
            capacity = added_liters / ((n2/d2) - (n1/d1))
            ans = round(capacity, 2)
        
        return problem, ans
    
    def generate_rational_number_problem(self, difficulty: str) -> Tuple[str, str]:
        problem_types = [
            self._generate_rational_operation,
            self._generate_rational_comparison,
            self._generate_rational_word_problem,
            self._generate_rational_simplification
        ]
        return random.choice(problem_types)(difficulty)
    
    def _generate_rational_operation(self, difficulty: str) -> Tuple[str, str]:
        # Generate two fractions, possibly negative
        den1 = random.randint(2, 12)
        num1 = random.randint(1, den1-1)
        if random.random() > 0.5:
            num1 = -num1
            
        den2 = random.randint(2, 12)
        num2 = random.randint(1, den2-1)
        if random.random() > 0.5:
            num2 = -num2
        
        op = random.choice(['+', '-', '×', '÷', '+', '-'])  # More likely to get + or -
        
        # For harder problems, include mixed operations
        if difficulty == 'hard' and random.random() > 0.7:
            op2 = random.choice(['+', '-', '×', '÷'])
            den3 = random.randint(2, 12)
            num3 = random.randint(1, den3-1)
            if random.random() > 0.5:
                num3 = -num3
            
            # Calculate first operation
            if op == '+':
                temp_num = num1 * den2 + num2 * den1
                temp_den = den1 * den2
            elif op == '-':
                temp_num = num1 * den2 - num2 * den1
                temp_den = den1 * den2
            elif op == '×':
                temp_num = num1 * num2
                temp_den = den1 * den2
            else:  # ÷
                temp_num = num1 * den2
                temp_den = den1 * num2
            
            # Calculate second operation
            if op2 == '+':
                result_num = temp_num * den3 + num3 * temp_den
                result_den = temp_den * den3
            elif op2 == '-':
                result_num = temp_num * den3 - num3 * temp_den
                result_den = temp_den * den3
            elif op2 == '×':
                result_num = temp_num * num3
                result_den = temp_den * den3
            else:  # ÷
                result_num = temp_num * den3
                result_den = temp_den * num3
            
            problem = f"({num1}/{den1}) {op} ({num2}/{den2}) {op2} ({num3}/{den3}) = ?"
        else:
            # Single operation
            if op == '+':
                result_num = num1 * den2 + num2 * den1
                result_den = den1 * den2
            elif op == '-':
                result_num = num1 * den2 - num2 * den1
                result_den = den1 * den2
            elif op == '×':
                result_num = num1 * num2
                result_den = den1 * den2
            else:  # ÷
                result_num = num1 * den2
                result_den = den1 * num2
            
            problem = f"({num1}/{den1}) {op} ({num2}/{den2}) = ?"
        
        # Simplify fraction
        gcd = math.gcd(abs(result_num), abs(result_den))
        result_num //= gcd
        result_den //= gcd
        
        # Format answer
        if result_den == 1:
            answer = str(result_num)
        elif result_num < 0 and result_den < 0:
            answer = f"{abs(result_num)}/{abs(result_den)}"
        elif result_den < 0:
            answer = f"{-result_num}/{abs(result_den)}"
        else:
            answer = f"{result_num}/{result_den}"
        
        return problem, answer
    
    def _generate_rational_comparison(self, difficulty: str) -> Tuple[str, str]:
        # Generate two fractions to compare
        den1 = random.randint(2, 12)
        num1 = random.randint(1, den1-1)
        if random.random() > 0.7:  # 30% chance of negative
            num1 = -num1
            
        den2 = random.randint(2, 12)
        num2 = random.randint(1, den2-1)
        if random.random() > 0.7:  # 30% chance of negative
            num2 = -num2
        
        # Calculate decimal values for comparison
        val1 = num1 / den1
        val2 = num2 / den2
        
        # Choose comparison operator
        if abs(val1 - val2) < 0.01:  # Values are effectively equal
            op = '='
            answer = '='
        elif val1 < val2:
            op = random.choice(['<', '≤'])
            answer = '<' if op == '<' else '≤'
        else:
            op = random.choice(['>', '≥'])
            answer = '>' if op == '>' else '≥'
        
        problem = f"Compare: {num1}/{den1} __ {num2}/{den2} (use <, >, ≤, ≥, or =)"
        return problem, answer
    
    def _generate_rational_word_problem(self, difficulty: str) -> Tuple[str, str]:
        problems = [
            (
                "A recipe calls for {n1}/{d1} cups of sugar, but you only have {n2}/{d2} cups. "
                "How much more sugar do you need?",
                "{n1}/{d1} - {n2}/{d2}"
            ),
            (
                "A car travels {n1}/{d1} km in {n2}/{d2} hours. What is its speed in km/h?",
                "{n1}/{d1} ÷ {n2}/{d2}"
            ),
            (
                "If {n1}/{d1} of a number is {n2}/{d2}, what is the number?",
                "{n2}/{d2} ÷ {n1}/{d1}"
            ),
            (
                "A tank is {n1}/{d1} full. After adding {n2} liters, it becomes {n3}/{d3} full. "
                "What is the capacity of the tank?",
                "({n3}/{d3} - {n1}/{d1}) × capacity = {n2}"
            )
        ]
        
        if difficulty == 'easy':
            template, expr = random.choice(problems[:3])
        else:
            template, expr = random.choice(problems)
        
        # Generate appropriate numbers
        d1 = random.randint(2, 8)
        n1 = random.randint(1, d1-1)
        d2 = random.randint(2, 8)
        n2 = random.randint(1, d2-1)
        d3 = random.randint(2, 8)
        n3 = random.randint(1, d3-1)
        
        # For the tank problem, ensure n3/d3 > n1/d1
        if "tank" in template:
            while n3/d3 <= n1/d1:
                d3 = random.randint(2, 8)
                n3 = random.randint(1, d3-1)
        
        # Format the problem
        problem = template.format(n1=n1, d1=d1, n2=n2, d2=d2, n3=n3, d3=d3)
        
        # Calculate the answer
        try:
            if "tank" in template:
                # Special handling for tank problem
                capacity = n2 / ((n3/d3) - (n1/d1))
                gcd = math.gcd(int(capacity * 1000), 1000)
                num = int(capacity * 1000) // gcd
                den = 1000 // gcd
                if den == 1:
                    answer = str(num)
                else:
                    answer = f"{num}/{den}"
            else:
                # Evaluate the expression
                result = eval(expr.format(n1=n1, d1=d1, n2=n2, d2=d2, n3=n3, d3=d3))
                if isinstance(result, float):
                    if result == int(result):
                        answer = str(int(result))
                    else:
                        answer = str(round(result, 3)).rstrip('0').rstrip('.')
                else:
                    answer = str(result)
            
            return problem, answer
        except:
            # If evaluation fails, try a different problem
            return self._generate_rational_word_problem(difficulty)
    
    def _generate_rational_simplification(self, difficulty: str) -> Tuple[str, str]:
        # Generate a fraction that can be simplified
        if difficulty == 'easy':
            factor = random.randint(2, 5)
            den = random.randint(2, 5) * factor
            num = random.randint(1, den//factor) * factor
        else:
            factor1 = random.randint(2, 5)
            factor2 = random.randint(2, 5)
            den = random.randint(2, 5) * factor1 * factor2
            num = random.randint(1, den//(factor1*factor2)) * factor1 * factor2
            
            # Randomly make it negative
            if random.random() > 0.7:
                num = -num
        
        problem = f"Simplify the fraction {num}/{den} to its lowest terms."
        
        # Calculate simplified form
        gcd = math.gcd(abs(num), abs(den))
        simple_num = num // gcd
        simple_den = den // gcd
        
        if simple_den == 1:
            answer = str(simple_num)
        elif simple_num < 0 and simple_den < 0:
            answer = f"{abs(simple_num)}/{abs(simple_den)}"
        elif simple_den < 0:
            answer = f"{-simple_num}/{abs(simple_den)}"
        else:
            answer = f"{simple_num}/{simple_den}"
        
        return problem, answer
    
    # Algebra Problems
    def generate_algebraic_expression(self, difficulty: str) -> Tuple[str, str]:
        vars = 'xyz'
        var = random.choice(vars)
        
        if difficulty == 'easy':
            coeff = random.randint(1, 5)
            const = random.randint(1, 10)
            op = random.choice(['+', '-'])
            if op == '+':
                return f"Simplify: {coeff}{var} + {const} + {random.randint(1,3)}{var}", f"{coeff + random.randint(1,3)}{var} + {const}"
            else:
                return f"Simplify: {coeff}{var} - {const} - {random.randint(1,3)}{var}", f"{coeff - random.randint(1,3)}{var} - {const}"
        else:
            # More complex expressions
            terms = []
            num_terms = random.randint(2, 4)
            for _ in range(num_terms):
                coeff = random.randint(1, 5)
                terms.append(f"{coeff}{var}^{random.randint(1,3)}")
            
            problem = " + ".join(terms) + " = ?"
            return f"Simplify: {problem}", "Expression simplification"
    
    def generate_simple_equation(self, difficulty: str) -> Tuple[str, float]:
        a = random.randint(1, 5)
        b = random.randint(1, 10)
        c = random.randint(1, 20)
        
        if difficulty == 'easy':
            # ax + b = c
            x = (c - b) / a
            return f"Solve for x: {a}x + {b} = {c}", round(x, 2)
        else:
            # ax + b = cx + d
            d = random.randint(1, 10)
            x = (d - b) / (a - c) if a != c else "No unique solution"
            return f"Solve for x: {a}x + {b} = {c}x + {d}", round(x, 2) if isinstance(x, (int, float)) else x
    
    def generate_exponent_problem(self, difficulty: str) -> Tuple[str, int]:
        if difficulty == 'easy':
            base = random.randint(2, 5)
            exp = random.randint(2, 4)
            return f"{base}^{exp} = ?", base ** exp
        else:
            # Laws of exponents
            law = random.choice(['product', 'quotient', 'power'])
            base = random.randint(2, 5)
            a = random.randint(1, 5)
            b = random.randint(1, 5)
            
            if law == 'product':
                return f"{base}^{a} × {base}^{b} = ?", base ** (a + b)
            elif law == 'quotient':
                return f"{base}^{a} ÷ {base}^{b} = ?", base ** (a - b)
            else:  # power
                return f"({base}^{a})^{b} = ?", base ** (a * b)
    
    # Geometry Problems
    def generate_lines_angles_problem(self, difficulty: str) -> Tuple[str, float]:
        angle = random.randint(20, 160)
        
        if difficulty == 'easy':
            # Complementary/Supplementary angles
            if random.choice([True, False]):
                return f"What is the complement of {angle}°?", 90 - angle
            else:
                return f"What is the supplement of {angle}°?", 180 - angle
        else:
            # Find angle between parallel lines
            angle1 = random.randint(30, 150)
            angle2 = 180 - angle1  # Corresponding angles
            return f"Two parallel lines are cut by a transversal. If one angle is {angle1}°, what is its corresponding angle?", angle2
    
    def generate_triangle_problem(self, difficulty: str) -> Tuple[str, float]:
        if difficulty == 'easy':
            # Find missing angle
            angle1 = random.randint(30, 80)
            angle2 = random.randint(30, 80)
            angle3 = 180 - angle1 - angle2
            return f"A triangle has angles of {angle1}° and {angle2}°. What is the measure of the third angle?", angle3
        else:
            # Pythagorean theorem
            a = random.randint(3, 8)
            b = random.randint(3, 8)
            c = round(math.sqrt(a**2 + b**2), 2)
            return f"A right triangle has legs of {a} cm and {b} cm. What is the length of the hypotenuse?", c
    
    def generate_congruence_problem(self, difficulty: str) -> Tuple[str, str]:
        triangles = ['ΔABC', 'ΔDEF', 'ΔPQR', 'ΔXYZ']
        t1, t2 = random.sample(triangles, 2)
        criteria = random.choice(['SAS', 'ASA', 'SSS', 'RHS'])
        
        problem = f"By which criterion are {t1} and {t2} congruent if "
        
        if criteria == 'SAS':
            problem += f"two sides and the included angle of {t1} are equal to the corresponding parts of {t2}?"
        elif criteria == 'ASA':
            problem += f"two angles and the included side of {t1} are equal to the corresponding parts of {t2}?"
        elif criteria == 'SSS':
            problem += f"all three sides of {t1} are equal to the corresponding sides of {t2}?"
        else:  # RHS
            problem += f"the hypotenuse and one side of right-angled {t1} are equal to the corresponding parts of {t2}?"
        
        return problem, criteria
    
    def generate_symmetry_problem(self, difficulty: str) -> Tuple[str, int]:
        shapes = {
            'equilateral triangle': 3,
            'square': 4,
            'regular pentagon': 5,
            'regular hexagon': 6,
            'rectangle': 2,
            'isosceles triangle': 1,
            'scalene triangle': 0,
            'parallelogram': 0,
            'rhombus': 2,
            'kite': 1
        }
        
        shape, lines = random.choice(list(shapes.items()))
        return f"How many lines of symmetry does a {shape} have?", lines
    
    # Mensuration Problems
    def generate_perimeter_area_problem(self, difficulty: str) -> Tuple[str, float]:
        shape = random.choice(['rectangle', 'square', 'triangle', 'circle'])
        
        if shape == 'rectangle':
            l = random.randint(5, 20)
            w = random.randint(2, 10)
            if random.choice(['perimeter', 'area']) == 'perimeter':
                return f"Find the perimeter of a rectangle with length {l} cm and width {w} cm.", 2 * (l + w)
            else:
                return f"Find the area of a rectangle with length {l} cm and width {w} cm.", l * w
        
        elif shape == 'square':
            s = random.randint(3, 15)
            if random.choice(['perimeter', 'area']) == 'perimeter':
                return f"Find the perimeter of a square with side {s} cm.", 4 * s
            else:
                return f"Find the area of a square with side {s} cm.", s * s
        
        elif shape == 'triangle':
            b = random.randint(5, 15)
            h = random.randint(3, 10)
            return f"Find the area of a triangle with base {b} cm and height {h} cm.", 0.5 * b * h
        
        else:  # circle
            r = random.randint(1, 10)
            if random.choice(['circumference', 'area']) == 'circumference':
                return f"Find the circumference of a circle with radius {r} cm. (Use π = 3.14)", round(2 * 3.14 * r, 2)
            else:
                return f"Find the area of a circle with radius {r} cm. (Use π = 3.14)", round(3.14 * r * r, 2)
    
    def generate_solid_shapes_problem(self, difficulty: str) -> Tuple[str, float]:
        shapes = ['cube', 'cuboid', 'cylinder', 'sphere', 'cone']
        shape = random.choice(shapes)
        
        if shape == 'cube':
            s = random.randint(2, 8)
            return f"Find the volume of a cube with edge length {s} cm.", s ** 3
        
        elif shape == 'cuboid':
            l = random.randint(3, 10)
            w = random.randint(3, 10)
            h = random.randint(3, 10)
            return f"Find the volume of a cuboid with dimensions {l}cm × {w}cm × {h}cm.", l * w * h
        
        elif shape == 'cylinder':
            r = random.randint(2, 6)
            h = random.randint(5, 15)
            return f"Find the volume of a cylinder with radius {r} cm and height {h} cm. (Use π = 3.14)", round(3.14 * r * r * h, 2)
        
        elif shape == 'sphere':
            r = random.randint(2, 8)
            return f"Find the volume of a sphere with radius {r} cm. (Use π = 3.14)", round((4/3) * 3.14 * (r ** 3), 2)
        
        else:  # cone
            r = random.randint(2, 6)
            h = random.randint(4, 12)
            return f"Find the volume of a cone with radius {r} cm and height {h} cm. (Use π = 3.14)", round((1/3) * 3.14 * (r ** 2) * h, 2)
    
    # Data Handling Problems
    def generate_probability_problem(self, difficulty: str) -> Tuple[str, str]:
        if difficulty == 'easy':
            # Simple probability
            outcomes = random.randint(2, 6)
            success = random.randint(1, outcomes - 1)
            return f"A number is chosen at random from 1 to {outcomes}. What is the probability of choosing {success}?", f"{success}/{outcomes}"
        else:
            # Probability with multiple events
            die_faces = 6
            event = random.choice(['even', 'odd', 'prime', 'multiple of 3'])
            
            if event == 'even':
                favorable = 3  # 2,4,6
            elif event == 'odd':
                favorable = 3  # 1,3,5
            elif event == 'prime':
                favorable = 3  # 2,3,5
            else:  # multiple of 3
                favorable = 2  # 3,6
                
            return f"A die is rolled. What is the probability of getting an {event} number?", f"{favorable}/6"
    
    def generate_chance_probability_problem(self, difficulty: str) -> Tuple[str, str]:
        scenarios = [
            ("tossing a coin and getting heads", "1/2"),
            ("drawing a red card from a standard deck", "1/2"),
            ("drawing a heart from a standard deck", "1/4"),
            ("rolling a die and getting a number greater than 4", "1/3"),
            ("picking a vowel from the English alphabet", "5/26")
        ]
        
        problem, answer = random.choice(scenarios)
        return f"What is the probability of {problem}?", answer
