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
        """Generate recipe scaling problems with increasing complexity."""
        if difficulty == 'easy':
            # Multi-ingredient recipe with simple scaling
            num_ingredients = random.randint(2, 3)
            ingredients = random.sample(self.ingredients, num_ingredients)
            scale = random.randint(2, 4)
            
            problem = "A recipe has the following ingredients:\n"
            answers = []
            
            for i, (ing, unit) in enumerate(ingredients):
                # Generate amounts that work well with the scale factor
                base_amount = random.choice([1, 2, 3, 4, 6, 8, 12])
                denom = random.choice([2, 3, 4, 6, 8, 12])
                num = random.randint(1, denom-1)
                
                amount = f"{num}/{denom}" if random.random() < 0.7 else f"{random.randint(1, 3)} {num}/{denom}"
                problem += f"- {amount} {unit} {ing}\n"
                
                # Calculate scaled amount
                if ' ' in amount:
                    whole, frac = amount.split()
                    whole = int(whole)
                    num, denom = map(int, frac.split('/'))
                    total = (whole + Fraction(num, denom)) * scale
                else:
                    num, denom = map(int, amount.split('/'))
                    total = Fraction(num, denom) * scale
                
                # Format answer
                whole_part = total.numerator // total.denominator
                remainder = total.numerator % total.denominator
                
                if remainder == 0:
                    answer = f"{whole_part} {unit} {ing}"
                elif whole_part > 0:
                    answer = f"{whole_part} {remainder}/{total.denominator} {unit} {ing}"
                else:
                    answer = f"{remainder}/{total.denominator} {unit} {ing}"
                
                answers.append(answer.strip())
            
            problem += f"\nIf you want to make {scale} times the recipe, how much of each ingredient will you need?"
            return problem, "\n".join(answers)
            
        elif difficulty == 'medium':
            # Recipe with unit conversions and mixed numbers
            num_ingredients = random.randint(2, 4)
            ingredients = random.sample(self.ingredients, num_ingredients)
            
            # Choose a scaling factor that might require unit conversions
            scale_whole = random.randint(1, 3)
            scale_frac = random.choice(['1/2', '1/3', '2/3', '3/4'])
            
            problem = "You're scaling a recipe. The original recipe makes 1 batch with the following ingredients:\n"
            answers = []
            
            for i, (ing, unit) in enumerate(ingredients):
                # Generate mixed number amounts
                whole = random.randint(0, 2) if random.random() < 0.7 else 0
                denom = random.choice([2, 3, 4, 8])
                num = random.randint(1, denom-1)
                
                if whole > 0:
                    amount = f"{whole} {num}/{denom}"
                    amount_frac = whole + Fraction(num, denom)
                else:
                    amount = f"{num}/{denom}"
                    amount_frac = Fraction(num, denom)
                
                problem += f"- {amount} {unit} {ing}\n"
                
                # Calculate scaled amount
                scale_num, scale_den = map(int, scale_frac.split('/'))
                scale = scale_whole + Fraction(scale_num, scale_den)
                total = amount_frac * scale
                
                # Format answer with unit conversion if needed
                if unit == 'cups' and total >= 4:  # Convert to quarts if >= 4 cups
                    quarts = total // 4
                    cups = total % 4
                    if cups == 0:
                        answer = f"{quarts} qt {ing}"
                    else:
                        answer = f"{quarts} qt {cups.numerator}/{cups.denominator} cups {ing}"
                elif unit == 'tablespoons' and total >= 16:  # Convert to cups if >= 16 tbsp
                    cups = total / 16
                    if cups.denominator == 1:
                        answer = f"{cups.numerator} cups {ing}"
                    else:
                        answer = f"{cups.numerator}/{cups.denominator} cups {ing}"
                else:
                    whole_part = total.numerator // total.denominator
                    remainder = total.numerator % total.denominator
                    
                    if remainder == 0:
                        answer = f"{whole_part} {unit} {ing}"
                    elif whole_part > 0:
                        answer = f"{whole_part} {remainder}/{total.denominator} {unit} {ing}"
                    else:
                        answer = f"{remainder}/{total.denominator} {unit} {ing}"
                
                answers.append(answer.strip())
            
            problem += f"\nIf you want to make {scale_whole} {scale_frac} times the recipe, how much of each ingredient will you need? "
            problem += "Convert measurements to larger units when appropriate (e.g., 4 cups = 1 quart)."
            return problem, "\n".join(answers)
            
        else:  # hard
            # Advanced recipe with percentage adjustments and multiple conversions
            problem_type = random.choice(['restaurant', 'baking', 'catering'])
            
            if problem_type == 'restaurant':
                # Restaurant-style problem with portion control and waste factor
                num_ingredients = random.randint(3, 5)
                ingredients = random.sample(self.ingredients, num_ingredients)
                portions = random.randint(20, 50)  # Number of portions needed
                
                problem = f"A restaurant needs to prepare {portions} portions of a dish. "
                problem += "The original recipe makes 8 portions and uses:\n"
                
                answers = []
                waste_factor = 1 + random.choice([0.1, 0.15, 0.2])  # 10-20% waste
                
                for ing, unit in ingredients:
                    # Generate realistic amounts based on ingredient type
                    if 'flour' in ing or 'sugar' in ing:
                        amount = random.choice(['2', '2 1/2', '3', '3 1/2', '4'])
                    elif 'milk' in ing or 'cream' in ing:
                        amount = random.choice(['1', '1 1/2', '2', '2 1/2', '3'])
                    else:
                        amount = random.choice(['1/4', '1/3', '1/2', '3/4', '1', '1 1/2'])
                    
                    problem += f"- {amount} {unit} {ing}\n"
                    
                    # Calculate scaled amount with waste factor
                    if ' ' in amount:
                        whole, frac = amount.split()
                        whole = int(whole)
                        num, denom = map(int, frac.split('/'))
                        base_amount = whole + Fraction(num, denom)
                    else:
                        if '/' in amount:
                            num, denom = map(int, amount.split('/'))
                            base_amount = Fraction(num, denom)
                        else:
                            base_amount = Fraction(int(amount))
                    
                    # Scale for portions and add waste
                    total = (base_amount * Fraction(portions, 8)) * Fraction(waste_factor).limit_denominator()
                    
                    # Convert to appropriate units (simplified for example)
                    if unit == 'cups' and total >= 4:
                        quarts = total // 4
                        cups = total % 4
                        if cups == 0:
                            answer = f"{quarts} qt {ing}"
                        else:
                            answer = f"{quarts} qt {cups.numerator}/{cups.denominator} cups {ing}"
                    else:
                        whole_part = total.numerator // total.denominator
                        remainder = total.numerator % total.denominator
                        
                        if remainder == 0:
                            answer = f"{whole_part} {unit} {ing}"
                        elif whole_part > 0:
                            answer = f"{whole_part} {remainder}/{total.denominator} {unit} {ing}"
                        else:
                            answer = f"{remainder}/{total.denominator} {unit} {ing}"
                    
                    answers.append(answer.strip())
                
                problem += f"\nAccounting for a {int((waste_factor-1)*100)}% waste factor, how much of each ingredient is needed? "
                problem += "Convert to larger units where appropriate."
                return problem, "\n".join(answers)
                
            elif problem_type == 'baking':
                # Baking problem with baker's percentages
                flour_amount = random.choice([500, 1000, 1500])  # grams
                ingredients = [
                    ('bread flour', 'g', 100),  # 100%
                    ('water', 'ml', random.randint(60, 75)),  # 60-75%
                    ('salt', 'g', 2),  # 2%
                    ('yeast', 'g', random.choice([1, 1.5, 2]))  # 1-2%
                ]
                
                problem = "A baker is making bread using baker's percentages. "
                problem += f"The recipe uses {flour_amount}g of flour as 100%. The other ingredients are:\n"
                
                answers = []
                for ing, unit, percent in ingredients[1:]:
                    amount = (flour_amount * percent) / 100
                    if unit == 'g' and amount < 1:  # Convert to mg for small amounts
                        answer = f"{int(amount * 1000)}mg {ing}"
                    else:
                        answer = f"{amount:.1f}{unit} {ing}"
                    
                    problem += f"- {percent}% {ing} (by weight of flour)\n"
                    answers.append(answer)
                
                problem += "\nCalculate the exact amounts needed for each ingredient."
                return problem, "\n".join(answers)
                
            else:  # catering
                # Catering problem with multiple dishes and shared ingredients
                dishes = [
                    ("pasta salad", 30, [
                        ("pasta", "oz", 8),
                        ("mayonnaise", "cups", 0.75),
                        ("vegetables", "cups", 2)
                    ]),
                    ("green salad", 25, [
                        ("lettuce", "heads", 2),
                        ("dressing", "cups", 0.5),
                        ("vegetables", "cups", 1.5)
                    ])
                ]
                
                problem = "A catering company is preparing the following dishes for an event:\n"
                total_ingredients = {}
                
                for dish_name, servings, ings in dishes:
                    problem += f"- {dish_name} (serves {servings}):\n"
                    for ing, unit, amt in ings:
                        problem += f"  - {amt} {unit} {ing}\n"
                        if (ing, unit) in total_ingredients:
                            total_ingredients[(ing, unit)] += amt
                        else:
                            total_ingredients[(ing, unit)] = amt
                
                problem += "\nIf you need to prepare enough food for 120 people, "
                problem += "how much of each ingredient will you need in total?"
                
                answers = []
                scale = 120 / sum(s for _, s, _ in dishes)  # Scale based on total servings
                
                for (ing, unit), amt in total_ingredients.items():
                    total = amt * scale
                    if unit == 'cups' and total >= 4:
                        quarts = int(total // 4)
                        cups = total % 4
                        if cups == 0:
                            answers.append(f"{quarts} qt {ing}")
                        else:
                            answers.append(f"{quarts} qt {cups:.1f} cups {ing}")
                    else:
                        answers.append(f"{total:.1f} {unit} {ing}")
                
                return problem, "\n".join(answers)
    
    def _generate_addition_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate fraction addition problems with increasing complexity."""
        if difficulty == 'easy':
            # Simple addition with like denominators and real-world context
            contexts = [
                ("baking", "cups", "flour"),
                ("pouring", "liters", "juice"),
                ("measuring", "meters", "fabric"),
                ("mixing", "cups", "sugar")
            ]
            action, unit, item = random.choice(contexts)
            
            denom = random.choice([2, 3, 4, 6, 8, 12])
            num1 = random.randint(1, denom-1)
            num2 = random.randint(1, denom-1)
            
            problem = f"While {action}, you use {num1}/{denom} {unit} of {item} and then add {num2}/{denom} {unit} more. "
            problem += f"How much {item} did you use in total?"
            
            result = Fraction(num1 + num2, denom)
            answer = self._format_fraction(result)
            return problem, f"{answer} {unit}"
            
        elif difficulty == 'medium':
            # Addition with unlike denominators and unit conversions
            contexts = [
                ("baking", [("flour", "cups"), ("sugar", "cups"), ("butter", "tablespoons")]),
                ("building a shelf", [("wood", "feet"), ("screws", "inches"), ("brackets", "")]),
                ("mixing paint", [("red", "cups"), ("blue", "cups"), ("white", "cups")])
            ]
            
            action, items = random.choice(contexts)
            item1, unit1 = random.choice(items)
            item2, unit2 = random.choice([i for i in items if i[0] != item1])
            
            # Generate fractions with different denominators
            denom1 = random.choice([2, 3, 4, 6, 8, 12])
            denom2 = random.choice([d for d in [2, 3, 4, 6, 8, 12] if d != denom1])
            num1 = random.randint(1, denom1-1)
            num2 = random.randint(1, denom2-1)
            
            # Convert to same unit if possible
            if unit1 == unit2:
                unit = unit1
                problem = f"For {action}, you need {num1}/{denom1} {unit} of {item1} and {num2}/{denom2} {unit} of {item2}. "
                problem += f"What's the total amount of {item1} and {item2} combined?"
                
                # Calculate result
                frac1 = Fraction(num1, denom1)
                frac2 = Fraction(num2, denom2)
                result = frac1 + frac2
                answer = self._format_fraction(result, mixed=True)
                return problem, f"{answer} {unit}"
            else:
                # Different units, keep them separate
                problem = f"For {action}, you need {num1}/{denom1} {unit1} of {item1} and {num2}/{denom2} {unit2} of {item2}. "
                problem += f"What's the total amount of materials you need?"
                
                answer = f"{num1}/{denom1} {unit1} of {item1} and {num2}/{denom2} {unit2} of {item2}"
                return problem, answer
                
        else:  # hard
            # Multi-step addition with mixed numbers and unit conversions
            scenario = random.choice(["construction", "cooking", "fabric", "time"])
            
            if scenario == "construction":
                lengths = [
                    (random.randint(1, 3), random.choice([2, 4, 8, 16])),  # feet and inches
                    (random.randint(1, 3), random.choice([2, 4, 8, 16])),
                    (random.randint(1, 3), random.choice([2, 4, 8, 16]))
                ]
                
                problem = "A carpenter has three pieces of wood: "
                problem += ", ".join([f"{f} feet {i} inches" for f, i in lengths])
                problem += ". What's the total length of all three pieces?"
                
                # Convert all to inches and add
                total_inches = sum(f * 12 + i for f, i in lengths)
                feet = total_inches // 12
                inches = total_inches % 12
                
                if inches == 0:
                    answer = f"{feet} feet"
                else:
                    answer = f"{feet} feet {inches} inches"
                    
                return problem, answer
                
            elif scenario == "cooking":
                # Recipe scaling with mixed numbers
                ingredients = [
                    ("flour", "cups", random.randint(2, 4)),
                    ("sugar", "cups", random.randint(1, 3)),
                    ("milk", "cups", random.randint(1, 2)),
                    ("eggs", "", random.randint(1, 4))
                ]
                
                # Original recipe serves 4, scale to random number
                servings = random.choice([6, 8, 10, 12])
                scale = Fraction(servings, 4)
                
                problem = f"A recipe serves 4 people and uses:\n"
                for ing, unit, amount in ingredients:
                    problem += f"- {amount} {unit} {ing}\n"
                problem += f"\nIf you want to serve {servings} people, how much of each ingredient do you need?"
                
                answers = []
                for ing, unit, amount in ingredients:
                    total = amount * scale
                    if unit:  # For items with units
                        if total.denominator == 1:
                            answers.append(f"{total.numerator} {unit} {ing}")
                        else:
                            answers.append(f"{total.numerator}/{total.denominator} {unit} {ing}")
                    else:  # For items without units (like eggs)
                        if total.denominator == 1:
                            answers.append(f"{total.numerator} {ing}")
                        else:
                            answers.append(f"{total.numerator}/{total.denominator} {ing}")
                
                return problem, "\n".join(answers)
                
            elif scenario == "fabric":
                # Adding fabric lengths with mixed units
                pieces = [
                    (random.randint(1, 3), random.choice([2, 4, 8, 16])),  # yards and feet
                    (random.randint(1, 3), random.choice([2, 4, 8, 12])),  # feet and inches
                    (random.randint(1, 3), random.choice([2, 4, 8, 16]))   # yards and feet
                ]
                
                problem = "A tailor has three pieces of fabric: "
                problem += ", ".join([f"{y} yards {f} feet" if i == 0 or i == 2 else f"{f} feet {i} inches" for i, (y, f) in enumerate(pieces)])
                problem += ". What's the total length in yards, feet, and inches?"
                
                # Convert all to inches and add
                total_inches = 0
                for i, (y, f) in enumerate(pieces):
                    if i == 1:  # feet and inches
                        total_inches += f * 12 + y  # y is actually inches here
                    else:  # yards and feet
                        total_inches += (y * 3 + f) * 12
                
                # Convert back to yards, feet, inches
                yards = total_inches // 36
                remaining_inches = total_inches % 36
                feet = remaining_inches // 12
                inches = remaining_inches % 12
                
                answer_parts = []
                if yards > 0:
                    answer_parts.append(f"{yards} yard{'s' if yards > 1 else ''}")
                if feet > 0:
                    answer_parts.append(f"{feet} foot{'s' if feet > 1 else ''}")
                if inches > 0 or not answer_parts:
                    answer_parts.append(f"{inches} inch{'es' if inches != 1 else ''}")
                
                return problem, " ".join(answer_parts)
                
            else:  # time
                # Adding time durations with hours, minutes, seconds
                durations = [
                    (random.randint(0, 2), random.randint(0, 59), random.randint(0, 59)),
                    (random.randint(0, 2), random.randint(0, 59), random.randint(0, 59)),
                    (random.randint(0, 2), random.randint(0, 59), random.randint(0, 59))
                ]
                
                problem = "Add the following time durations: "
                problem += ", ".join([f"{h} hour{'s' if h != 1 else ''} {m} minute{'s' if m != 1 else ''} {s} second{'s' if s != 1 else ''}" for h, m, s in durations])
                problem += ". What's the total duration?"
                
                # Calculate total seconds
                total_seconds = sum(h * 3600 + m * 60 + s for h, m, s in durations)
                
                # Convert back to hours, minutes, seconds
                hours = total_seconds // 3600
                remaining_seconds = total_seconds % 3600
                minutes = remaining_seconds // 60
                seconds = remaining_seconds % 60
                
                answer_parts = []
                if hours > 0:
                    answer_parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
                if minutes > 0 or hours > 0:  # Include minutes if there are hours, even if 0
                    answer_parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
                answer_parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
                
                return problem, " ".join(answer_parts)
    
    def _generate_sharing_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate problems about sharing items fairly with increasing complexity."""
        if difficulty == 'easy':
            # Sharing with fractional results and remainders
            items = [
                ("pizza", "slices", 8),
                ("chocolate bar", "pieces", 6),
                ("apple pie", "slices", 6),
                ("sandwich", "halves", 2)
            ]
            item, unit, parts = random.choice(items)
            
            # Choose number of people that doesn't divide evenly
            people = random.choice([3, 5, 7, 9])
            
            problem = f"You have {parts} {unit} of {item} to share equally among {people} people. "
            problem += f"How much {item} will each person get?"
            
            portion = Fraction(parts, people)
            
            if portion.denominator == 1:
                answer = f"{portion.numerator} {unit} each"
            else:
                answer = f"{portion.numerator}/{portion.denominator} of a {unit[:-1]} each"
                
            return problem, answer
            
        elif difficulty == 'medium':
            # Sharing with mixed numbers and unit conversions
            scenarios = [
                ("a rope", "feet", 12, 3, "Each piece should be cut to "),
                ("fabric", "yards", 5, 4, "Each piece should be "),
                ("ribbon", "feet", 8, 5, "Cut the ribbon into pieces of ")
            ]
            item, unit, total, people, prefix = random.choice(scenarios)
            
            problem = f"You have {total} {unit} of {item} that needs to be shared equally among {people} people. "
            problem += "What length should each piece be?"
            
            portion = Fraction(total, people)
            
            # Convert to mixed number
            whole = portion.numerator // portion.denominator
            remainder = portion.numerator % portion.denominator
            
            if remainder == 0:
                answer = f"{prefix}{whole} {unit}"
            elif whole > 0:
                answer = f"{prefix}{whole} {remainder}/{portion.denominator} {unit}"
            else:
                answer = f"{prefix}{portion.numerator}/{portion.denominator} {unit}"
                
            return problem, answer
            
        else:  # hard
            # Multi-step sharing with ratios and different portion sizes
            problem_type = random.choice(['sports', 'baking', 'construction'])
            
            if problem_type == 'sports':
                # Sports team sharing problem
                players = random.randint(12, 24)
                water_bottles = random.randint(3, 6)
                sports_drinks = random.randint(2, 4)
                
                problem = f"A sports team has {players} players. They have {water_bottles} full water bottles "
                problem += f"and {sports_drinks} full sports drink bottles to share. The coach wants to make sure "
                problem += "all players get the same amount of each drink. How much of each drink will each player receive?"
                
                water_per = Fraction(water_bottles, players)
                drink_per = Fraction(sports_drinks, players)
                
                answers = []
                for amount, drink in [(water_per, "water"), (drink_per, "sports drink")]:
                    whole = amount.numerator // amount.denominator
                    remainder = amount.numerator % amount.denominator
                    
                    if remainder == 0:
                        answers.append(f"{whole} bottles of {drink}")
                    elif whole > 0:
                        answers.append(f"{whole} {remainder}/{amount.denominator} bottles of {drink}")
                    else:
                        answers.append(f"{remainder}/{amount.denominator} of a bottle of {drink}")
                
                return problem, " and ".join(answers)
                
            elif problem_type == 'baking':
                # Baking ingredients sharing
                batches = random.randint(3, 6)
                people = random.randint(4, 8)
                
                problem = f"A baker made {batches} batches of cookies using a recipe that calls for 2 1/2 cups of flour "
                problem += f"and 3/4 cup of sugar per batch. The baker wants to divide all the cookies equally among {people} friends. "
                problem += "How much of each ingredient was used per friend's share?"
                
                total_flour = Fraction(5, 2) * batches  # 2 1/2 = 5/2
                total_sugar = Fraction(3, 4) * batches
                
                flour_per = total_flour / people
                sugar_per = total_sugar / people
                
                answers = []
                for amount, ingredient in [(flour_per, "flour"), (sugar_per, "sugar")]:
                    whole = amount.numerator // amount.denominator
                    remainder = amount.numerator % amount.denominator
                    
                    if remainder == 0:
                        answers.append(f"{whole} cups of {ingredient}")
                    elif whole > 0:
                        answers.append(f"{whole} {remainder}/{amount.denominator} cups of {ingredient}")
                    else:
                        answers.append(f"{remainder}/{amount.denominator} cup of {ingredient}")
                
                return problem, " and ".join(answers)
                
            else:  # construction
                # Construction materials sharing
                length = random.choice([16, 20, 24])  # feet
                cuts = random.randint(5, 8)
                
                problem = f"A {length}-foot wooden beam needs to be cut into {cuts} equal pieces. "
                problem += "If the saw blade makes a 1/8-inch wide cut each time, what will be the actual length "
                problem += "of each piece after accounting for the material lost to saw cuts?"
                
                total_cut_loss = Fraction(1, 8) * (cuts - 1)  # n-1 cuts for n pieces
                remaining_length = length * 12 - total_cut_loss  # convert feet to inches
                piece_length = remaining_length / cuts
                
                # Convert back to feet and inches
                inches = piece_length.numerator // piece_length.denominator
                remainder = piece_length.numerator % piece_length.denominator
                feet = inches // 12
                inches = inches % 12
                
                parts = []
                if feet > 0:
                    parts.append(f"{feet} foot" + ("s" if feet > 1 else ""))
                if inches > 0 or remainder > 0:
                    if remainder > 0:
                        inch_part = f"{inches} {remainder}/{piece_length.denominator}"
                    else:
                        inch_part = str(inches)
                    parts.append(f"{inch_part} inch" + ("" if inches == 1 and remainder == 0 else "es"))
                
                answer = " ".join(parts) + " per piece"
                return problem, answer
    
    def _generate_subtraction_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate fraction subtraction problems with real-world contexts and increasing complexity."""
        if difficulty == 'easy':
            # Real-world context with like denominators
            contexts = [
                ("A recipe calls for {0}/{2} cups of sugar. You use {1}/{2} cups. How much sugar is left?", "cups", "sugar"),
                ("A {0}/{2} liter bottle of juice has {1}/{2} liters left. How much was drunk?", "liters", "juice"),
                ("A piece of fabric is {0}/{2} meters long. You cut off {1}/{2} meters. How much remains?", "meters", "fabric"),
                ("You have {0}/{2} cups of flour and use {1}/{2} cups for baking. How much is left?", "cups", "flour")
            ]
            template, unit, item = random.choice(contexts)
            denom = random.choice([2, 3, 4, 6, 8, 12])
            # Ensure we have a valid range for num1 and num2
            num1 = random.randint(2, denom)  # Allow up to denom to get 1 as a result
            num2 = random.randint(1, min(num1, denom-1))  # Ensure num2 <= num1 and < denom
            
            problem = template.format(num1, num2, denom)
            result = Fraction(num1 - num2, denom)
            answer = self._format_fraction(result)
            return problem, answer
            
        elif difficulty == 'medium':
            # Unlike denominators with unit conversions
            denom1 = random.choice([2, 3, 4, 6, 8, 12])
            denom2 = random.choice([2, 3, 4, 6, 8, 12])
            while denom2 == denom1:  # Ensure different denominators
                denom2 = random.choice([2, 3, 4, 6, 8, 12])
                
            num1 = random.randint(1, denom1-1)
            num2 = random.randint(1, denom2-1)
            
            # Ensure first fraction is larger after conversion
            first = Fraction(num1, denom1)
            second = Fraction(num2, denom2)
            if first <= second:
                denom1, denom2 = denom2, denom1
                num1, num2 = num2, num1
                
            # Real-world context with unit conversion
            contexts = [
                ("A carpenter has a {0}/{1} foot board and cuts off {2}/{3} feet. How much remains?", "foot", "board"),
                ("A container has {0}/{1} gallons of water. {2}/{3} gallons are poured out. How much is left?", "gallon", "water"),
                ("A recipe needs {0}/{1} cups of milk but you only have {2}/{3} cups. How much more do you need?", "cup", "milk")
            ]
            template, unit, item = random.choice(contexts)
            problem = template.format(num1, denom1, num2, denom2)
            
            result = Fraction(num1, denom1) - Fraction(num2, denom2)
            answer = self._format_fraction(result)
            return problem, answer
            
        else:  # hard
            # Multi-step problems with mixed numbers and unit conversions
            problem_type = random.choice(['construction', 'cooking', 'fabric', 'time'])
            
            if problem_type == 'construction':
                # Construction scenario with feet and inches
                feet1 = random.randint(1, 3)
                inches1 = random.choice([0, 2, 4, 6, 8, 10])
                feet2 = random.randint(0, feet1-1)
                inches2 = random.choice([0, 2, 4, 6, 8, 10])
                
                problem = f"A board is {feet1} feet {inches1} inches long. You cut off {feet2} feet {inches2} inches. How much remains?"
                
                # Convert everything to inches
                total_inches1 = feet1 * 12 + inches1
                total_inches2 = feet2 * 12 + inches2
                remaining_inches = total_inches1 - total_inches2
                
                # Convert back to feet and inches
                feet = remaining_inches // 12
                inches = remaining_inches % 12
                
                answer_parts = []
                if feet > 0:
                    answer_parts.append(f"{feet} foot{'s' if feet > 1 else ''}")
                if inches > 0 or not answer_parts:
                    answer_parts.append(f"{inches} inch{'es' if inches != 1 else ''}")
                
                return problem, " ".join(answer_parts)
                
            elif problem_type == 'cooking':
                # Cooking scenario with recipe adjustments
                denom1 = random.choice([3, 4, 6, 8])
                denom2 = random.choice([2, 3, 4, 6, 8])
                num1 = random.randint(1, denom1-1)
                num2 = random.randint(1, denom2-1)
                
                ingredients = ['sugar', 'flour', 'milk', 'butter', 'oil']
                ingredient = random.choice(ingredients)
                
                problem = f"A recipe calls for 2 {num1}/{denom1} cups of {ingredient}. You use 1 {num2}/{denom2} cups. How much is left?"
                
                total1 = 2 + Fraction(num1, denom1)
                total2 = 1 + Fraction(num2, denom2)
                result = total1 - total2
                
                answer = self._format_fraction(result, mixed=True)
                return problem, f"{answer} cups"
                
            elif problem_type == 'fabric':
                # Fabric measurement with yards, feet, and inches
                yards1 = random.randint(1, 2)
                feet1 = random.randint(0, 2)
                inches1 = random.choice([0, 3, 6, 9])
                
                yards2 = random.randint(0, yards1-1)
                feet2 = random.randint(0, 2)
                inches2 = random.choice([0, 3, 6, 9])
                
                problem = f"A fabric is {yards1} yards {feet1} feet {inches1} inches long. You cut off {yards2} yards {feet2} feet {inches2} inches. How much remains?"
                
                # Convert everything to inches
                total_inches1 = (yards1 * 3 + feet1) * 12 + inches1
                total_inches2 = (yards2 * 3 + feet2) * 12 + inches2
                remaining_inches = total_inches1 - total_inches2
                
                # Convert back to yards, feet, inches
                total_feet, inches = divmod(remaining_inches, 12)
                yards, feet = divmod(total_feet, 3)
                
                answer_parts = []
                if yards > 0:
                    answer_parts.append(f"{yards} yard{'s' if yards > 1 else ''}")
                if feet > 0:
                    answer_parts.append(f"{feet} foot{'s' if feet > 1 else ''}")
                if inches > 0 or not answer_parts:
                    answer_parts.append(f"{inches} inch{'es' if inches != 1 else ''}")
                
                return problem, " ".join(answer_parts)
                
            else:  # time
                # Time subtraction with hours, minutes, seconds
                hours1 = random.randint(1, 5)
                minutes1 = random.randint(0, 59)
                seconds1 = random.choice([0, 15, 30, 45])
                
                hours2 = random.randint(0, hours1-1)
                minutes2 = random.randint(0, 59)
                seconds2 = random.choice([0, 15, 30, 45])
                
                problem = f"A task started at {hours1}:{minutes1:02d}:{seconds1:02d} and ended at {hours2}:{minutes2:02d}:{seconds2:02d}. How long did it take?"
                
                # Convert everything to seconds
                total_seconds1 = hours1 * 3600 + minutes1 * 60 + seconds1
                total_seconds2 = hours2 * 3600 + minutes2 * 60 + seconds2
                duration_seconds = total_seconds2 - total_seconds1
                
                # Convert back to hours, minutes, seconds
                hours, remainder = divmod(duration_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                
                answer_parts = []
                if hours > 0:
                    answer_parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
                if minutes > 0:
                    answer_parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
                if seconds > 0 or not answer_parts:
                    answer_parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
                
                return problem, " ".join(answer_parts)
    
    def _generate_multiplication_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate fraction multiplication problems with real-world applications."""
        if difficulty == 'easy':
            # Simple scaling with whole numbers and unit fractions
            contexts = [
                ("A recipe uses {0}/{2} cups of {1}. How much is needed for {3} batches?", 
                 ['flour', 'sugar', 'milk', 'oil'], 'cups'),
                ("A car travels {0}/{2} miles per hour. How far will it go in {3} hours?",
                 [], 'miles'),
                ("A bottle holds {0}/{2} liters of water. How much water is in {3} bottles?",
                 [], 'liters')
            ]
            
            template, items, unit = random.choice(contexts)
            denom = random.choice([2, 3, 4, 5, 10])
            num = random.randint(1, denom-1)
            multiplier = random.randint(2, 5)
            
            if items:
                item = random.choice(items)
            else:
                item = ""
                
            problem = template.format(num, item, denom, multiplier)
            result = Fraction(num * multiplier, denom)
            answer = self._format_fraction(result)
            return f"{problem} (in {unit})", f"{answer} {unit}"
            
        elif difficulty == 'medium':
            # Area and scaling with mixed numbers
            problem_type = random.choice(['area', 'scaling', 'time'])
            
            if problem_type == 'area':
                # Area of rectangles with fractional sides
                length_whole = random.randint(1, 3)
                length_num = random.randint(1, 3)
                length_denom = random.choice([2, 3, 4])
                width_whole = random.randint(1, 3)
                width_num = random.randint(1, 3)
                width_denom = random.choice([2, 3, 4])
                
                problem = (f"A rectangle has a length of {length_whole} {length_num}/{length_denom} units "
                          f"and a width of {width_whole} {width_num}/{width_denom} units. "
                          "What is its area?")
                
                length = length_whole + Fraction(length_num, length_denom)
                width = width_whole + Fraction(width_num, width_denom)
                result = length * width
                answer = self._format_fraction(result, mixed=True)
                return problem, f"{answer} square units"
                
            elif problem_type == 'scaling':
                # Recipe scaling with mixed numbers
                ingredient, unit = random.choice(self.ingredients)
                whole = random.randint(1, 3)
                num = random.randint(1, 3)
                denom = random.choice([2, 3, 4])
                scale_whole = random.randint(2, 4)
                scale_num = random.randint(1, 2)
                scale_denom = random.choice([2, 3, 4])
                
                problem = (f"A recipe calls for {whole} {num}/{denom} {unit} of {ingredient}. "
                          f"How much is needed for {scale_whole} {scale_num}/{scale_denom} times the recipe?")
                
                amount = whole + Fraction(num, denom)
                scale = scale_whole + Fraction(scale_num, scale_denom)
                result = amount * scale
                answer = self._format_fraction(result, mixed=True)
                return problem, f"{answer} {unit}"
                
            else:  # time
                # Time and rate problems
                rate_whole = random.randint(1, 3)
                rate_num = random.randint(1, 3)
                rate_denom = random.choice([2, 3, 4])
                time_whole = random.randint(1, 3)
                time_num = random.randint(1, 3)
                time_denom = random.choice([2, 3, 4])
                
                problem = (f"A machine produces {rate_whole} {rate_num}/{rate_denom} items per hour. "
                          f"How many items will it produce in {time_whole} {time_num}/{time_denom} hours?")
                
                rate = rate_whole + Fraction(rate_num, rate_denom)
                time = time_whole + Fraction(time_num, time_denom)
                result = rate * time
                answer = self._format_fraction(result, mixed=True)
                return problem, f"{answer} items"
                
        else:  # hard
            # Volume and complex scaling problems
            problem_type = random.choice(['volume', 'compound_scaling', 'multi_step'])
            
            if problem_type == 'volume':
                # Volume of rectangular prisms with mixed numbers
                length_whole = random.randint(1, 3)
                length_num = random.randint(1, 3)
                length_denom = random.choice([2, 3, 4])
                width_whole = random.randint(1, 3)
                width_num = random.randint(1, 3)
                width_denom = random.choice([2, 3, 4])
                height_whole = random.randint(1, 3)
                height_num = random.randint(1, 3)
                height_denom = random.choice([2, 3, 4])
                
                problem = (f"A box has dimensions {length_whole} {length_num}/{length_denom} ft × "
                          f"{width_whole} {width_num}/{width_denom} ft × "
                          f"{height_whole} {height_num}/{height_denom} ft. What is its volume?")
                
                length = length_whole + Fraction(length_num, length_denom)
                width = width_whole + Fraction(width_num, width_denom)
                height = height_whole + Fraction(height_num, height_denom)
                result = length * width * height
                answer = self._format_fraction(result, mixed=True)
                return problem, f"{answer} cubic feet"
                
            elif problem_type == 'compound_scaling':
                # Compound scaling with multiple ingredients
                num_ingredients = random.randint(2, 3)
                ingredients = random.sample(self.ingredients, num_ingredients)
                scale_whole = random.randint(2, 4)
                scale_num = random.randint(1, 2)
                scale_denom = random.choice([2, 3, 4])
                
                problem = "A recipe has the following ingredients:\n"
                amounts = []
                
                for i, (ing, unit) in enumerate(ingredients):
                    whole = random.randint(1, 2)
                    num = random.randint(1, 3)
                    denom = random.choice([2, 3, 4])
                    problem += f"- {whole} {num}/{denom} {unit} {ing}\n"
                    amounts.append(whole + Fraction(num, denom))
                
                problem += f"\nHow much of each ingredient is needed for {scale_whole} {scale_num}/{scale_denom} batches?\n"
                
                scale = scale_whole + Fraction(scale_num, scale_denom)
                answers = []
                
                for i, (ing, unit) in enumerate(ingredients):
                    result = amounts[i] * scale
                    answer = self._format_fraction(result, mixed=True)
                    answers.append(f"- {answer} {unit} {ing}")
                
                return problem, "\n".join(answers)
                
            else:  # multi_step
                # Multi-step problem with fractions and scaling
                ingredient1, unit1 = random.choice(self.ingredients)
                ingredient2, unit2 = random.choice([i for i in self.ingredients if i[0] != ingredient1])
                
                whole1 = random.randint(1, 2)
                num1 = random.randint(1, 3)
                denom1 = random.choice([2, 3, 4])
                whole2 = random.randint(1, 2)
                num2 = random.randint(1, 3)
                denom2 = random.choice([2, 3, 4])
                batches = random.randint(3, 5)
                
                problem = (f"A recipe calls for {whole1} {num1}/{denom1} {unit1} of {ingredient1} "
                          f"and {whole2} {num2}/{denom2} {unit2} of {ingredient2}. "
                          f"How much of each ingredient is needed for {batches} batches?")
                
                amount1 = (whole1 + Fraction(num1, denom1)) * batches
                amount2 = (whole2 + Fraction(num2, denom2)) * batches
                answer1 = self._format_fraction(amount1, mixed=True)
                answer2 = self._format_fraction(amount2, mixed=True)
                
                return problem, f"{answer1} {unit1} {ingredient1}\n{answer2} {unit2} {ingredient2}"
    
    def _generate_division_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate fraction division problems with real-world contexts."""
        if difficulty == 'easy':
            # Simple sharing or grouping problems
            contexts = [
                ("If you have {0}/{1} of a {2} and want to share it equally among {3} people, how much will each person get?",
                 ['pizza', 'cake', 'chocolate bar', 'pie']),
                ("A {0} meter rope is cut into pieces of {1}/{2} meters each. How many pieces can be made?",
                 [3, 4, 5, 6]),
                ("If a car travels {0}/{1} miles in {2} hours, what is its speed in miles per hour?",
                 [1, 2, 3, 4])
            ]
            
            template, items = random.choice(contexts)
            denom = random.choice([2, 3, 4, 5, 6, 8, 10, 12])
            num = random.randint(1, denom-1)
            divisor = random.randint(2, 6)
            
            if items and isinstance(items[0], str):
                item = random.choice(items)
                problem = template.format(num, denom, item, divisor)
            else:
                item = random.choice(items)
                problem = template.format(item, num, denom, divisor)
                
            result = Fraction(num, denom * divisor)
            answer = self._format_fraction(result)
            if 'speed' in problem:
                return problem, f"{answer} miles per hour"
            elif 'rope' in problem:
                return problem, f"{int((num/denom) / (1/divisor))} pieces"
            return problem, answer
            
        elif difficulty == 'medium':
            # Unit rate and scaling problems
            problem_type = random.choice(['unit_rate', 'scaling', 'measurement'])
            
            if problem_type == 'unit_rate':
                # Unit rate problems
                amount = random.randint(2, 5)
                denom = random.choice([2, 3, 4])
                num = random.randint(1, denom-1)
                unit = random.choice(['pounds', 'liters', 'cups', 'meters'])
                
                problem = (f"If {amount} {unit} of rice costs ${num}/{denom}, "
                         f"what is the cost per {unit}?")
                
                result = Fraction(num, denom * amount)
                answer = self._format_fraction(result)
                return problem, f"${answer} per {unit}"
                
            elif problem_type == 'scaling':
                # Recipe scaling problems
                ingredient, unit = random.choice(self.ingredients)
                whole = random.randint(1, 3)
                num = random.randint(1, 3)
                denom = random.choice([2, 3, 4])
                portions = random.randint(2, 4)
                
                problem = (f"A recipe uses {whole} {num}/{denom} {unit} of {ingredient} "
                         f"to make {portions} servings. How much {ingredient} is needed "
                         f"for 1 serving?")
                
                total = whole + Fraction(num, denom)
                result = total / portions
                answer = self._format_fraction(result, mixed=True)
                return problem, f"{answer} {unit}"
                
            else:  # measurement
                # Measurement conversion problems
                from_unit, to_unit = random.choice([
                    ('feet', 'inches'), ('pounds', 'ounces'), 
                    ('gallons', 'quarts'), ('hours', 'minutes')
                ])
                
                if from_unit == 'feet':
                    whole = random.randint(1, 4)
                    num = random.randint(1, 3)
                    denom = random.choice([2, 3, 4])
                    conversion = 12
                elif from_unit == 'pounds':
                    whole = random.randint(1, 3)
                    num = random.randint(1, 3)
                    denom = random.choice([2, 3, 4])
                    conversion = 16
                elif from_unit == 'gallons':
                    whole = random.randint(1, 2)
                    num = random.randint(1, 3)
                    denom = random.choice([2, 3, 4])
                    conversion = 4
                else:  # hours
                    whole = random.randint(1, 2)
                    num = random.randint(1, 2)
                    denom = random.choice([2, 3, 4])
                    conversion = 60
                
                problem = (f"Convert {whole} {num}/{denom} {from_unit} to {to_unit}. "
                         f"(1 {from_unit} = {conversion} {to_unit})")
                
                total = (whole + Fraction(num, denom)) * conversion
                answer = self._format_fraction(total, mixed=True)
                return problem, f"{answer} {to_unit}"
                
        else:  # hard
            # Multi-step and complex problems
            problem_type = random.choice(['multi_step', 'rate', 'sharing'])
            
            if problem_type == 'multi_step':
                # Multi-step problems with multiple operations
                ingredient1, unit1 = random.choice(self.ingredients)
                ingredient2, unit2 = random.choice([i for i in self.ingredients if i[0] != ingredient1])
                
                whole1 = random.randint(1, 2)
                num1 = random.randint(1, 3)
                denom1 = random.choice([2, 3, 4])
                whole2 = random.randint(1, 2)
                num2 = random.randint(1, 3)
                denom2 = random.choice([2, 3, 4])
                people = random.randint(3, 6)
                
                problem = (f"A recipe uses {whole1} {num1}/{denom1} {unit1} of {ingredient1} and "
                         f"{whole2} {num2}/{denom2} {unit2} of {ingredient2} to make a cake that "
                         f"serves {people} people. How much of each ingredient is needed per person?")
                
                amount1 = (whole1 + Fraction(num1, denom1)) / people
                amount2 = (whole2 + Fraction(num2, denom2)) / people
                answer1 = self._format_fraction(amount1, mixed=True)
                answer2 = self._format_fraction(amount2, mixed=True)
                
                return problem, f"{answer1} {unit1} {ingredient1}\n{answer2} {unit2} {ingredient2}"
                
            elif problem_type == 'rate':
                # Complex rate problems
                rate_whole = random.randint(1, 3)
                rate_num = random.randint(1, 3)
                rate_denom = random.choice([2, 3, 4])
                time_whole = random.randint(1, 2)
                time_num = random.randint(1, 3)
                time_denom = random.choice([2, 3, 4])
                
                problem = (f"A machine produces {rate_whole} {rate_num}/{rate_denom} items per hour. "
                         f"How long will it take to produce {time_whole} {time_num}/{time_denom} items? "
                         "(Answer in hours and minutes)")
                
                rate = rate_whole + Fraction(rate_num, rate_denom)
                items = time_whole + Fraction(time_num, time_denom)
                hours = items / rate
                
                # Convert to hours and minutes
                whole_hours = int(hours)
                minutes = int((hours - whole_hours) * 60)
                
                if whole_hours == 0:
                    answer = f"{minutes} minutes"
                elif minutes == 0:
                    answer = f"{whole_hours} hours"
                else:
                    answer = f"{whole_hours} hours and {minutes} minutes"
                
                return problem, answer
                
            else:  # sharing
                # Complex sharing problems with remainders
                item = random.choice(['pizza', 'cake', 'chocolate bar', 'pie'])
                people = random.randint(3, 6)
                whole = random.randint(1, 2)
                num = random.randint(1, 3)
                denom = random.choice([2, 3, 4])
                
                problem = (f"You have {whole} {num}/{denom} {item}s to share equally among {people} people. "
                         f"How much {item} will each person get?")
                
                total = whole + Fraction(num, denom)
                each = total / people
                answer = self._format_fraction(each, mixed=True)
                
                return problem, f"{answer} of a {item}"
    
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
        """Generate fraction comparison problems with real-world contexts."""
        max_attempts = 5  # Prevent infinite loops
        
        if difficulty == 'easy':
            # Real-world context with like denominators
            contexts = [
                ("You have {0}/{2} of a {3} and your friend has {1}/{2} of the same {3}. Who has more? (use >, <, or =)",
                 ['pizza', 'cake', 'chocolate bar', 'pie']),
                ("A plant grew {0}/{2} inches last week and {1}/{2} inches this week. Which week did it grow more? (use >, <, or =)",
                 None),
                ("You've completed {0}/{2} of your homework and your sibling has completed {1}/{2}. Who has completed more? (use >, <, or =)",
                 None)
            ]
            
            for _ in range(max_attempts):
                try:
                    template, items = random.choice(contexts)
                    denom = random.choice([2, 3, 4, 6, 8, 12])
                    num1 = random.randint(1, max(2, denom-1))  # Ensure at least 2 possible values
                    num2 = random.randint(1, max(2, denom-1))
                    
                    # Ensure they're different and not too close
                    if abs(num1 - num2) < 1 and denom > 3:  # If too close, try again
                        continue
                    
                    if items:
                        item = random.choice(items)
                        problem = template.format(min(num1, num2), max(num1, num2), denom, item)
                    else:
                        problem = template.format(min(num1, num2), max(num1, num2), denom)
                    
                    if num1 > num2:
                        answer = ">"
                    elif num1 < num2:
                        answer = "<"
                    else:
                        continue  # Shouldn't happen due to check above
                        
                    return problem, answer
                except Exception as e:
                    print(f"Error generating easy comparison problem: {e}")
                    continue
            
            # Fallback problem if all attempts fail
            return "Compare 1/2 and 3/4 (use >, <, or =)", "<"
            
        elif difficulty == 'medium':
            # Real-world context with different denominators
            contexts = [
                ("A recipe calls for {0}/{1} cups of {3} and another recipe needs {2}/{4} cups. Which recipe uses more {3}? (use >, <, or =)",
                 ['sugar', 'flour', 'milk', 'butter']),
                ("A car travels {0}/{1} miles on one gallon of gas and another car travels {2}/{3} miles. Which car has better mileage? (use >, <, or =)",
                 None),
                ("A plant grew {0}/{1} inches in the first week and {2}/{3} inches in the second week. When did it grow more? (use >, <, or =)",
                 None)
            ]
            
            for _ in range(max_attempts):
                try:
                    template, items = random.choice(contexts)
                    denom1 = random.choice([2, 3, 4, 6, 8, 12])
                    denom2 = denom1 * random.choice([2, 3, 4])
                    num1 = random.randint(1, max(2, denom1-1))
                    num2 = random.randint(1, max(2, denom2-1))
                    
                    # Calculate cross products to determine relationship
                    cross1 = num1 * denom2
                    cross2 = num2 * denom1
                    
                    # Ensure they're not too close
                    if abs(cross1 - cross2) < 1:
                        continue
                    
                    if items:
                        item = random.choice(items)
                        problem = template.format(num1, denom1, num2, denom2, item)
                    else:
                        problem = template.format(num1, denom1, num2, denom2)
                    
                    if cross1 > cross2:
                        answer = ">"
                    elif cross1 < cross2:
                        answer = "<"
                    else:
                        answer = "="
                    
                    return problem, answer
                except Exception as e:
                    print(f"Error generating medium comparison problem: {e}")
                    continue
            
            # Fallback problem if all attempts fail
            return "Compare 1/2 and 1/3 (use >, <, or =)", ">"
            
        else:  # hard
            # Real-world context with mixed numbers and improper fractions
            contexts = [
                ("A baker has {0} {1}/{2} cups of {5} and needs {3}/{4} cups for a recipe. Does the baker have enough? (use >, <, or =)",
                 ['sugar', 'flour', 'milk', 'butter'], 'ingredient'),
                ("A marathon runner completed {0} {1}/{2} miles in the first hour and {3}/{4} of the race in the second hour. When did they cover more distance? (use >, <, or =)",
                 None, 'distance'),
                ("A container has {0} {1}/{2} liters of water. If you pour out {3}/{4} liters, will there be any water left? (use >, <, or =)",
                 None, 'water')
            ]
            
            # Ensure we don't get stuck in a loop
            max_attempts = 10
            attempt = 0
            
            while attempt < max_attempts:
                template, items, context_type = random.choice(contexts)
                whole = random.randint(1, 3)
                denom1 = random.choice([3, 4, 5, 6, 8, 12])
                denom2 = random.choice([3, 4, 5, 6, 8, 12])
                num1 = random.randint(1, denom1-1)
                num2 = random.randint(1, denom2*2)  # Can be proper or improper
                
                # Calculate values for comparison
                value1 = whole + (num1 / denom1)
                value2 = num2 / denom2
                
                # Ensure we have a valid comparison (not too close)
                if abs(value1 - value2) < 0.1:  # If too close, try again
                    attempt += 1
                    continue
                    
                # Format the problem
                if items:
                    item = random.choice(items)
                    problem = template.format(whole, num1, denom1, num2, denom2, item)
                else:
                    problem = template.format(whole, num1, denom1, num2, denom2)
                
                # Determine the answer
                if abs(value1 - value2) < 0.0001:  # Account for floating point precision
                    answer = "="
                elif value1 > value2:
                    answer = ">"
                else:
                    answer = "<"
                
                # If we get here, we have a valid problem
                return problem, answer
            
            # If we've tried too many times, return a default problem
            return "Compare: 1 1/2 and 3/2 (use >, <, or =)", "="
                
            return problem, answer
    
    def _generate_conversion_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate problems involving fraction/decimal/percentage conversions with real-world contexts."""
        if difficulty == 'easy':
            # Real-world context for simple conversions
            contexts = [
                ("A recipe calls for {0}/{1} cups of {2}. Convert this fraction to a decimal.",
                 ['sugar', 'flour', 'milk', 'butter']),
                ("You've completed {0}/{1} of your homework. What decimal represents this fraction?",
                 None),
                ("A pie is cut into {1} equal slices. If you eat {0} slices, what decimal represents the portion you ate?",
                 None)
            ]
            
            template, items = random.choice(contexts)
            denom = random.choice([2, 4, 5, 10, 20, 25, 50, 100])
            num = random.randint(1, denom-1)
            
            if items:
                item = random.choice(items)
                problem = template.format(num, denom, item)
            else:
                problem = template.format(num, denom)
                
            answer = f"{num/denom:.3f}".rstrip('0').rstrip('.')
            if answer.endswith('.'):
                answer = answer[:-1]
                
            return problem, answer
            
        elif difficulty == 'medium':
            # Real-world context for mixed numbers and percentages
            problem_type = random.choice(['mixed_to_decimal', 'fraction_to_percent', 'measurement_conversion'])
            
            if problem_type == 'mixed_to_decimal':
                # Mixed numbers in measurement contexts
                contexts = [
                    ("A carpenter needs a board that is {0} {1}/{2} feet long. Convert this to a decimal.",
                     None),
                    ("A recipe calls for {0} {1}/{2} cups of {3}. Convert this to a decimal.",
                     ['sugar', 'flour', 'milk', 'butter']),
                    ("You walked {0} {1}/{2} miles today. Convert this distance to a decimal.",
                     None)
                ]
                
                template, items = random.choice(contexts)
                whole = random.randint(1, 5)
                denom = random.choice([2, 4, 5, 8, 10, 20, 25, 50])
                num = random.randint(1, denom-1)
                
                if items:
                    item = random.choice(items)
                    problem = template.format(whole, num, denom, item)
                else:
                    problem = template.format(whole, num, denom)
                
                decimal = whole + (num / denom)
                answer = f"{decimal:.3f}".rstrip('0').rstrip('.')
                if answer.endswith('.'):
                    answer = answer[:-1]
                return problem, answer
                
            elif problem_type == 'fraction_to_percent':
                # Real-world percentage problems
                contexts = [
                    ("In a survey, {0}/{1} of students prefer pizza. What percentage is this?",
                     None),
                    ("A test has {0} questions out of {1} correct. What percentage was scored?",
                     None),
                    ("A sale offers {0}/{1} off the original price. What percentage discount is this?",
                     None)
                ]
                
                template, _ = random.choice(contexts)
                denom = random.choice([2, 4, 5, 10, 20, 25, 50, 100])
                num = random.randint(1, denom-1)
                
                problem = template.format(num, denom)
                percentage = (num / denom) * 100
                if percentage == int(percentage):
                    answer = f"{int(percentage)}%"
                else:
                    answer = f"{percentage:.1f}%".replace(".0", "")
                return problem, answer
                
            else:  # measurement_conversion
                # Real-world measurement conversions
                conversions = [
                    ('feet', 'inches', 12),
                    ('pounds', 'ounces', 16),
                    ('gallons', 'quarts', 4),
                    ('hours', 'minutes', 60),
                    ('meters', 'centimeters', 100),
                    ('kilometers', 'meters', 1000)
                ]
                
                from_unit, to_unit, factor = random.choice(conversions)
                whole = random.randint(1, 5)
                denom = random.choice([2, 4, 5, 8, 10])
                num = random.randint(1, denom-1)
                
                problem = f"Convert {whole} {num}/{denom} {from_unit} to {to_unit}. (1 {from_unit} = {factor} {to_unit})"
                total = (whole + (num / denom)) * factor
                
                if total == int(total):
                    answer = f"{int(total)} {to_unit}"
                else:
                    answer = f"{total:.2f} {to_unit}".replace(".00", "")
                return problem, answer
                
        else:  # hard
            # Complex real-world conversion scenarios
            problem_type = random.choice(['repeating_decimal', 'multi_step_conversion', 'recipe_scaling'])
            
            if problem_type == 'repeating_decimal':
                # Repeating decimals in real-world contexts
                contexts = [
                    ("A repeating pattern occurs every {0} seconds. Express {1}/{2} of this interval as a decimal with repeating notation.",
                     [3, 6, 9, 12, 15]),
                    ("A wheel turns {1}/{2} of a full rotation. Express this as a decimal with repeating notation.",
                     None),
                    ("A recipe calls for {1}/{2} cups of {3}. Convert this to a decimal with repeating notation.",
                     ['sugar', 'flour', 'milk', 'butter'])
                ]
                
                template, items = random.choice(contexts)
                denom = random.choice([3, 6, 7, 9, 11, 12, 13, 15])
                num = random.randint(1, denom-1)
                
                if items and isinstance(items, list):
                    if items[0] in ['sugar', 'flour', 'milk', 'butter']:
                        item = random.choice(items)
                        problem = template.format("", num, denom, item)
                    else:
                        item = random.choice(items)
                        problem = template.format(item, num, denom)
                else:
                    problem = template.format("", num, denom)
                
                # Calculate repeating decimal
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
        """Generate problems with mixed operations on fractions in real-world contexts."""
        if difficulty == 'easy':
            # Real-world context with two operations (like denominators)
            contexts = [
                ("You have {0}/{3} of a pizza. You eat {1}/{3} and then get {2}/{3} more. How much pizza do you have now?",
                 ['+', '+']),
                ("A recipe calls for {0}/{3} cups of sugar. You add {1}/{3} cups and then remove {2}/{3} cups. How much sugar is left?",
                 ['+', '-']),
                ("A plant was {0}/{3} meters tall. It grew {1}/{3} meters and then another {2}/{3} meters. How tall is it now?",
                 ['+', '+'])
            ]
            
            template, ops = random.choice(contexts)
            denom = random.choice([2, 3, 4, 5, 6, 8, 10, 12])
            nums = [random.randint(1, denom-1) for _ in range(3)]
            
            # Ensure positive results for subtraction
            if '-' in ops:
                if ops[0] == '-' and nums[0] < nums[1]:
                    nums[0], nums[1] = nums[1], nums[0]
                if ops[1] == '-' and nums[0] + (1 if ops[0] == '+' else -1) * nums[1] < nums[2]:
                    nums[2] = random.randint(1, nums[0] + (1 if ops[0] == '+' else -1) * nums[1] - 1)
            
            problem = template.format(nums[0], nums[1], nums[2], denom)
            
            # Evaluate step by step
            if ops[0] == '+':
                step1 = Fraction(nums[0] + nums[1], denom)
            else:  # '-'
                step1 = Fraction(nums[0] - nums[1], denom)
                
            if ops[1] == '+':
                result = step1 + Fraction(nums[2], denom)
            else:  # '-'
                result = step1 - Fraction(nums[2], denom)
            
            answer = self._format_fraction(result, mixed=True)
            return problem, answer
            
        elif difficulty == 'medium':
            # Real-world context with two operations (unlike denominators)
            contexts = [
                ("A recipe needs {0}/{1} cups of flour and {2}/{3} cups of sugar. You double the recipe and then use {4}/{5} cups. How much is left?",
                 ['+', '×', '-']),
                ("A car travels {0}/{1} miles in an hour and {2}/{3} miles in the next hour. If it then travels {4}/{5} times that total distance, how far did it go?",
                 ['+', '×']),
                ("A tank has {0}/{1} gallons of water. {2}/{3} gallons are added, and then half of the total is used. How much water remains?",
                 ['+', '×']),
                ("A student studies {0}/{1} hours on Monday and {2}/{3} hours on Tuesday. On Wednesday, they study {4}/{5} of the previous total. How many hours did they study in total?",
                 ['+', '×'])
            ]
            
            template, ops = random.choice(contexts)
            
            # Generate appropriate denominators and numerators
            if random.random() < 0.5:
                denoms = [random.choice([2, 3, 4, 5, 6, 8, 10, 12]) for _ in range(3)]
            else:
                base_denom = random.choice([2, 3, 4, 5, 6, 8, 10, 12])
                denoms = [base_denom, base_denom * random.choice([2, 3]), base_denom]
                
            nums = [random.randint(1, d-1) for d in denoms]
            
            # Ensure reasonable results (positive, not too large)
            if ops[0] == '-':
                if Fraction(nums[0], denoms[0]) < Fraction(nums[1], denoms[1]):
                    nums[0], nums[1] = nums[1], nums[0]
            
            problem = template.format(nums[0], denoms[0], nums[1], denoms[1], nums[2], denoms[2])
            
            # Evaluate the expression
            frac1 = Fraction(nums[0], denoms[0])
            frac2 = Fraction(nums[1], denoms[1])
            frac3 = Fraction(nums[2], denoms[2])
            
            # First operation
            if ops[0] == '+':
                step1 = frac1 + frac2
            else:  # '-'
                step1 = frac1 - frac2
            
            # Second operation (handle both 2 and 3 operation cases)
            if len(ops) > 1:
                if ops[1] == '×':
                    if len(ops) > 2 and ops[2] == '-':
                        result = step1 * frac3 - frac3
                    else:
                        result = step1 * frac3
                else:  # ops[1] is '+'
                    if len(ops) > 2 and ops[2] == '×':
                        result = step1 + (frac2 * frac3)
                    else:
                        result = step1 + frac3
            else:
                result = step1
            
            answer = self._format_fraction(result, mixed=True)
            return problem, answer
            
        else:  # hard
            # Complex real-world scenarios with multiple operations
            scenarios = [
                self._generate_recipe_scaling_problem,
                self._generate_travel_problem,
                self._generate_construction_problem,
                self._generate_shopping_problem
            ]
            
            return random.choice(scenarios)()
    
    def _generate_recipe_scaling_problem(self) -> Tuple[str, str]:
        """Generate a recipe scaling problem with mixed operations."""
        ingredients = [
            ('flour', 'cups'),
            ('sugar', 'cups'),
            ('butter', 'tablespoons'),
            ('milk', 'cups'),
            ('eggs', '')
        ]
        ingredient, unit = random.choice(ingredients)
        
        # Original amounts
        whole1 = random.randint(1, 3)
        num1, denom1 = random.choice([(1,2), (1,3), (1,4), (2,3), (3,4)])
        
        # Scaling factors
        whole2 = random.randint(2, 4)
        num2, denom2 = random.choice([(1,2), (1,3), (2,3), (1,4), (3,4)])
        
        # Adjustment
        num3, denom3 = random.choice([(1,2), (1,3), (1,4), (1,8)])
        
        problem = f"A recipe calls for {whole1} {num1}/{denom1} {unit} of {ingredient}. "
        problem += f"You want to make {whole2} {num2}/{denom2} times the recipe, but then reduce the {ingredient} by {num3}/{denom3} {unit}. "
        problem += f"How much {ingredient} should you use?"
        
        # Calculate
        original = whole1 + Fraction(num1, denom1)
        scaled = original * (whole2 + Fraction(num2, denom2))
        adjusted = scaled - Fraction(num3, denom3)
        
        answer = self._format_fraction(adjusted, mixed=True)
        if unit:
            answer += f" {unit}"
            
        return problem, answer
    
    def _generate_travel_problem(self) -> Tuple[str, str]:
        """Generate a travel distance problem with mixed operations."""
        # Generate distances
        whole1 = random.randint(1, 4)
        num1, denom1 = random.choice([(1,2), (1,3), (2,3), (3,4)])
        whole2 = random.randint(1, 3)
        num2, denom2 = random.choice([(1,2), (1,3), (2,3), (1,4)])
        
        # Time fractions
        time_num, time_denom = random.choice([(1,2), (2,3), (3,4), (4,5)])
        
        problem = f"A train travels {whole1} {num1}/{denom1} miles in {time_num}/{time_denom} hours. "
        problem += f"It then travels {whole2} {num2}/{denom2} miles in the same amount of time. "
        problem += "What is the average speed for the entire trip in miles per hour?"
        
        # Calculate total distance
        dist1 = whole1 + Fraction(num1, denom1)
        dist2 = whole2 + Fraction(num2, denom2)
        total_dist = dist1 + dist2
        
        # Calculate total time
        total_time = 2 * Fraction(time_num, time_denom)
        
        # Calculate average speed
        avg_speed = total_dist / total_time
        
        answer = self._format_fraction(avg_speed, mixed=True) + " miles per hour"
        return problem, answer
    
    def _generate_construction_problem(self) -> Tuple[str, str]:
        """Generate a construction materials problem with mixed operations."""
        materials = [
            ('wood', 'feet', 'lengths'),
            ('pipe', 'feet', 'sections'),
            ('wire', 'feet', 'spools'),
            ('fabric', 'yards', 'pieces')
        ]
        material, unit, pieces = random.choice(materials)
        
        # Generate measurements
        whole1 = random.randint(5, 10)
        num1, denom1 = random.choice([(1,2), (1,3), (2,3), (3,4)])
        whole2 = random.randint(2, 4)
        num2, denom2 = random.choice([(1,2), (1,3), (2,3), (1,4)])
        
        problem = f"A builder needs {whole1} {num1}/{denom1} {unit} of {material}. "
        problem += f"The {material} comes in {whole2} {num2}/{denom2} {unit} {pieces}. "
        problem += f"How many {pieces} are needed, and how much will be left over?"
        
        # Calculate
        total_needed = whole1 + Fraction(num1, denom1)
        piece_size = whole2 + Fraction(num2, denom2)
        
        pieces_needed = (total_needed + piece_size - Fraction(1, 1000)) // 1  # Ceiling division
        total_purchased = pieces_needed * piece_size
        leftover = total_purchased - total_needed
        
        answer = f"{int(pieces_needed)} {pieces} needed, with {self._format_fraction(leftover, mixed=True)} {unit} left over"
        return problem, answer
    
    def _generate_shopping_problem(self) -> Tuple[str, str]:
        """Generate a shopping discount problem with mixed operations."""
        items = [
            ('shirt', 15, 25),
            ('book', 10, 30),
            ('toy', 20, 40),
            ('game', 30, 50)
        ]
        item, min_price, max_price = random.choice(items)
        
        # Generate prices and discount
        price1 = random.randint(min_price, max_price)
        price2 = random.randint(min_price, max_price)
        discount_num, discount_denom = random.choice([(1,4), (1,3), (1,2), (2,3)])
        
        problem = f"A store sells {item}s for ${price1} each. You buy 2 {item}s during a {discount_num}/{discount_denom} off sale. "
        problem += f"There's also a 10% tax on the discounted price. How much do you pay in total?"
        
        # Calculate total
        subtotal = 2 * price1
        discount = subtotal * Fraction(discount_num, discount_denom)
        discounted = subtotal - discount
        tax = discounted * Fraction(10, 100)
        total = discounted + tax
        
        # Convert to float for proper currency formatting
        total_float = float(total.numerator) / float(total.denominator)
        answer = f"${total_float:.2f}"
        return problem, answer
    
    def _generate_measurement_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate measurement problems involving fractions with real-world contexts."""
        if difficulty == 'easy':
            # Real-world contexts for simple measurement problems
            problems = [
                {
                    'template': "A piece of {item} is {w1} {n1}/{d} {unit} long. If you cut off {w2} {n2}/{d} {unit}, how much is left?",
                    'items': ['wood', 'fabric', 'rope', 'pipe'],
                    'units': ['feet', 'yards', 'meters'],
                    'wholes': [1, 2, 3],
                    'denominators': [2, 4, 8]
                },
                {
                    'template': "A recipe calls for {w1} {n1}/{d} {unit} of {item}. If you only have {w2} {n2}/{d} {unit}, how much more do you need?",
                    'items': ['flour', 'sugar', 'milk', 'oil'],
                    'units': ['cups', 'tablespoons'],
                    'wholes': [1, 2],
                    'denominators': [2, 3, 4]
                },
                {
                    'template': "A water tank has a capacity of {w1} {n1}/{d} gallons. It currently has {w2} {n2}/{d} gallons. How much more water can be added?",
                    'items': ['water'],
                    'units': ['gallon'],
                    'wholes': [5, 10, 15],
                    'denominators': [2, 4]
                }
            ]
            
            # Select a problem type and generate values
            problem_data = random.choice(problems)
            item = random.choice(problem_data['items'])
            unit = random.choice(problem_data['units'])
            whole1 = random.choice(problem_data['wholes'])
            whole2 = random.choice([w for w in problem_data['wholes'] if w < whole1] or [max(1, whole1-1)])
            denom = random.choice(problem_data['denominators'])
            num1 = random.randint(1, denom-1)
            num2 = random.randint(1, denom-1)
            
            # Format the problem string
            problem = problem_data['template'].format(
                item=item,
                w1=whole1, n1=num1, d=denom, unit=unit,
                w2=whole2, n2=num2
            )
            
            # Calculate the answer
            total = whole1 + Fraction(num1, denom)
            used = whole2 + Fraction(num2, denom)
            
            # Determine if we're subtracting or adding based on the problem type
            if 'cut' in problem or 'left' in problem:
                result = total - used
                answer = self._format_fraction(abs(result), mixed=True) + f" {unit}"
            elif 'more' in problem or 'added' in problem:
                result = total - used
                if result > 0:
                    answer = f"{self._format_fraction(result, mixed=True)} {unit} more needed"
                else:
                    answer = f"You have enough. You have {self._format_fraction(-result, mixed=True)} {unit} extra."
            else:
                result = used - total
                answer = self._format_fraction(abs(result), mixed=True) + f" {unit}"
            
            return problem, answer
            
        elif difficulty == 'medium':
            # More complex measurement problems with unit conversions
            problem_type = random.choice(['area_volume', 'conversion', 'time_distance'])
            
            if problem_type == 'area_volume':
                shapes = [
                    ('rectangle', 'area', 'square'),
                    ('box', 'volume', 'cubic'),
                    ('garden', 'area', 'square'),
                    ('swimming pool', 'volume', 'cubic')
                ]
                shape, measure, unit_prefix = random.choice(shapes)
                
                # Generate dimensions with fractions
                dims = []
                for _ in range(2 if 'area' in measure else 3):
                    whole = random.randint(1, 5)
                    num, den = random.choice([(1,2), (1,3), (2,3), (3,4), (1,4)])
                    dims.append((whole, num, den))
                
                if 'area' in measure:
                    l_whole, l_num, l_den = dims[0]
                    w_whole, w_num, w_den = dims[1]
                    problem = (f"Find the area of a {shape} with length {l_whole} {l_num}/{l_den} meters "
                              f"and width {w_whole} {w_num}/{w_den} meters.")
                    
                    length = l_whole + Fraction(l_num, l_den)
                    width = w_whole + Fraction(w_num, w_den)
                    result = length * width
                    unit = f"{unit_prefix} meters"
                    
                else:  # volume
                    l_whole, l_num, l_den = dims[0]
                    w_whole, w_num, w_den = dims[1]
                    h_whole, h_num, h_den = dims[2]
                    problem = (f"Find the volume of a {shape} with dimensions {l_whole} {l_num}/{l_den} ft × "
                              f"{w_whole} {w_num}/{w_den} ft × {h_whole} {h_num}/{h_den} ft.")
                    
                    length = l_whole + Fraction(l_num, l_den)
                    width = w_whole + Fraction(w_num, w_den)
                    height = h_whole + Fraction(h_num, h_den)
                    result = length * width * height
                    unit = f"{unit_prefix} feet"
                
                answer = f"{self._format_fraction(result, mixed=True)} {unit}"
                return problem, answer
                
            elif problem_type == 'conversion':
                # Unit conversion problems
                conversions = [
                    ('feet', 'inches', 12),
                    ('yards', 'feet', 3),
                    ('miles', 'feet', 5280),
                    ('gallons', 'quarts', 4),
                    ('pounds', 'ounces', 16),
                    ('hours', 'minutes', 60)
                ]
                from_unit, to_unit, factor = random.choice(conversions)
                
                whole = random.randint(1, 5)
                num, den = random.choice([(1,2), (1,3), (2,3), (3,4), (1,4)])
                
                problem = (f"Convert {whole} {num}/{den} {from_unit} to {to_unit}. "
                         f"(1 {from_unit} = {factor} {to_unit})")
                
                amount = whole + Fraction(num, den)
                result = amount * factor
                answer = self._format_fraction(result, mixed=True) + f" {to_unit}"
                
            else:  # time_distance
                # Time and distance problems
                speeds = [
                    ('walking', 'miles per hour', 2, 4),
                    ('biking', 'miles per hour', 8, 15),
                    ('driving', 'miles per hour', 25, 60),
                    ('running', 'kilometers per hour', 5, 12)
                ]
                activity, speed_unit, min_speed, max_speed = random.choice(speeds)
                
                time_whole = random.randint(1, 2)
                time_num, time_den = random.choice([(1,2), (1,3), (2,3), (3,4)])
                speed_whole = random.randint(min_speed, max_speed)
                speed_num, speed_den = random.choice([(0,1), (1,2), (1,3), (2,3)])
                
                problem = (f"If you are {activity} at a speed of {speed_whole} "
                         f"{f'{speed_num}/{speed_den} ' if speed_num > 0 else ''}{speed_unit} for "
                         f"{time_whole} {time_num}/{time_den} hours, how far will you travel?")
                
                time = time_whole + Fraction(time_num, time_den)
                speed = speed_whole + (Fraction(speed_num, speed_den) if speed_num > 0 else 0)
                distance = time * speed
                
                distance_whole = distance.numerator // distance.denominator
                distance_remainder = distance.numerator % distance.denominator
                
                if distance_remainder == 0:
                    answer = f"{distance_whole} {speed_unit.split()[0]}s"
                else:
                    answer = (f"{distance_whole} {distance_remainder}/{distance.denominator} "
                             f"{speed_unit.split()[0]}s")
            
            return problem, answer
                
        else:  # hard
            # Multi-step measurement problems with real-world applications
            problem_type = random.choice(['recipe_scaling', 'construction', 'fabric', 'garden', 'painting'])
            
            if problem_type == 'recipe_scaling':
                # Complex recipe scaling with multiple ingredients and unit conversions
                num_ingredients = random.randint(2, 4)
                ingredients = random.sample([
                    ('all-purpose flour', 'cups'),
                    ('granulated sugar', 'cups'),
                    ('brown sugar', 'cups'),
                    ('milk', 'cups'),
                    ('heavy cream', 'cups'),
                    ('butter', 'tablespoons'),
                    ('vegetable oil', 'tablespoons'),
                    ('eggs', ''),
                    ('vanilla extract', 'teaspoons')
                ], num_ingredients)
                
                # Original amounts (as fractions)
                original = {}
                for ing, unit in ingredients:
                    denom = random.choice([2, 3, 4, 6, 8])
                    num = random.randint(1, denom-1)
                    original[(ing, unit)] = Fraction(num, denom)
                
                # Scaling factor - more complex than simple multiplication
                scaling_options = [
                    ("double", 2),
                    ("triple", 3),
                    ("make 1.5 times", Fraction(3, 2)),
                    ("make 2.5 times", Fraction(5, 2)),
                    ("make 3/4 of", Fraction(3, 4)),
                    ("make 1 1/2 times", Fraction(3, 2))
                ]
                scale_desc, scale = random.choice(scaling_options)
                
                # Build problem with more context
                problem = (f"You're baking {random.choice(['cookies', 'a cake', 'muffins', 'bread'])} "
                         f"and need to {scale_desc} the recipe. The original recipe calls for:\n")
                
                for (ing, unit), amount in original.items():
                    if amount.denominator == 1:
                        problem += f"- {amount.numerator} {unit} {ing}\n"
                    else:
                        problem += f"- {amount.numerator}/{amount.denominator} {unit} {ing}\n"
                
                problem += (f"\nCalculate the new amounts needed for each ingredient. "
                          f"Simplify all fractions to lowest terms.")
                
                # Calculate and format answers
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
                            amount_str = f"{whole} {Fraction(remainder, total.denominator)}"
                    
                    unit_str = f" {unit}" if unit else ""
                    answers.append(f"- {amount_str}{unit_str} {ing}")
                
                return problem, "\n".join(answers)
                
            elif problem_type == 'construction':
                # Complex construction problem with multiple materials and waste calculation
                materials = [
                    ('wooden planks', 'feet', 8, 12),  # name, unit, min_length, max_length
                    ('PVC pipes', 'feet', 4, 10),
                    ('electrical wire', 'feet', 6, 15),
                    ('metal rods', 'feet', 3, 8)
                ]
                material, unit, min_len, max_len = random.choice(materials)
                
                # Generate random lengths with fractions
                def random_mixed():
                    whole = random.randint(1, 3)
                    num, den = random.choice([(1,2), (1,3), (2,3), (1,4), (3,4)])
                    return f"{whole} {num}/{den}"
                
                pieces = [random_mixed() for _ in range(random.randint(2, 4))]
                
                # Calculate total length needed
                def parse_mixed(mixed):
                    parts = mixed.split()
                    if len(parts) == 1:
                        return Fraction(parts[0])
                    whole, frac = parts
                    return int(whole) + Fraction(frac)
                
                total_needed = sum(parse_mixed(p) for p in pieces)
                
                # Add waste percentage (5-15%)
                waste_percent = random.randint(5, 15)
                total_with_waste = total_needed * (1 + waste_percent/100)
                
                # Standard lengths available
                standard_lengths = [8, 10, 12, 16]
                standard_length = random.choice(standard_lengths)
                
                # Calculate how many standard lengths needed
                num_standard = (total_with_waste + standard_length - 1) // standard_length  # Ceiling division
                
                problem = (
                    f"You're building a {random.choice(['deck', 'fence', 'shelving unit', 'play structure'])} "
                    f"and need the following pieces of {material}:\n"
                )
                problem += "\n".join(f"- {p} {unit}" for p in pieces)
                problem += (
                    f"\n\nThe {material} comes in {standard_length}-{unit} lengths. "
                    f"You need to add {waste_percent}% for waste and mistakes.\n"
                    f"How many {standard_length}-{unit} pieces of {material} should you buy?"
                )
                
                return problem, f"{num_standard} pieces"
                
            elif problem_type == 'fabric':
                # Complex fabric problem with multiple conversions and calculations
                fabric_types = [
                    ('cotton', 'yards'),
                    ('silk', 'meters'),
                    ('upholstery', 'yards'),
                    ('fleece', 'meters')
                ]
                fabric, unit = random.choice(fabric_types)
                
                # Generate project requirements
                projects = []
                total_needed = 0
                
                for _ in range(random.randint(2, 4)):
                    project_type = random.choice(['curtains', 'pillows', 'tablecloth', 'dress', 'shirt'])
                    amount = random.choice([0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3])
                    projects.append((project_type, amount))
                    total_needed += amount
                
                # Convert to fractions for better display
                def float_to_mixed(f):
                    whole = int(f)
                    frac = f - whole
                    if frac == 0:
                        return str(whole)
                    return f"{whole} {Fraction(frac).limit_denominator()}"
                
                # Build problem
                problem = (
                    f"You're making {len(projects)} items from {fabric} fabric (sold by the {unit}):\n"
                )
                for i, (item, amt) in enumerate(projects, 1):
                    problem += f"{i}. {item.capitalize()}: {float_to_mixed(amt)} {unit}"
                    if i < len(projects):
                        problem += "\n"
                
                # Add additional requirements
                problem += (
                    f"\n\nThe fabric is 60 inches wide. You need to add 10% for pattern matching "
                    f"and mistakes. The fabric store sells by the 1/4 {unit}.\n"
                    f"How much fabric should you buy?"
                )
                
                # Calculate answer
                total_with_extra = total_needed * 1.1
                # Round up to nearest 0.25
                buy_amount = math.ceil(total_with_extra * 4) / 4
                
                # Format answer nicely
                if buy_amount == int(buy_amount):
                    answer = f"{int(buy_amount)} {unit}"
                else:
                    whole = int(buy_amount)
                    frac = Fraction(buy_amount - whole).limit_denominator(4)
                    answer = f"{whole} {frac} {unit}".replace(" ", "", 1)  # Remove space if whole is 0
                
                return problem, answer
                
            elif problem_type == 'garden':
                # Garden planning with area calculations
                garden_type = random.choice(['vegetable', 'flower', 'herb'])
                
                # Garden dimensions with fractions
                length_whole = random.randint(5, 10)
                width_whole = random.randint(3, 8)
                l_num, l_den = random.choice([(1,2), (1,3), (2,3), (3,4)])
                w_num, w_den = random.choice([(1,2), (1,3), (2,3), (3,4)])
                
                # Plant spacing requirements
                plant_type = random.choice([
                    ('tomatoes', 'plants', 3, 4),  # name, unit, spacing (ft), depth (in)
                    ('carrots', 'seeds', 0.5, 0.25),
                    ('lettuce', 'plants', 1, 0.25),
                    ('sunflowers', 'plants', 2, 1),
                    ('basil', 'plants', 1, 0.25)
                ])
                plant_name, plant_unit, spacing, depth = plant_type
                
                # Calculate area
                length = length_whole + Fraction(l_num, l_den)
                width = width_whole + Fraction(w_num, w_den)
                area = length * width
                
                # Calculate number of plants
                plants_per_row = int(float(length) / spacing)
                num_rows = int(float(width) / spacing)
                total_plants = plants_per_row * num_rows
                
                # Calculate soil needed (convert depth to feet)
                depth_ft = Fraction(depth) / 12
                soil_needed = area * depth_ft  # in cubic feet
                
                # Bags of soil (2 cubic feet per bag)
                bags_needed = math.ceil(float(soil_needed) / 2)
                
                problem = (
                    f"You're planning a {garden_type} garden that is {length_whole} {l_num}/{l_den} feet long "
                    f"and {width_whole} {w_num}/{w_den} feet wide. You want to plant {plant_name} "
                    f"with {spacing}-foot spacing between {plant_unit}. Each {plant_name} needs a {depth}-inch "
                    f"layer of soil. Bags of soil are 2 cubic feet each.\n\n"
                    f"1. How many {plant_name} {plant_unit} can you fit in the garden?\n"
                    f"2. How many bags of soil should you buy?"
                )
                
                answer = (
                    f"1. {total_plants} {plant_name} {plant_unit}\n"
                    f"2. {bags_needed} bags of soil"
                )
                
                return problem, answer
                
            else:  # painting
                # Room painting calculation with doors and windows
                room_types = [
                    ('bedroom', 10, 12, 8),
                    ('living room', 14, 16, 9),
                    ('kitchen', 12, 10, 8),
                    ('bathroom', 8, 10, 8)
                ]
                room, length, width, height = random.choice(room_types)
                
                # Add fractions to dimensions
                l_frac = random.choice([0, 0.5])
                w_frac = random.choice([0, 0.25, 0.5, 0.75])
                h_frac = random.choice([0, 0.25, 0.5])
                
                # Calculate total wall area
                length_total = length + l_frac
                width_total = width + w_frac
                height_total = height + h_frac
                
                wall_area = 2 * (length_total + width_total) * height_total
                
                # Subtract doors and windows
                num_doors = random.randint(1, 2)
                door_area = num_doors * 21  # 3x7 feet doors
                
                num_windows = random.randint(1, 3)
                window_area = num_windows * 10  # 2.5x4 feet windows
                
                total_area = wall_area - door_area - window_area
                
                # Paint coverage (1 gallon covers ~350 sq ft)
                gallons_needed = total_area / 350
                
                # Round up to nearest quart (4 quarts per gallon)
                quarts_needed = math.ceil(gallons_needed * 4)
                gallons = quarts_needed // 4
                quarts = quarts_needed % 4
                
                problem = (
                    f"You're painting a {room} that is {length}{' ' + str(Fraction(l_frac)) if l_frac > 0 else ''} feet long, "
                    f"{width}{' ' + str(Fraction(w_frac)) if w_frac > 0 else ''} feet wide, and "
                    f"{height}{' ' + str(Fraction(h_frac)) if h_frac > 0 else ''} feet high. "
                    f"The room has {num_doors} door(s) and {num_windows} window(s). "
                    f"One gallon of paint covers 350 square feet. Paint is sold in 1-gallon or 1-quart cans.\n\n"
                    f"How many gallons and quarts of paint should you buy to put two coats of paint on the walls?"
                )
                
                # Format answer
                answer_parts = []
                if gallons > 0:
                    answer_parts.append(f"{gallons} gallon{'s' if gallons > 1 else ''}")
                if quarts > 0:
                    answer_parts.append(f"{quarts} quart{'s' if quarts > 1 else ''}")
                
                return problem, " and ".join(answer_parts)

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
