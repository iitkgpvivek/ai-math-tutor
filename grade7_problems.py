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
            self._generate_temperature_problem,
            self._generate_elevation_problem,
            self._generate_money_problem,
            self._generate_sequence_problem,
            self._generate_average_problem
        ]
        return random.choice(problem_types)(difficulty)
    
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
                problem += f" Then, ₹{amount} was {action}. "
            
            problem += "What is the final balance?"
            return problem, balance
    
    def _generate_sequence_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate number sequence problems."""
        if difficulty == 'easy':
            start = random.randint(-20, 20)
            step = random.choice([-3, -2, 2, 3, 4, 5])
            sequence = [start + i*step for i in range(4)]
            sequence_str = ", ".join(map(str, sequence[:3])) + ", ..."
            return f"What is the next number in the sequence: {sequence_str}?", sequence[3]
        else:
            # More complex patterns like alternating sequences
            pattern = random.choice([
                ('alternating', [1, -2, 3, -4, 5, -6]),
                ('squares', [1, 4, 9, 16, 25]),
                ('cubes', [1, 8, 27, 64]),
                ('primes', [2, 3, 5, 7, 11])
            ])
            pattern_name, sequence = pattern
            sequence_str = ", ".join(map(str, sequence[:4])) + "..."
            return f"Identify the pattern and find the next number: {sequence_str}", sequence[4]
    
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
    
    def generate_fraction_decimal_problem(self, difficulty: str) -> Tuple[str, float]:
        if difficulty == 'easy':
            # Simple fraction addition/subtraction
            denom = random.choice([2, 4, 5, 10, 100])
            a = random.randint(1, denom-1)
            b = random.randint(1, denom-1)
            op = random.choice(['+', '-'])
            if op == '+':
                return f"{a}/{denom} + {b}/{denom} = ?", round((a + b)/denom, 2)
            else:
                return f"{a}/{denom} - {b}/{denom} = ?", round((a - b)/denom, 2)
        else:
            # Mixed operations with decimals
            a = round(random.uniform(0.1, 10), 1)
            b = round(random.uniform(0.1, 10), 1)
            op = random.choice(['+', '-', '×', '÷'])
            if op == '+':
                return f"{a} + {b} = ?", round(a + b, 2)
            elif op == '-':
                return f"{a} - {b} = ?", round(a - b, 2)
            elif op == '×':
                return f"{a} × {b} = ?", round(a * b, 2)
            else:  # ÷
                return f"{a} ÷ {b} = ?", round(a / b, 2)
    
    def generate_rational_number_problem(self, difficulty: str) -> Tuple[str, str]:
        # Generate two fractions
        den1 = random.randint(2, 10)
        num1 = random.randint(1, den1-1)
        den2 = random.randint(2, 10)
        num2 = random.randint(1, den2-1)
        
        op = random.choice(['+', '-', '×', '÷'])
        
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
        
        # Simplify fraction
        gcd = math.gcd(result_num, result_den)
        result_num //= gcd
        result_den //= gcd
        
        problem = f"({num1}/{den1}) {op} ({num2}/{den2}) = ?"
        if result_den == 1:
            answer = str(result_num)
        else:
            answer = f"{result_num}/{result_den}"
        
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
