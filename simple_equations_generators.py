"""
Simple Equations Word Problem Generators for Grade 7 Math

This module provides a collection of word problem generators focused on simple equations.
The problems are designed to help students practice setting up and solving equations
in various real-world contexts.

Last updated: 2025-07-27
"""
import random
from typing import Tuple, Union, Dict, Any
from dataclasses import dataclass

@dataclass
class Problem:
    """Container class for a generated problem and its solution."""
    statement: str
    answer: Union[int, float, str]
    solution_steps: list[str]
    difficulty: str
    problem_type: str

class SimpleEquationsGenerator:
    """
    A class to generate word problems involving simple equations.
    Problems are designed for 7th grade students with intermediate to hard difficulty.
    """
    
    def __init__(self):
        """Initialize the problem generator with common problem templates and settings."""
        self.difficulty_levels = ['intermediate', 'hard']
        self.currencies = {
            'USD': ('dollar', 'dollars'),
            'EUR': ('euro', 'euros'),
            'GBP': ('pound', 'pounds'),
            'INR': ('rupee', 'rupees'),
            'JPY': ('yen', 'yen')
        }
        self.items = {
            'stationery': ['pencil', 'pen', 'eraser', 'ruler', 'notebook', 'book'],
            'food': ['apple', 'banana', 'sandwich', 'chocolate bar', 'soda'],
            'clothing': ['shirt', 'pants', 'hat', 'socks', 'shoes']
        }
        
    def generate_problem(self, problem_type: str = None, difficulty: str = None) -> Problem:
        """
        Generate a word problem of the specified type and difficulty.
        
        Args:
            problem_type: Type of problem to generate. If None, a random type is selected.
                         Currently supports 'age_related', 'number', 'consecutive_integers', etc.
            difficulty: 'intermediate' or 'hard'. If None, a random level is selected.
                       Note: Not all problem types use this parameter.
            
        Returns:
            Problem object containing the problem statement, answer, solution steps,
            difficulty level, and problem type.
            
        Raises:
            ValueError: If an unimplemented problem type is requested.
        """
        # Map problem types to their respective generator methods and whether they use difficulty
        problem_generators = {
            # Age-related problems - use age_related_sum as the default age_related problem
            'age_related': (self._generate_age_sum_problem, False),
            'age_related_sum': (self._generate_age_sum_problem, False),
            'age_related_difference': (self._generate_age_difference_problem, False),
            'age_related_ratio': (self._generate_age_ratio_problem, False),
            'age_related_ratio_change': (self._generate_age_ratio_change_problem, True),
            'age_related_three_people': (self._generate_age_three_people_problem, True),
            'age_related_combined': (self._generate_age_combined_conditions_problem, True),
            
            # Number problems
            'number': (self._generate_basic_number_problem, False),
            'consecutive_integers': (self._generate_consecutive_integers_problem, False),
            'number_reversal': (self._generate_number_reversal_problem, False),
            
            # Money problems
            'money_basic': (self._generate_basic_money_problem, False),
            'money_discount': (self._generate_discount_problem, False),
            'money_profit_loss': (self._generate_profit_loss_problem, False),
            
            # Geometry problems
            'geometry': (self._generate_geometry_problem, False),
            'rectangle_perimeter': (self._generate_rectangle_perimeter_problem, False),
            'rectangle_area': (self._generate_rectangle_area_problem, False),
            'square_perimeter': (self._generate_square_perimeter_problem, False),
            'square_area': (self._generate_square_area_problem, False),
            'triangle_perimeter': (self._generate_triangle_perimeter_problem, False),
            'triangle_area': (self._generate_triangle_area_problem, False),
            'circle_circumference': (self._generate_circle_circumference_problem, False),
            'circle_area': (self._generate_circle_area_problem, False),
            'geometry': (self._generate_geometry_problem, False),  # Random geometry problem
            
            # Mixture problems
            'mixture_solution': (self._generate_mixture_problem, True),  # True indicates it uses difficulty
            'mixture_alloy': (self._generate_mixture_problem, True),
            'mixture_ingredients': (self._generate_mixture_problem, True),
            'mixture': (self._generate_mixture_problem, True),  # Random mixture problem
            
            # Work and Rate problems
            'work_rate': (self._generate_work_rate_problem, False),  # Random work rate problem
            'work_rate_basic': (lambda diff=None: self._generate_work_rate_problem('basic'), False),
            'work_rate_combined': (lambda diff=None: self._generate_work_rate_problem('combined'), False),
            'work_rate_efficiency': (lambda diff: self._generate_work_rate_problem('efficiency', diff), True),
            
            # Distance, Rate, and Time problems
            'drt': (self._generate_drt_problem, False),  # Random DRT problem
            'drt_basic': (lambda diff=None: self._generate_drt_problem('basic', diff) if diff else self._generate_drt_problem('basic'), True),
            'drt_two_objects': (lambda diff=None: self._generate_drt_problem('two_objects', diff) if diff else self._generate_drt_problem('two_objects'), True),
            'drt_relative_speed': (lambda diff: self._generate_drt_problem('relative_speed', diff), True),
            
            # Shopping and Budgeting problems
            'shopping': (lambda diff=None: self._generate_shopping_budget_problem(), False),  # Random shopping problem
            'shopping_max_quantity': (lambda diff=None: self._generate_shopping_budget_problem('shopping_max_quantity'), False),
            'shopping_remaining_money': (lambda diff=None: self._generate_shopping_budget_problem('shopping_remaining_money'), False),
            'shopping_max_price': (lambda diff=None: self._generate_shopping_budget_problem('shopping_max_price'), False)
        }
        
        if problem_type is None:
            # Only select from implemented problem types
            problem_type = random.choice(list(problem_generators.keys()))
        
        if difficulty is None:
            difficulty = random.choice(self.difficulty_levels)
        
        if problem_type not in problem_generators:
            raise ValueError(f"Problem type '{problem_type}' is not implemented. "
                          f"Available types: {list(problem_generators.keys())}")
        
        generator_func, uses_difficulty = problem_generators[problem_type]
        if uses_difficulty:
            # Special handling for mixture problems to pass the specific type
            if problem_type.startswith('mixture_'):
                if problem_type == 'mixture':
                    return generator_func(problem_type=None, difficulty=difficulty)
                else:
                    return generator_func(problem_type=problem_type, difficulty=difficulty)
            return generator_func(difficulty)
        else:
            return generator_func()
    
    def _generate_basic_number_problem(self) -> Problem:
        """Generate a basic number relationship problem."""
        x = random.randint(1, 50)
        operations = [
            (lambda a, b: a + b, 'added to'),
            (lambda a, b: a - b, 'subtracted from'),
            (lambda a, b: a * b, 'multiplied by'),
            (lambda a, b: a * b, 'times')  # Alternative wording
        ]
        
        # Randomly select operation and constants
        operation, op_text = random.choice(operations)
        constant = random.randint(2, 10)
        result = operation(constant, x)
        
        # Ensure result is positive for subtraction
        if operation == (lambda a, b: a - b):
            x = random.randint(constant + 1, 50)
            result = x - constant
        
        # Format the problem statement
        statement = f"If {constant} is {op_text} a number, the result is {result}. Find the number."
        
        return Problem(
            statement=statement,
            answer=x,
            solution_steps=[
                f"Let the number be x.",
                f"The equation is: {constant} {op_text.replace('subtracted from', 'subtracted from x equals').replace('added to', 'plus x equals').replace('multiplied by', 'times x equals').replace('times', 'times x equals')} {result}",
                f"Simplify: {constant} {op_text.replace('subtracted from', '= x -').replace('added to', '+ x =').replace('multiplied by', '× x =').replace('times', '× x =')} {result}",
                f"Solve for x: x = {x}"
            ],
            difficulty='intermediate',
            problem_type='basic_number_relationship'
        )
        
    def _generate_consecutive_integers_problem(self) -> Problem:
        """Generate a problem about consecutive integers."""
        problem_type = random.choice([
            'two_consecutive',
            'three_consecutive',
            'consecutive_even_odd'
        ])
        
        if problem_type == 'two_consecutive':
            # Problem: The sum of two consecutive integers is X. Find the integers.
            x = random.randint(10, 100)
            total = x + (x + 1)
            return Problem(
                statement=f"The sum of two consecutive integers is {total}. Find the smaller integer.",
                answer=x,
                solution_steps=[
                    "Let the smaller integer be x.",
                    f"Then the next consecutive integer is x + 1.",
                    f"The equation is: x + (x + 1) = {total}",
                    f"Simplify: 2x + 1 = {total}",
                    f"2x = {total - 1}",
                    f"x = {x}"
                ],
                difficulty='hard',
                problem_type='consecutive_integers_sum'
            )
            
        elif problem_type == 'three_consecutive':
            # Problem: The sum of three consecutive integers is X. Find the middle integer.
            middle = random.randint(10, 50)
            total = (middle - 1) + middle + (middle + 1)
            return Problem(
                statement=f"The sum of three consecutive integers is {total}. Find the middle integer.",
                answer=middle,
                solution_steps=[
                    "Let the middle integer be x.",
                    "Then the three consecutive integers are (x - 1), x, and (x + 1).",
                    f"The equation is: (x - 1) + x + (x + 1) = {total}",
                    f"Simplify: 3x = {total}",
                    f"x = {middle}"
                ],
                difficulty='hard',
                problem_type='three_consecutive_integers_sum'
            )
            
        else:  # consecutive_even_odd
            # Problem: Find two consecutive even/odd integers that add up to X
            is_even = random.choice([True, False])
            type_str = 'even' if is_even else 'odd'
            x = random.randint(5, 25) * 2  # Ensures even number
            if not is_even:
                x += 1  # Make it odd if needed
                
            total = x + (x + 2)
            
            return Problem(
                statement=f"The sum of two consecutive {type_str} integers is {total}. Find the smaller integer.",
                answer=x,
                solution_steps=[
                    f"Let the smaller {type_str} integer be x.",
                    f"Then the next consecutive {type_str} integer is x + 2.",
                    f"The equation is: x + (x + 2) = {total}",
                    f"Simplify: 2x + 2 = {total}",
                    f"2x = {total - 2}",
                    f"x = {x}"
                ],
                difficulty='hard',
                problem_type=f'consecutive_{type_str}_integers'
            )
            
    def _generate_number_reversal_problem(self) -> Problem:
        """Generate a number reversal problem."""
        # Generate a two-digit number
        tens = random.randint(1, 9)  # 1-9 (can't be 0 for a two-digit number)
        units = random.randint(0, 9)
        original_num = 10 * tens + units
        reversed_num = 10 * units + tens
        
        # Choose between sum or difference problem
        if random.choice([True, False]):
            # Sum problem: original + reversed = sum
            total = original_num + reversed_num
            statement = (f"The sum of a two-digit number and the number obtained by reversing its digits is {total}. "
                       f"If the tens digit is {tens - units} more than the units digit, find the original number.")
            
            solution_steps = [
                "Let the units digit be u and the tens digit be t.",
                f"The original number is 10t + u, and the reversed number is 10u + t.",
                f"Given: t = u + {tens - units}  (tens digit is {tens - units} more than units digit)",
                f"The sum of the numbers: (10t + u) + (10u + t) = 11t + 11u = {total}",
                f"Divide both sides by 11: t + u = {total // 11}",
                f"Substitute t from the first equation: (u + {tens - units}) + u = {total // 11}",
                f"2u + {tens - units} = {total // 11}",
                f"2u = {total // 11 - (tens - units)}",
                f"u = {units}",
                f"Then t = u + {tens - units} = {tens}",
                f"Therefore, the original number is {original_num}."
            ]
            
            return Problem(
                statement=statement,
                answer=original_num,
                solution_steps=solution_steps,
                difficulty='hard',
                problem_type='number_reversal_sum'
            )
        else:
            # Difference problem: |original - reversed| = difference
            difference = abs(original_num - reversed_num)
            statement = (f"The difference between a two-digit number and the number obtained by reversing "
                        f"its digits is {difference}. If the tens digit is {tens - units} more than the "
                        f"units digit, find the original number.")
            
            solution_steps = [
                "Let the units digit be u and the tens digit be t.",
                f"The original number is 10t + u, and the reversed number is 10u + t.",
                f"Given: t = u + {tens - units}  (tens digit is {tens - units} more than units digit)",
                f"The difference between the numbers: |(10t + u) - (10u + t)| = |9t - 9u| = {difference}",
                f"Divide both sides by 9: |t - u| = {difference // 9}",
                f"Since t > u, we have: t - u = {difference // 9}",
                f"But from the problem, t - u = {tens - units}. This must equal {difference // 9}.",
                f"Therefore, the original number is {original_num}."
            ]
            
            return Problem(
                statement=statement,
                answer=original_num,
                solution_steps=solution_steps,
                difficulty='hard',
                problem_type='number_reversal_difference'
            )
            
    def _generate_basic_money_problem(self) -> Problem:
        """Generate a basic money problem involving simple transactions."""
        # Choose a random currency
        currency_code = random.choice(list(self.currencies.keys()))
        currency_single, currency_plural = self.currencies[currency_code]
        
        # Choose between different types of basic money problems
        problem_type = random.choice(['total_cost', 'change', 'multiple_items'])
        
        if problem_type == 'total_cost':
            # Problem type: You have X money and buy Y items costing Z each
            item = random.choice(self.items['stationery'])
            item_cost = random.randint(2, 20)
            quantity = random.randint(2, 5)
            total_cost = item_cost * quantity
            
            statement = f"If one {item} costs {item_cost} {currency_plural}, " \
                       f"how much do {quantity} {item}s cost?"
            
            solution_steps = [
                f"Cost of one {item} = {item_cost} {currency_plural}",
                f"Number of {item}s = {quantity}",
                f"Total cost = {item_cost} × {quantity} = {total_cost} {currency_plural}"
            ]
            
            return Problem(
                statement=statement,
                answer=total_cost,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type='money_basic_total_cost'
            )
            
        elif problem_type == 'change':
            # Problem type: You have X money and buy something that costs Y, how much change?
            item = random.choice(self.items['food'])
            item_cost = random.randint(5, 50)
            money_paid = item_cost + random.randint(5, 20)  # Ensure enough money
            change = money_paid - item_cost
            
            statement = f"If you buy a {item} that costs {item_cost} {currency_plural} and " \
                       f"pay with a {money_paid}-{currency_single} bill, how much change " \
                       f"will you receive?"
            
            solution_steps = [
                f"Amount paid = {money_paid} {currency_plural}",
                f"Cost of {item} = {item_cost} {currency_plural}",
                f"Change = {money_paid} - {item_cost} = {change} {currency_plural}"
            ]
            
            return Problem(
                statement=statement,
                answer=change,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type='money_basic_change'
            )
            
        else:  # multiple_items
            # Problem type: Buying multiple items with different prices
            selected_items = random.sample(self.items['stationery'], 3)
            item_costs = [random.randint(1, 10) for _ in range(3)]
            total_cost = sum(item_costs)
            
            statement = (
                f"If a {selected_items[0]} costs {item_costs[0]} {currency_plural}, "
                f"a {selected_items[1]} costs {item_costs[1]} {currency_plural}, "
                f"and a {selected_items[2]} costs {item_costs[2]} {currency_plural}, "
                f"how much do all three items cost together?"
            )
            
            solution_steps = [
                f"Cost of {selected_items[0]} = {item_costs[0]} {currency_plural}",
                f"Cost of {selected_items[1]} = {item_costs[1]} {currency_plural}",
                f"Cost of {selected_items[2]} = {item_costs[2]} {currency_plural}",
                f"Total cost = {item_costs[0]} + {item_costs[1]} + {item_costs[2]} = {total_cost} {currency_plural}"
            ]
            
            return Problem(
                statement=statement,
                answer=total_cost,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type='money_basic_multiple_items'
            )
    
    def _generate_discount_problem(self) -> Problem:
        """Generate a discount/sales price problem."""
        currency_code = random.choice(list(self.currencies.keys()))
        currency_single, currency_plural = self.currencies[currency_code]
        
        # Choose between different types of discount problems
        problem_type = random.choice(['find_discount', 'find_original', 'find_final'])
        
        if problem_type == 'find_discount':
            # Problem type: Find the final price after discount
            original_price = random.randint(20, 100)
            discount_percent = random.choice([10, 15, 20, 25, 30, 40, 50])
            discount_amount = (original_price * discount_percent) // 100
            final_price = original_price - discount_amount
            
            item = random.choice(self.items['clothing'])
            statement = f"A {item} originally costs {original_price} {currency_plural}. " \
                       f"It's on sale for {discount_percent}% off. What is the sale price of the {item}?"
            
            solution_steps = [
                f"Original price = {original_price} {currency_plural}",
                f"Discount = {discount_percent}% of {original_price}",
                f"Discount amount = ({discount_percent}/100) × {original_price} = {discount_amount} {currency_plural}",
                f"Sale price = {original_price} - {discount_amount} = {final_price} {currency_plural}"
            ]
            
            return Problem(
                statement=statement,
                answer=final_price,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type='money_discount_find_final'
            )
            
        elif problem_type == 'find_original':
            # Problem type: Find the original price before discount
            original_price = random.randint(20, 100)
            discount_percent = random.choice([10, 15, 20, 25, 30, 40, 50])
            discount_amount = (original_price * discount_percent) // 100
            final_price = original_price - discount_amount
            
            item = random.choice(self.items['clothing'])
            statement = f"A {item} is on sale for {final_price} {currency_plural} after a {discount_percent}% discount. " \
                       f"What was the original price of the {item}?"
            
            solution_steps = [
                f"Let the original price be x {currency_plural}.",
                f"Discount amount = {discount_percent}% of x = 0.{discount_percent}x",
                f"Sale price = x - 0.{discount_percent}x = 0.{100-discount_percent}x",
                f"Set up the equation: 0.{100-discount_percent}x = {final_price}",
                f"Solve for x: x = {final_price} / 0.{100-discount_percent} = {original_price} {currency_plural}"
            ]
            
            return Problem(
                statement=statement,
                answer=original_price,
                solution_steps=solution_steps,
                difficulty='hard',
                problem_type='money_discount_find_original'
            )
            
        else:  # find_final
            # Problem type: Multiple discounts in sequence
            original_price = random.randint(50, 200)
            discount1 = random.choice([10, 15, 20])
            discount2 = random.choice([5, 10, 15])
            
            # Calculate final price after both discounts
            price_after_first = original_price * (100 - discount1) / 100
            final_price = round(price_after_first * (100 - discount2) / 100, 2)
            
            item = random.choice(self.items['clothing'])
            statement = f"A {item} costs {original_price} {currency_plural}. It's on sale for {discount1}% off, " \
                       f"and then an additional {discount2}% off the sale price. What is the final price " \
                       f"after both discounts?"
            
            solution_steps = [
                f"First discount: {discount1}% off {original_price} {currency_plural}",
                f"Price after first discount: {original_price} × 0.{100-discount1} = {price_after_first} {currency_plural}",
                f"Second discount: {discount2}% off {price_after_first} {currency_plural}",
                f"Final price: {price_after_first} × 0.{100-discount2} = {final_price} {currency_plural}"
            ]
            
            return Problem(
                statement=statement,
                answer=final_price,
                solution_steps=solution_steps,
                difficulty='hard',
                problem_type='money_discount_multiple'
            )
    
    def _generate_profit_loss_problem(self) -> Problem:
        """Generate a profit/loss percentage problem."""
        # Choose a random currency
        currency_code = random.choice(list(self.currencies.keys()))
        currency_singular, currency_plural = self.currencies[currency_code]
        
        # Choose a random item
        item_category = random.choice(list(self.items.keys()))
        item = random.choice(self.items[item_category])
        
        # Choose problem type: find profit/loss percentage, find CP, or find SP
        problem_type = random.choice(['find_percentage', 'find_cp', 'find_sp'])
        
        if problem_type == 'find_percentage':
            cp = random.randint(50, 200)  # Cost price
            is_profit = random.choice([True, False])  # Whether it's a profit or loss
            
            if is_profit:
                profit_percent = random.randint(5, 50)  # 5% to 50% profit
                sp = cp * (100 + profit_percent) // 100  # Selling price
                
                statement = f"A shopkeeper buys a {item} for {cp} {currency_plural} and sells it for {sp} {currency_plural}. " \
                          f"What is the profit percentage?"
                
                solution_steps = [
                    f"Cost Price (CP) = {cp} {currency_plural}",
                    f"Selling Price (SP) = {sp} {currency_plural}",
                    f"Profit = SP - CP = {sp} - {cp} = {sp - cp} {currency_plural}",
                    f"Profit % = (Profit/CP) × 100 = ({(sp-cp)}/{cp}) × 100 = {profit_percent}%"
                ]
                
                return Problem(
                    statement=statement,
                    answer=profit_percent,
                    solution_steps=solution_steps,
                    difficulty='intermediate',
                    problem_type='money_profit_percent'
                )
            else:
                loss_percent = random.randint(5, 40)  # 5% to 40% loss
                sp = cp * (100 - loss_percent) // 100  # Selling price
                
                statement = f"A trader buys a {item} for {cp} {currency_plural} and sells it for {sp} {currency_plural}. " \
                          f"What is the loss percentage?"
                
                solution_steps = [
                    f"Cost Price (CP) = {cp} {currency_plural}",
                    f"Selling Price (SP) = {sp} {currency_plural}",
                    f"Loss = CP - SP = {cp} - {sp} = {cp - sp} {currency_plural}",
                    f"Loss % = (Loss/CP) × 100 = ({(cp-sp)}/{cp}) × 100 = {loss_percent}%"
                ]
                
                return Problem(
                    statement=statement,
                    answer=loss_percent,
                    solution_steps=solution_steps,
                    difficulty='intermediate',
                    problem_type='money_loss_percent'
                )
                
        elif problem_type == 'find_cp':
            is_profit = random.choice([True, False])
            
            if is_profit:
                profit_percent = random.randint(10, 50)  # 10% to 50% profit
                sp = random.randint(100, 500)  # Selling price
                cp = (sp * 100) // (100 + profit_percent)  # Cost price
                
                statement = f"By selling a {item} for {sp} {currency_plural}, a shopkeeper makes a profit of {profit_percent}%. " \
                          f"Find the cost price of the {item}."
                
                solution_steps = [
                    f"Let the Cost Price (CP) be x {currency_plural}",
                    f"Profit = {profit_percent}% of CP = {profit_percent/100}x",
                    f"Selling Price (SP) = CP + Profit = x + {profit_percent/100:.2f}x = {1 + profit_percent/100:.2f}x",
                    f"Given SP = {sp} {currency_plural}",
                    f"{1 + profit_percent/100:.2f}x = {sp}",
                    f"x = {sp} / {1 + profit_percent/100:.2f} = {cp} {currency_plural}"
                ]
                
                return Problem(
                    statement=statement,
                    answer=cp,
                    solution_steps=solution_steps,
                    difficulty='hard',
                    problem_type='money_find_cp_profit'
                )
            else:
                loss_percent = random.randint(5, 40)  # 5% to 40% loss
                sp = random.randint(50, 400)  # Selling price
                cp = (sp * 100) // (100 - loss_percent)  # Cost price
                
                statement = f"By selling a {item} for {sp} {currency_plural}, a shopkeeper incurs a loss of {loss_percent}%. " \
                          f"Find the cost price of the {item}."
                
                solution_steps = [
                    f"Let the Cost Price (CP) be x {currency_plural}",
                    f"Loss = {loss_percent}% of CP = {loss_percent/100}x",
                    f"Selling Price (SP) = CP - Loss = x - {loss_percent/100:.2f}x = {1 - loss_percent/100:.2f}x",
                    f"Given SP = {sp} {currency_plural}",
                    f"{1 - loss_percent/100:.2f}x = {sp}",
                    f"x = {sp} / {1 - loss_percent/100:.2f} = {cp} {currency_plural}"
                ]
                
                return Problem(
                    statement=statement,
                    answer=cp,
                    solution_steps=solution_steps,
                    difficulty='hard',
                    problem_type='money_find_cp_loss'
                )
                
        else:  # find_sp
            cp = random.randint(100, 500)  # Cost price
            is_profit = random.choice([True, False])
            
            if is_profit:
                profit_percent = random.randint(10, 50)  # 10% to 50% profit
                sp = cp * (100 + profit_percent) // 100  # Selling price
                
                statement = f"A shopkeeper buys a {item} for {cp} {currency_plural} and wants to make a profit of {profit_percent}%. " \
                          f"What should be the selling price?"
                
                solution_steps = [
                    f"Cost Price (CP) = {cp} {currency_plural}",
                    f"Profit = {profit_percent}% of CP = {profit_percent/100} × {cp} = {profit_percent*cp//100} {currency_plural}",
                    f"Selling Price (SP) = CP + Profit = {cp} + {profit_percent*cp//100} = {sp} {currency_plural}",
                    f"Alternatively, SP = CP × (100 + Profit%)/100 = {cp} × {100 + profit_percent}/100 = {sp} {currency_plural}"
                ]
                
                return Problem(
                    statement=statement,
                    answer=sp,
                    solution_steps=solution_steps,
                    difficulty='intermediate',
                    problem_type='money_find_sp_profit'
                )
            else:
                loss_percent = random.randint(5, 40)  # 5% to 40% loss
                sp = cp * (100 - loss_percent) // 100  # Selling price
                
                statement = f"A shopkeeper buys a {item} for {cp} {currency_plural} and has to sell it at a loss of {loss_percent}%. " \
                          f"What should be the selling price?"
                
                solution_steps = [
                    f"Cost Price (CP) = {cp} {currency_plural}",
                    f"Loss = {loss_percent}% of CP = {loss_percent/100} × {cp} = {loss_percent*cp//100} {currency_plural}",
                    f"Selling Price (SP) = CP - Loss = {cp} - {loss_percent*cp//100} = {sp} {currency_plural}",
                    f"Alternatively, SP = CP × (100 - Loss%)/100 = {cp} × {100 - loss_percent}/100 = {sp} {currency_plural}"
                ]
                
                return Problem(
                    statement=statement,
                    answer=sp,
                    solution_steps=solution_steps,
                    difficulty='intermediate',
                    problem_type='money_find_sp_loss'
                )

    def _generate_geometry_problem(self) -> Problem:
        """Generate a geometry problem (perimeter, area, or angles)."""
        # Choose a random geometry problem type
        problem_type = random.choice([
            'rectangle_perimeter',
            'rectangle_area',
            'square_perimeter',
            'square_area',
            'triangle_perimeter',
            'triangle_area',
            'circle_circumference',
            'circle_area'
        ])
        
        if problem_type == 'rectangle_perimeter':
            return self._generate_rectangle_perimeter_problem()
        elif problem_type == 'rectangle_area':
            return self._generate_rectangle_area_problem()
        elif problem_type == 'square_perimeter':
            return self._generate_square_perimeter_problem()
        elif problem_type == 'square_area':
            return self._generate_square_area_problem()
        elif problem_type == 'triangle_perimeter':
            return self._generate_triangle_perimeter_problem()
        elif problem_type == 'triangle_area':
            return self._generate_triangle_area_problem()
        elif problem_type == 'circle_circumference':
            return self._generate_circle_circumference_problem()
        elif problem_type == 'circle_area':
            return self._generate_circle_area_problem()
    
    def _generate_rectangle_perimeter_problem(self) -> Problem:
        """Generate a rectangle perimeter problem."""
        length = random.randint(5, 20)
        width = random.randint(2, 15)
        perimeter = 2 * (length + width)
        
        if random.choice([True, False]):
            # Find perimeter given dimensions
            statement = f"A rectangle has a length of {length} units and a width of {width} units. What is its perimeter?"
            solution_steps = [
                f"Perimeter of a rectangle = 2 × (length + width)",
                f"= 2 × ({length} + {width})",
                f"= 2 × {length + width}",
                f"= {perimeter} units"
            ]
            return Problem(
                statement=statement,
                answer=perimeter,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type='geometry_rectangle_perimeter_find'
            )
        else:
            # Find missing dimension given perimeter and one dimension
            if random.choice([True, False]):
                # Find width given length and perimeter
                statement = f"A rectangle has a length of {length} units and a perimeter of {perimeter} units. What is its width?"
                solution_steps = [
                    f"Let the width be w.",
                    f"Perimeter = 2 × (length + width)",
                    f"{perimeter} = 2 × ({length} + w)",
                    f"{perimeter} = {2 * length} + 2w",
                    f"2w = {perimeter - 2 * length}",
                    f"w = {width} units"
                ]
                return Problem(
                    statement=statement,
                    answer=width,
                    solution_steps=solution_steps,
                    difficulty='hard',
                    problem_type='geometry_rectangle_perimeter_find_width'
                )
            else:
                # Find length given width and perimeter
                statement = f"A rectangle has a width of {width} units and a perimeter of {perimeter} units. What is its length?"
                solution_steps = [
                    f"Let the length be l.",
                    f"Perimeter = 2 × (length + width)",
                    f"{perimeter} = 2 × (l + {width})",
                    f"{perimeter} = 2l + {2 * width}",
                    f"2l = {perimeter - 2 * width}",
                    f"l = {length} units"
                ]
                return Problem(
                    statement=statement,
                    answer=length,
                    solution_steps=solution_steps,
                    difficulty='hard',
                    problem_type='geometry_rectangle_perimeter_find_length'
                )
    
    def _generate_rectangle_area_problem(self) -> Problem:
        """Generate a rectangle area problem."""
        length = random.randint(3, 15)
        width = random.randint(2, 12)
        area = length * width
        
        if random.choice([True, False]):
            # Find area given dimensions
            statement = f"A rectangle has a length of {length} units and a width of {width} units. What is its area?"
            solution_steps = [
                f"Area of a rectangle = length × width",
                f"= {length} × {width}",
                f"= {area} square units"
            ]
            return Problem(
                statement=statement,
                answer=area,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type='geometry_rectangle_area_find'
            )
        else:
            # Find missing dimension given area and one dimension
            if random.choice([True, False]):
                # Find width given length and area
                statement = f"A rectangle has a length of {length} units and an area of {area} square units. What is its width?"
                solution_steps = [
                    f"Let the width be w.",
                    f"Area = length × width",
                    f"{area} = {length} × w",
                    f"w = {area} ÷ {length}",
                    f"w = {width} units"
                ]
                return Problem(
                    statement=statement,
                    answer=width,
                    solution_steps=solution_steps,
                    difficulty='hard',
                    problem_type='geometry_rectangle_area_find_width'
                )
            else:
                # Find length given width and area
                statement = f"A rectangle has a width of {width} units and an area of {area} square units. What is its length?"
                solution_steps = [
                    f"Let the length be l.",
                    f"Area = length × width",
                    f"{area} = l × {width}",
                    f"l = {area} ÷ {width}",
                    f"l = {length} units"
                ]
                return Problem(
                    statement=statement,
                    answer=length,
                    solution_steps=solution_steps,
                    difficulty='hard',
                    problem_type='geometry_rectangle_area_find_length'
                )
    
    def _generate_square_perimeter_problem(self) -> Problem:
        """Generate a square perimeter problem."""
        side = random.randint(3, 20)
        perimeter = 4 * side
        
        if random.choice([True, False]):
            # Find perimeter given side
            statement = f"A square has a side length of {side} units. What is its perimeter?"
            solution_steps = [
                f"Perimeter of a square = 4 × side",
                f"= 4 × {side}",
                f"= {perimeter} units"
            ]
            return Problem(
                statement=statement,
                answer=perimeter,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type='geometry_square_perimeter_find'
            )
        else:
            # Find side given perimeter
            statement = f"A square has a perimeter of {perimeter} units. What is the length of each side?"
            solution_steps = [
                f"Let the side length be s.",
                f"Perimeter = 4 × side",
                f"{perimeter} = 4 × s",
                f"s = {perimeter} ÷ 4",
                f"s = {side} units"
            ]
            return Problem(
                statement=statement,
                answer=side,
                solution_steps=solution_steps,
                difficulty='hard',
                problem_type='geometry_square_perimeter_find_side'
            )
    
    def _generate_square_area_problem(self) -> Problem:
        """Generate a square area problem."""
        side = random.randint(3, 15)
        area = side ** 2
        
        if random.choice([True, False]):
            # Find area given side
            statement = f"A square has a side length of {side} units. What is its area?"
            solution_steps = [
                f"Area of a square = side × side",
                f"= {side} × {side}",
                f"= {area} square units"
            ]
            return Problem(
                statement=statement,
                answer=area,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type='geometry_square_area_find'
            )
        else:
            # Find side given area
            statement = f"A square has an area of {area} square units. What is the length of each side?"
            solution_steps = [
                f"Let the side length be s.",
                f"Area = s × s = s²",
                f"s² = {area}",
                f"s = √{area}",
                f"s = {side} units"
            ]
            return Problem(
                statement=statement,
                answer=side,
                solution_steps=solution_steps,
                difficulty='hard',
                problem_type='geometry_square_area_find_side'
            )
    
    def _generate_triangle_perimeter_problem(self) -> Problem:
        """Generate a triangle perimeter problem."""
        a = random.randint(5, 15)
        b = random.randint(5, 15)
        c = a + b - random.randint(1, 3)  # Ensure triangle inequality
        perimeter = a + b + c
        
        if random.choice([True, False]):
            # Find perimeter given sides
            statement = f"A triangle has sides of {a} units, {b} units, and {c} units. What is its perimeter?"
            solution_steps = [
                f"Perimeter of a triangle = sum of all sides",
                f"= {a} + {b} + {c}",
                f"= {perimeter} units"
            ]
            return Problem(
                statement=statement,
                answer=perimeter,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type='geometry_triangle_perimeter_find'
            )
        else:
            # Find missing side given perimeter and other two sides
            sides = [a, b, c]
            random.shuffle(sides)
            given_sides = sides[:2]
            missing_side = sides[2]
            
            statement = f"A triangle has a perimeter of {perimeter} units and two sides measuring {given_sides[0]} units and {given_sides[1]} units. What is the length of the third side?"
            solution_steps = [
                f"Let the third side be x.",
                f"Perimeter = sum of all sides",
                f"{perimeter} = {given_sides[0]} + {given_sides[1]} + x",
                f"{perimeter} = {sum(given_sides)} + x",
                f"x = {perimeter} - {sum(given_sides)}",
                f"x = {missing_side} units"
            ]
            return Problem(
                statement=statement,
                answer=missing_side,
                solution_steps=solution_steps,
                difficulty='hard',
                problem_type='geometry_triangle_perimeter_find_side'
            )
    
    def _generate_triangle_area_problem(self) -> Problem:
        """Generate a triangle area problem."""
        base = random.randint(5, 20)
        height = random.randint(4, 15)
        area = 0.5 * base * height
        
        if random.choice([True, False]):
            # Find area given base and height
            statement = f"A triangle has a base of {base} units and a height of {height} units. What is its area?"
            solution_steps = [
                f"Area of a triangle = ½ × base × height",
                f"= ½ × {base} × {height}",
                f"= {area} square units"
            ]
            return Problem(
                statement=statement,
                answer=area,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type='geometry_triangle_area_find'
            )
        else:
            # Find missing dimension given area and one dimension
            if random.choice([True, False]):
                # Find height given base and area
                statement = f"A triangle has a base of {base} units and an area of {area} square units. What is its height?"
                solution_steps = [
                    f"Let the height be h.",
                    f"Area = ½ × base × height",
                    f"{area} = ½ × {base} × h",
                    f"{area} = {0.5 * base} × h",
                    f"h = {area} ÷ {0.5 * base}",
                    f"h = {height} units"
                ]
                return Problem(
                    statement=statement,
                    answer=height,
                    solution_steps=solution_steps,
                    difficulty='hard',
                    problem_type='geometry_triangle_area_find_height'
                )
            else:
                # Find base given height and area
                statement = f"A triangle has a height of {height} units and an area of {area} square units. What is the length of its base?"
                solution_steps = [
                    f"Let the base be b.",
                    f"Area = ½ × base × height",
                    f"{area} = ½ × b × {height}",
                    f"{area} = {0.5 * height} × b",
                    f"b = {area} ÷ {0.5 * height}",
                    f"b = {base} units"
                ]
                return Problem(
                    statement=statement,
                    answer=base,
                    solution_steps=solution_steps,
                    difficulty='hard',
                    problem_type='geometry_triangle_area_find_base'
                )
    
    def _generate_circle_circumference_problem(self) -> Problem:
        """Generate a circle circumference problem."""
        radius = random.randint(2, 15)
        diameter = 2 * radius
        circumference = round(2 * 3.14 * radius, 2)
        
        if random.choice([True, False]):
            # Find circumference given radius
            statement = f"A circle has a radius of {radius} units. What is its circumference? (Use π = 3.14)"
            solution_steps = [
                f"Circumference = 2 × π × radius",
                f"= 2 × 3.14 × {radius}",
                f"= {circumference} units"
            ]
            return Problem(
                statement=statement,
                answer=circumference,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type='geometry_circle_circumference_find_radius'
            )
        else:
            # Find radius given circumference
            statement = f"A circle has a circumference of {circumference} units. What is its radius? (Use π = 3.14)"
            solution_steps = [
                f"Let the radius be r.",
                f"Circumference = 2 × π × radius",
                f"{circumference} = 2 × 3.14 × r",
                f"{circumference} = 6.28 × r",
                f"r = {circumference} ÷ 6.28",
                f"r = {radius} units"
            ]
            return Problem(
                statement=statement,
                answer=radius,
                solution_steps=solution_steps,
                difficulty='hard',
                problem_type='geometry_circle_circumference_find_radius'
            )
    
    def _generate_circle_area_problem(self) -> Problem:
        """Generate a circle area problem."""
        radius = random.randint(2, 12)
        area = round(3.14 * (radius ** 2), 2)
        
        if random.choice([True, False]):
            # Find area given radius
            statement = f"A circle has a radius of {radius} units. What is its area? (Use π = 3.14)"
            solution_steps = [
                f"Area = π × radius²",
                f"= 3.14 × {radius}²",
                f"= 3.14 × {radius ** 2}",
                f"= {area} square units"
            ]
            return Problem(
                statement=statement,
                answer=area,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type='geometry_circle_area_find_radius'
            )
        else:
            # Find radius given area
            statement = f"A circle has an area of {area} square units. What is its radius? (Use π = 3.14)"
            solution_steps = [
                f"Let the radius be r.",
                f"Area = π × r²",
                f"{area} = 3.14 × r²",
                f"r² = {area} ÷ 3.14",
                f"r² = {area / 3.14:.2f}",
                f"r = √{area / 3.14:.2f}",
                f"r = {radius} units"
            ]
            return Problem(
                statement=statement,
                answer=radius,
                solution_steps=solution_steps,
                difficulty='hard',
                problem_type='geometry_circle_area_find_radius'
            )      
        return random.choice(variations)()
    
    # Intermediate difficulty problems
    def _generate_age_sum_problem(self) -> Problem:
        """Generate a problem about the sum of ages changing over time."""
        age1 = random.randint(15, 30)  # Alex's age
        age_diff = random.randint(2, 10)  # Age difference between Alex and Taylor
        years = random.randint(1, 5)  # Years in the future
        total_in_future = age1 + (age1 - age_diff) + 2 * years  # Total ages in the future
        
        return Problem(
            statement=f"Alex is {age_diff} years older than Taylor. In {years} years, the sum of their ages will be {total_in_future}. How old is Alex now?",
            answer=age1,
            solution_steps=[
                f"Let Alex's current age be x.",
                f"Then Taylor's current age is x - {age_diff}.",
                f"In {years} years, Alex will be x + {years} and Taylor will be (x - {age_diff}) + {years} = x - {age_diff - years}.",
                f"The sum of their ages in {years} years: (x + {years}) + (x - {age_diff - years}) = 2x + {2*years - age_diff}",
                f"Set up the equation: 2x + {2*years - age_diff} = {total_in_future}",
                f"Solve for x: 2x = {total_in_future - (2*years - age_diff)} → x = {age1}"
            ],
            difficulty='intermediate',
            problem_type='age_related_sum'
        )
    
    def _generate_age_difference_problem(self) -> Problem:
        """Generate problem about age difference remaining constant."""
        age1 = random.randint(15, 25)
        age2 = random.randint(5, 14)
        years_ago = random.randint(1, 5)
        
        return Problem(
            statement=f"A mother is {age1 - age2} years older than her daughter. {years_ago} years ago, the mother was {age1 - years_ago} years old. How old is the daughter now?",
            answer=age2,
            solution_steps=[
                f"Let the daughter's current age be x.",
                f"Then the mother's current age is x + {age1 - age2}.",
                f"{years_ago} years ago, the mother was (x + {age1 - age2}) - {years_ago} = x + {age1 - age2 - years_ago} years old.",
                f"Set up the equation: x + {age1 - age2 - years_ago} = {age1 - years_ago}",
                f"Solve for x: x = {age1 - years_ago} - {age1 - age2 - years_ago} = {age2}"
            ],
            difficulty='intermediate',
            problem_type='age_related_difference'
        )
    
    def _generate_age_ratio_problem(self) -> Problem:
        """Generate problem about ratio of ages."""
        age1 = random.randint(6, 12) * 2  # Ensures even number
        ratio = random.choice([2, 3, 4])
        age2 = age1 // ratio
        
        return Problem(
            statement=f"The ratio of Sarah's age to her younger brother's age is {ratio}:1. If Sarah is {age1} years old, how old is her brother?",
            answer=age2,
            solution_steps=[
                f"Let the brother's age be x.",
                f"The ratio of Sarah's age to her brother's age is {ratio}:1.",
                f"Set up the proportion: {age1}/x = {ratio}/1",
                f"Cross-multiply: {age1} = {ratio}x",
                f"Solve for x: x = {age1}/{ratio} = {age2}"
            ],
            difficulty='intermediate',
            problem_type='age_related_ratio'
        )
    
    # Hard difficulty problems
    def _generate_age_ratio_change_problem(self, difficulty: str = 'hard') -> Problem:
        """Generate a problem where the ratio of ages changes over time.
        
        Args:
            difficulty: The difficulty level ('intermediate' or 'hard').
                       This parameter is included for API consistency but not used.
        """
        son_age = random.randint(5, 15)
        father_age = random.randint(30, 50)
        years_ago = random.randint(1, 10)
        old_ratio = random.choice([3, 4, 5])
        
        # Adjust son's age to make the ratio work
        son_age = (father_age - years_ago) // old_ratio + years_ago
        
        return Problem(
            statement=f"A father is {father_age} years old and his son is {son_age} years old. How many years ago was the father {old_ratio} times as old as his son?",
            answer=years_ago,
            solution_steps=[
                f"Let x be the number of years ago when the father was {old_ratio} times as old as his son.",
                f"x years ago, father's age was {father_age} - x and son's age was {son_age} - x.",
                f"Set up the equation: {father_age} - x = {old_ratio}({son_age} - x)",
                f"Solve for x: {father_age} - x = {old_ratio*son_age} - {old_ratio}x",
                f"{old_ratio}x - x = {old_ratio*son_age} - {father_age}",
                f"{old_ratio-1}x = {old_ratio*son_age - father_age}",
                f"x = {years_ago}"
            ],
            difficulty='hard',
            problem_type='age_related_ratio_change'
        )
    
    def _generate_age_three_people_problem(self, difficulty: str = 'hard') -> Problem:
        """Generate problem involving ages of three people.
        
        Args:
            difficulty: The difficulty level ('intermediate' or 'hard').
                       This parameter is included for API consistency but not used.
        """
        a = random.randint(10, 20)
        b = a + random.randint(2, 5)
        c = b + random.randint(2, 5)
        total = a + b + c
        
        return Problem(
            statement=f"The sum of the ages of three siblings is {total}. The oldest is {c-a} years older than the youngest, and the middle child is {b-a} years older than the youngest. How old is each sibling?",
            answer={'youngest': a, 'middle': b, 'oldest': c},
            solution_steps=[
                "Let the youngest sibling's age be x.",
                f"Then the middle sibling's age is x + {b-a}.",
                f"And the oldest sibling's age is x + {c-a}.",
                f"The sum of their ages: x + (x + {b-a}) + (x + {c-a}) = 3x + {b+c-2*a}",
                f"Set up the equation: 3x + {b+c-2*a} = {total}",
                f"Solve for x: 3x = {total - (b+c-2*a)} → x = {a}",
                f"Therefore, the siblings are {a}, {b}, and {c} years old."
            ],
            difficulty='hard',
            problem_type='age_related_three_people'
        )
    
    def _generate_age_combined_conditions_problem(self, difficulty: str = 'hard') -> Problem:
        """Generate problem with multiple conditions on ages.
        
        Args:
            difficulty: The difficulty level ('intermediate' or 'hard').
                       This parameter is included for API consistency but not used.
        """
        son_age = random.randint(10, 15)
        father_age = son_age * 3 + random.randint(1, 5)
        years = random.randint(5, 10)
        
        return Problem(
            statement=f"A father is three times as old as his son. In {years} years, he will be twice as old as his son will be then. How old are they now?",
            answer={'father': father_age, 'son': son_age},
            solution_steps=[
                "Let son's current age be x.",
                f"Then father's current age is 3x + {father_age - 3*son_age}.",
                f"In {years} years, son will be x + {years} and father will be 3x + {father_age - 3*son_age + years}.",
                f"Set up the equation: 3x + {father_age - 3*son_age + years} = 2(x + {years})",
                f"Solve for x: 3x + {father_age - 3*son_age + years} = 2x + {2*years}",
                f"3x - 2x = {2*years - (father_age - 3*son_age + years)}",
                f"x = {son_age}",
                f"Therefore, son is {son_age} years old and father is {father_age} years old."
            ],
            difficulty='hard',
            problem_type='age_combined_conditions'
        )

    def _generate_time_scheduling_problem(self) -> Problem:
        """
        Generate a time and scheduling problem.
        
        Problem types:
        1. Calculating duration between two times
        2. Determining end time of an event
        3. Scheduling multiple activities within a time frame
        """
        problem_type = random.choice([
            'time_duration',
            'end_time',
            'schedule_activities'
        ])
        
        # Common activities for scheduling problems
        activities = {
            'morning': ['breakfast', 'exercise', 'reading', 'shower', 'getting ready'],
            'school': ['math class', 'science class', 'lunch', 'recess', 'art class', 'music class'],
            'after_school': ['homework', 'sports practice', 'music lessons', 'chores'],
            'evening': ['dinner', 'family time', 'homework', 'preparing for bed']
        }
        
        if problem_type == 'time_duration':
            # Generate random start and end times
            start_hour = random.randint(1, 11)
            start_minute = random.choice([0, 15, 30, 45])
            start_am_pm = random.choice(['AM', 'PM'])
            
            # Ensure duration is reasonable (15 minutes to 6 hours)
            duration_hours = random.randint(0, 5)
            duration_minutes = random.choice([0, 15, 30, 45])
            
            # Calculate end time
            end_hour = start_hour + duration_hours
            end_minute = start_minute + duration_minutes
            
            if end_minute >= 60:
                end_hour += 1
                end_minute -= 60
                
            # Handle AM/PM changes
            end_am_pm = start_am_pm
            if end_hour >= 12:
                if start_am_pm == 'AM' and end_hour > 12:
                    end_am_pm = 'PM'
                elif start_am_pm == 'PM' and end_hour > 12:
                    end_am_pm = 'AM'  # Next day
                if end_hour > 12:
                    end_hour -= 12
            
            start_time = f"{start_hour}:{start_minute:02d} {start_am_pm}"
            end_time = f"{end_hour}:{end_minute:02d} {end_am_pm}"
            
            # Calculate total minutes for the answer
            total_minutes = duration_hours * 60 + duration_minutes
            
            statement = (
                f"If you start an activity at {start_time} and finish at {end_time}, "
                f"how many minutes does the activity last?"
            )
            
            solution_steps = [
                f"1. Start time: {start_time}",
                f"2. End time: {end_time}",
                f"3. Calculate hours: {duration_hours} hours × 60 minutes = {duration_hours * 60} minutes",
                f"4. Add minutes: {duration_hours * 60} + {duration_minutes} = {total_minutes} minutes",
                f"5. The activity lasts for {total_minutes} minutes."
            ]
            
            return Problem(
                statement=statement,
                answer=total_minutes,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type=problem_type
            )
            
        elif problem_type == 'end_time':
            # Generate random start time and duration
            start_hour = random.randint(1, 12)
            start_minute = random.choice([0, 15, 30, 45])
            start_am_pm = random.choice(['AM', 'PM'])
            
            duration_hours = random.randint(1, 3)
            duration_minutes = random.choice([0, 15, 30, 45])
            
            # Calculate end time
            end_hour = start_hour + duration_hours
            end_minute = start_minute + duration_minutes
            
            if end_minute >= 60:
                end_hour += 1
                end_minute -= 60
                
            # Handle AM/PM changes
            end_am_pm = start_am_pm
            if end_hour >= 12:
                if start_am_pm == 'AM' and end_hour > 12:
                    end_am_pm = 'PM'
                elif start_am_pm == 'PM' and end_hour > 12:
                    end_am_pm = 'AM'  # Next day
                if end_hour > 12:
                    end_hour -= 12
            
            start_time = f"{start_hour}:{start_minute:02d} {start_am_pm}"
            end_time = f"{end_hour}:{end_minute:02d} {end_am_pm}"
            
            # Format duration for the problem statement
            duration_str = ""
            if duration_hours > 0:
                duration_str += f"{duration_hours} hour"
                if duration_hours > 1:
                    duration_str += "s"
            if duration_minutes > 0:
                if duration_str:
                    duration_str += " and "
                duration_str += f"{duration_minutes} minute"
                if duration_minutes > 1:
                    duration_str += "s"
            
            statement = (
                f"If you start an activity at {start_time} and it lasts for {duration_str}, "
                f"what time will you finish?"
            )
            
            solution_steps = [
                f"1. Start time: {start_time}",
                f"2. Add {duration_hours} hours: {start_hour} {start_am_pm} + {duration_hours} hours = {end_hour} {end_am_pm}",
                f"3. Add {duration_minutes} minutes: {end_minute} minutes past the hour",
                f"4. The activity will end at {end_time}."
            ]
            
            return Problem(
                statement=statement,
                answer=end_time,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type=problem_type
            )
            
        else:  # schedule_activities
            # Generate a schedule with multiple activities
            time_available = random.randint(120, 300)  # 2 to 5 hours in minutes
            num_activities = random.randint(3, 5)
            
            # Generate random activities with durations
            activity_list = []
            total_duration = 0
            
            for _ in range(num_activities - 1):
                # Ensure we leave enough time for the last activity
                max_duration = min(60, time_available - total_duration - (num_activities - len(activity_list) - 1) * 15)
                if max_duration < 15:  # Ensure minimum 15 minutes per activity
                    break
                duration = random.randint(1, max_duration // 15) * 15  # Rounded to nearest 15 minutes
                activity = random.choice(activities[random.choice(list(activities.keys()))])
                activity_list.append((activity, duration))
                total_duration += duration
            
            # Add the last activity to fill remaining time
            last_duration = time_available - total_duration
            if last_duration >= 15:  # Only add if there's at least 15 minutes left
                activity = random.choice(activities[random.choice(list(activities.keys()))])
                activity_list.append((activity, last_duration))
                total_duration += last_duration
            
            # Generate the problem statement
            statement = "You have the following activities to complete in your day. "
            statement += f"You have {time_available//60} hours and {time_available%60} minutes available. "
            statement += "Can you fit all these activities into your schedule? If yes, how much free time will you have left?\n\n"
            
            for i, (activity, duration) in enumerate(activity_list, 1):
                hours = duration // 60
                minutes = duration % 60
                time_str = f"{hours} hour" if hours == 1 else f"{hours} hours"
                if minutes > 0:
                    time_str += f" and {minutes} minute"
                    if minutes > 1:
                        time_str += "s"
                statement += f"{i}. {activity.capitalize()} ({time_str})\n"
            
            # Calculate free time
            free_time = time_available - total_duration
            
            solution_steps = [
                "1. Calculate total time needed for all activities:"
            ]
            
            total_time = 0
            for i, (activity, duration) in enumerate(activity_list, 1):
                total_time += duration
                solution_steps.append(f"   - {activity.capitalize()}: {duration} minutes")
            
            solution_steps.append(f"2. Total time needed: {total_time} minutes")
            solution_steps.append(f"3. Time available: {time_available} minutes")
            
            if free_time >= 0:
                solution_steps.append(f"4. Free time left: {free_time} minutes")
                solution = f"Yes, you can fit all activities with {free_time} minutes of free time."
            else:
                solution_steps.append(f"4. You need {-free_time} more minutes to complete all activities.")
                solution = f"No, you need {-free_time} more minutes to complete all activities."
            
            return Problem(
                statement=statement,
                answer=solution,
                solution_steps=solution_steps,
                difficulty='hard',
                problem_type=problem_type
            )
    
    def _generate_mixture_problem(self, problem_type: str = None, difficulty: str = None) -> Problem:
        """
        Generate a mixture problem involving combining substances with different properties.
        
        Args:
            problem_type: Specific type of mixture problem to generate. If None, a random type is selected.
                         Options: 'mixture_solution', 'mixture_alloy', 'mixture_ingredients'
            difficulty: 'intermediate' or 'hard'. If None, a random level is selected.
            
        Returns:
            Problem object containing the problem statement, answer, solution steps,
            difficulty level, and problem type.
        """
        if problem_type is None:
            problem_type = random.choice(['mixture_solution', 'mixture_alloy', 'mixture_ingredients'])
            
        if problem_type == 'mixture_solution':
            return self._generate_solution_mixture_problem(difficulty)
        elif problem_type == 'mixture_alloy':
            return self._generate_alloy_mixture_problem(difficulty)
        elif problem_type == 'mixture_ingredients':
            return self._generate_ingredients_mixture_problem(difficulty)
        else:
            raise ValueError(f"Unknown mixture problem type: {problem_type}")
            
    def _generate_solution_mixture_problem(self, difficulty: str = None) -> Problem:
        """Generate a problem about mixing two solutions with different concentrations."""
        if difficulty is None:
            difficulty = random.choice(self.difficulty_levels)
            
        # Choose random concentrations and volumes
        c1 = random.randint(5, 20)  # Concentration 1 (5% to 20%)
        c2 = random.randint(25, 50)  # Concentration 2 (25% to 50%)
        v1 = random.randint(100, 500)  # Volume 1 in mL
        
        # For intermediate difficulty, ask for the final concentration
        if difficulty == 'intermediate':
            v2 = random.randint(100, 500)  # Volume 2 in mL
            
            # Calculate final concentration
            final_conc = (c1 * v1 + c2 * v2) / (v1 + v2)
            
            # Ensure we use 'mix', 'combine', or 'blend' in the problem statement
            mix_verb = random.choice(['mix', 'combine', 'blend'])
            problem = f"You {mix_verb} {v1} mL of a {c1}% solution with {v2} mL of a {c2}% solution. " \
                     f"What is the concentration of the resulting mixture?"
            
            solution = [
                f"1. Calculate the amount of solute in the first solution: {c1}% of {v1} mL = 0.{c1} × {v1} = {c1 * v1 / 100} mL",
                f"2. Calculate the amount of solute in the second solution: {c2}% of {v2} mL = 0.{c2} × {v2} = {c2 * v2 / 100} mL",
                f"3. Total solute = {c1 * v1 / 100} + {c2 * v2 / 100} = {c1 * v1 / 100 + c2 * v2 / 100} mL",
                f"4. Total volume = {v1} + {v2} = {v1 + v2} mL",
                f"5. Final concentration = (Total solute / Total volume) × 100 = "
                f"({c1 * v1 / 100 + c2 * v2 / 100} / {v1 + v2}) × 100 = {final_conc:.1f}%"
            ]
            
            return Problem(
                statement=problem,
                answer=round(final_conc, 1),
                solution_steps=solution,
                difficulty=difficulty,
                problem_type='mixture_solution_conc'
            )
            
        # For hard difficulty, ask for the volume needed to achieve a specific concentration
        else:
            target_conc = random.randint(c1 + 5, c2 - 5)  # Target concentration between c1 and c2
            
            # Calculate required volume v2 to achieve target_conc
            # target_conc = (c1*v1 + c2*v2) / (v1 + v2)
            # Solving for v2:
            v2 = (v1 * (target_conc - c1)) / (c2 - target_conc)
            v2 = round(v2)  # Round to nearest whole number
            
            # Ensure we use 'mix', 'combine', or 'blend' in the problem statement
            mix_verb = random.choice(['mix', 'combine', 'blend'])
            problem = f"You have {v1} mL of a {c1}% solution. How many mL of a {c2}% solution should you {mix_verb} with it " \
                     f"to make a {target_conc}% solution?"
            
            solution = [
                f"1. Let x be the mL of {c2}% solution to add.",
                f"2. Amount of solute from first solution: {c1}% of {v1} mL = 0.{c1} × {v1} = {c1 * v1 / 100} mL",
                f"3. Amount of solute from second solution: {c2}% of x mL = 0.{c2}x mL",
                f"4. Total solute = {c1 * v1 / 100} + 0.{c2}x",
                f"5. Total volume = {v1} + x",
                f"6. Set up the equation: ({c1 * v1 / 100} + 0.{c2}x) / ({v1} + x) = {target_conc/100}",
                f"7. Solve for x: {c1 * v1 / 100} + 0.{c2}x = {target_conc/100}({v1} + x)",
                f"8. {c1 * v1 / 100} + 0.{c2}x = {target_conc * v1 / 100} + {target_conc/100}x",
                f"9. 0.{c2}x - {target_conc/100}x = {target_conc * v1 / 100} - {c1 * v1 / 100}",
                f"10. x = {v2} mL"
            ]
            
            return Problem(
                statement=problem,
                answer=v2,
                solution_steps=solution,
                difficulty=difficulty,
                problem_type='mixture_solution_volume'
            )
    
    def _generate_alloy_mixture_problem(self, difficulty: str = None) -> Problem:
        """Generate a problem about mixing metals to create an alloy."""
        if difficulty is None:
            difficulty = random.choice(self.difficulty_levels)
            
        # Choose random metals and percentages
        metal1, metal2 = random.sample(['gold', 'silver', 'copper', 'nickel', 'zinc'], 2)
        p1 = random.randint(20, 40)  # Percentage of metal1 in alloy1 (20% to 40%)
        p2 = random.randint(60, 80)  # Percentage of metal1 in alloy2 (60% to 80%)
        w1 = random.randint(100, 300)  # Weight of alloy1 in grams
        
        if difficulty == 'intermediate':
            w2 = random.randint(100, 300)  # Weight of alloy2 in grams
            
            # Calculate final percentage of metal1 in the mixture
            final_percent = (p1 * w1 + p2 * w2) / (w1 + w2)
            
            # Ensure we use 'mix', 'combine', or 'blend' in the problem statement
            mix_verb = random.choice(['mix', 'combine', 'blend'])
            problem = f"You have {w1}g of an alloy that is {p1}% {metal1} and {100-p1}% {metal2}. " \
                     f"You {mix_verb} it with {w2}g of another alloy that is {p2}% {metal1} and {100-p2}% {metal2}. " \
                     f"What percentage of the resulting mixture is {metal1}?"
            
            solution = [
                f"1. Calculate the amount of {metal1} in the first alloy: {p1}% of {w1}g = {p1 * w1 / 100}g",
                f"2. Calculate the amount of {metal1} in the second alloy: {p2}% of {w2}g = {p2 * w2 / 100}g",
                f"3. Total {metal1} = {p1 * w1 / 100} + {p2 * w2 / 100} = {p1 * w1 / 100 + p2 * w2 / 100}g",
                f"4. Total weight of mixture = {w1} + {w2} = {w1 + w2}g",
                f"5. Percentage of {metal1} = (Total {metal1} / Total weight) × 100 = "
                f"({p1 * w1 / 100 + p2 * w2 / 100} / {w1 + w2}) × 100 = {final_percent:.1f}%"
            ]
            
            return Problem(
                statement=problem,
                answer=round(final_percent, 1),
                solution_steps=solution,
                difficulty=difficulty,
                problem_type='mixture_alloy_percent'
            )
            
        else:  # Hard difficulty
            target_percent = random.randint(p1 + 10, p2 - 10)  # Target percentage between p1 and p2
            
            # Calculate required weight w2 to achieve target_percent
            # target_percent = (p1*w1 + p2*w2) / (w1 + w2)
            # Solving for w2:
            w2 = (w1 * (target_percent - p1)) / (p2 - target_percent)
            w2 = round(w2 / 50) * 50  # Round to nearest 50g for realism
            
            problem = f"You have {w1}g of an alloy that is {p1}% {metal1}. " \
                     f"How many grams of a {p2}% {metal1} alloy should you mix with it to create an alloy that is {target_percent}% {metal1}?"
            
            solution = [
                f"1. Let x be the grams of {p2}% {metal1} alloy to add.",
                f"2. Amount of {metal1} in first alloy: {p1}% of {w1}g = {p1 * w1 / 100}g",
                f"3. Amount of {metal1} in second alloy: {p2}% of x g = 0.{p2}x g",
                f"4. Total {metal1} = {p1 * w1 / 100} + 0.{p2}x",
                f"5. Total weight = {w1} + x",
                f"6. Set up the equation: ({p1 * w1 / 100} + 0.{p2}x) / ({w1} + x) = {target_percent/100}",
                f"7. Solve for x: {p1 * w1 / 100} + 0.{p2}x = {target_percent/100}({w1} + x)",
                f"8. {p1 * w1 / 100} + 0.{p2}x = {target_percent * w1 / 100} + {target_percent/100}x",
                f"9. 0.{p2}x - {target_percent/100}x = {target_percent * w1 / 100} - {p1 * w1 / 100}",
                f"10. x = {w2}g"
            ]
            
            return Problem(
                statement=problem,
                answer=w2,
                solution_steps=solution,
                difficulty=difficulty,
                problem_type='mixture_alloy_weight'
            )
    
    def _generate_ingredients_mixture_problem(self, difficulty: str = None) -> Problem:
        """Generate a problem about mixing ingredients with different costs or qualities."""
        if difficulty is None:
            difficulty = random.choice(self.difficulty_levels)
            
        # Choose random ingredients and properties
        ingredient1, ingredient2 = random.sample(['coffee beans', 'tea leaves', 'chocolate', 'nuts', 'dried fruit'], 2)
        price1 = round(random.uniform(2.0, 5.0), 2)  # Price per unit of ingredient1
        price2 = round(random.uniform(5.0, 10.0), 2)  # Price per unit of ingredient2 (higher than price1)
        q1 = random.randint(2, 5)  # Quantity of ingredient1
        
        if difficulty == 'intermediate':
            q2 = random.randint(2, 5)  # Quantity of ingredient2
            
            # Calculate average price per unit
            avg_price = (price1 * q1 + price2 * q2) / (q1 + q2)
            
            # Ensure we use 'mix', 'combine', or 'blend' in the problem statement
            mix_verb = random.choice(['mixes', 'combines', 'blends'])
            problem = f"A store owner {mix_verb} {q1} kg of {ingredient1} that costs ${price1:.2f}/kg with {q2} kg of {ingredient2} that costs ${price2:.2f}/kg. " \
                     f"What should be the price per kg of the mixture to break even?"
            
            solution = [
                f"1. Cost of {ingredient1}: {q1} kg × ${price1:.2f}/kg = ${price1 * q1:.2f}",
                f"2. Cost of {ingredient2}: {q2} kg × ${price2:.2f}/kg = ${price2 * q2:.2f}",
                f"3. Total cost = ${price1 * q1:.2f} + ${price2 * q2:.2f} = ${price1 * q1 + price2 * q2:.2f}",
                f"4. Total weight = {q1} + {q2} = {q1 + q2} kg",
                f"5. Price per kg = Total cost / Total weight = ${price1 * q1 + price2 * q2:.2f} / {q1 + q2} = ${avg_price:.2f}/kg"
            ]
            
            return Problem(
                statement=problem,
                answer=round(avg_price, 2),
                solution_steps=solution,
                difficulty=difficulty,
                problem_type='mixture_ingredients_price'
            )
            
        else:  # Hard difficulty
            target_price = round(random.uniform(price1 + 1, price2 - 1), 2)  # Target price between price1 and price2
            
            # Calculate required quantity q2 to achieve target_price
            # target_price = (price1 * q1 + price2 * q2) / (q1 + q2)
            # Solving for q2:
            q2 = (q1 * (target_price - price1)) / (price2 - target_price)
            q2 = round(q2 * 2) / 2  # Round to nearest 0.5 kg for realism
            
            problem = f"A store owner has {q1} kg of {ingredient1} that costs ${price1:.2f}/kg. " \
                     f"How many kg of {ingredient2} that costs ${price2:.2f}/kg should be mixed with it " \
                     f"to create a mixture that can be sold for ${target_price:.2f}/kg?"
            
            solution = [
                f"1. Let x be the kg of {ingredient2} to add.",
                f"2. Cost of {ingredient1}: {q1} kg × ${price1:.2f}/kg = ${price1 * q1:.2f}",
                f"3. Cost of {ingredient2}: x kg × ${price2:.2f}/kg = ${price2:.2f}x",
                f"4. Total cost = ${price1 * q1:.2f} + ${price2:.2f}x",
                f"5. Total weight = {q1} + x kg",
                f"6. Set up the equation: (${price1 * q1:.2f} + ${price2:.2f}x) / ({q1} + x) = ${target_price:.2f}",
                f"7. Solve for x: {price1 * q1:.2f} + {price2:.2f}x = {target_price:.2f}({q1} + x)",
                f"8. {price1 * q1:.2f} + {price2:.2f}x = {target_price * q1:.2f} + {target_price:.2f}x",
                f"9. {price2:.2f}x - {target_price:.2f}x = {target_price * q1:.2f} - {price1 * q1:.2f}",
                f"10. x = {q2:.1f} kg"
            ]
            
            return Problem(
                statement=problem,
                answer=q2,
                solution_steps=solution,
                difficulty=difficulty,
                problem_type='mixture_ingredients_quantity'
            )

    def _generate_shopping_budget_problem(self, problem_type=None):
        """
        Generate a shopping budget problem.
        
        Args:
            problem_type (str, optional): The type of shopping problem to generate. 
                If None, a random type will be selected.
                
        Returns:
            Problem: A shopping budget problem.
        """
        if problem_type is None:
            problem_type = random.choice(['shopping_max_quantity', 'shopping_remaining_money', 'shopping_max_price'])
        
        # Choose a random item category and item
        category = random.choice(list(self.items.keys()))
        item = random.choice(self.items[category])
        
        price = round(random.uniform(0.5, 10.0), 2)
        quantity = random.randint(2, 10)
        budget = round(price * quantity * random.uniform(1.2, 2.0), 2)  # Budget is 20-100% more than exact cost
        
        if problem_type == 'shopping_max_quantity':
            statement = (
                f"You have ${budget:.2f} to spend on {item}s. "
                f"Each {item} costs ${price:.2f}. "
                f"What is the maximum number of {item}s you can buy without exceeding your budget?"
            )
            max_quantity = int(budget // price)
            solution_steps = [
                f"1. Divide your budget by the price per {item}: ${budget:.2f} ÷ ${price:.2f} = {budget/price:.2f}",
                f"2. Since you can't buy a fraction of an {item}, round down to the nearest whole number: {max_quantity}",
                f"3. Verify: {max_quantity} × ${price:.2f} = ${max_quantity * price:.2f} ≤ ${budget:.2f}",
                f"4. Therefore, you can buy a maximum of {max_quantity} {item}s."
            ]
            return Problem(
                statement=statement,
                answer=max_quantity,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type=problem_type
            )
        
        elif problem_type == 'shopping_remaining_money':
            quantity = random.randint(2, min(10, int(budget/price)))
            total_cost = round(price * quantity, 2)
            remaining = round(budget - total_cost, 2)
            
            statement = (
                f"You have ${budget:.2f} and want to buy {quantity} {item}s. "
                f"Each {item} costs ${price:.2f}. How much money will you have left after your purchase?"
            )
            
            solution_steps = [
                f"1. Calculate total cost: {quantity} × ${price:.2f} = ${total_cost:.2f}",
                f"2. Subtract from your budget: ${budget:.2f} - ${total_cost:.2f} = ${remaining:.2f}",
                f"3. You will have ${remaining:.2f} remaining."
            ]
            
            return Problem(
                statement=statement,
                answer=remaining,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type=problem_type
            )
        
        else:  # shopping_max_price
            max_price = round(budget / quantity, 2)
            
            statement = (
                f"You have ${budget:.2f} and need to buy {quantity} {item}s. "
                "What is the maximum price you can pay for each item without exceeding your budget?"
            )
            
            solution_steps = [
                f"1. Divide your budget by the number of items: ${budget:.2f} ÷ {quantity} = ${max_price:.2f}",
                f"2. The maximum price per item is ${max_price:.2f}",
                f"3. Verify: {quantity} × ${max_price:.2f} = ${budget:.2f} (your total budget)"
            ]
            
            return Problem(
                statement=statement,
                answer=max_price,
                solution_steps=solution_steps,
                difficulty='intermediate',
                problem_type=problem_type
            )
    
    def _generate_drt_problem(self, problem_type: str = None, difficulty: str = None) -> Problem:
        """
        Generate a distance, rate, and time problem.
        
        Args:
            problem_type: Specific type of DRT problem to generate.
                         Options: 'basic', 'two_objects', 'relative_speed'
            difficulty: 'intermediate' or 'hard'. If None, a random level is selected.
        
        Returns:
            Problem object with the generated problem and solution
        """
        if problem_type is None:
            problem_type = random.choice(['basic', 'two_objects', 'relative_speed'])
            
        if difficulty is None:
            difficulty = random.choice(self.difficulty_levels)
        
        if problem_type == 'basic':
            return self._generate_basic_drt_problem(difficulty)
        elif problem_type == 'two_objects':
            return self._generate_two_objects_drt_problem(difficulty)
        else:  # relative_speed
            return self._generate_relative_speed_drt_problem(difficulty)
    
    def _generate_basic_drt_problem(self, difficulty: str) -> Problem:
        """Generate a basic distance, rate, or time problem."""
        # Possible problem variants: find distance, rate, or time
        variant = random.choice(['find_distance', 'find_rate', 'find_time'])
        
        # Generate realistic values based on difficulty
        if difficulty == 'intermediate':
            rate = random.randint(10, 60)  # km/h or mph
            time = random.randint(1, 5)    # hours
        else:  # hard
            rate = random.randint(20, 100)  # km/h or mph
            time = random.uniform(0.5, 4)   # hours (can be fractions)
        
        distance = rate * time
        
        # Round to 2 decimal places for display
        rate = round(rate, 2) if isinstance(rate, float) else rate
        time = round(time, 2) if isinstance(time, float) else time
        distance = round(distance, 2)
        
        # Transportation modes and their units
        modes = [
            ('car', 'km/h', 'kilometers'),
            ('bicycle', 'km/h', 'kilometers'),
            ('train', 'mph', 'miles'),
            ('airplane', 'km/h', 'kilometers')
        ]
        mode, speed_unit, distance_unit = random.choice(modes)
        
        if variant == 'find_distance':
            statement = (
                f"If a {mode} travels at a constant speed of {rate} {speed_unit} "
                f"for {time} hours, how many {distance_unit} does it travel?"
            )
            solution_steps = [
                f"1. Use the formula: Distance = Rate × Time",
                f"2. Plug in the values: Distance = {rate} {speed_unit} × {time} hours",
                f"3. Calculate: {rate} × {time} = {distance} {distance_unit}"
            ]
            answer = distance
            
        elif variant == 'find_rate':
            statement = (
                f"A {mode} travels {distance} {distance_unit} in {time} hours. "
                f"What is its average speed in {speed_unit}?"
            )
            solution_steps = [
                f"1. Use the formula: Rate = Distance / Time",
                f"2. Plug in the values: Rate = {distance} {distance_unit} / {time} hours",
                f"3. Calculate: {distance} / {time} = {rate} {speed_unit}"
            ]
            answer = rate
            
        else:  # find_time
            statement = (
                f"How many hours will it take a {mode} traveling at {rate} {speed_unit} "
                f"to travel {distance} {distance_unit}?"
            )
            solution_steps = [
                f"1. Use the formula: Time = Distance / Rate",
                f"2. Plug in the values: Time = {distance} {distance_unit} / {rate} {speed_unit}",
                f"3. Calculate: {distance} / {rate} = {time} hours"
            ]
            answer = time
        
        return Problem(
            statement=statement,
            answer=answer,
            solution_steps=solution_steps,
            difficulty=difficulty,
            problem_type=f"drt_basic_{variant}"
        )
    
    def _generate_two_objects_drt_problem(self, difficulty: str) -> Problem:
        """Generate a problem with two objects moving toward or away from each other."""
        # Choose if objects are moving toward or away from each other
        direction = random.choice(['toward', 'away'])
        
        # Generate realistic speeds based on difficulty
        if difficulty == 'intermediate':
            speed1 = random.randint(40, 70)  # km/h
            speed2 = random.randint(40, 70)  # km/h
            distance = random.randint(100, 300)  # km
        else:  # hard
            speed1 = random.randint(50, 100)  # km/h
            speed2 = random.randint(50, 100)  # km/h
            distance = random.randint(200, 500)  # km
        
        # Calculate time until meeting/parting
        if direction == 'toward':
            combined_speed = speed1 + speed2
            time = distance / combined_speed
            direction_text = "toward each other"
        else:  # away
            combined_speed = abs(speed1 - speed2)
            if combined_speed == 0:  # Prevent division by zero
                combined_speed = 1
            time = distance / combined_speed
            direction_text = "in opposite directions"
        
        # Round time to 2 decimal places
        time = round(time, 2)
        
        # Transportation modes
        modes = [
            ('car', 'truck'),
            ('train', 'train'),
            ('bicycle', 'scooter'),
            ('motorcycle', 'car')
        ]
        mode1, mode2 = random.choice(modes)
        
        # Generate the problem
        if direction == 'toward':
            statement = (
                f"Two {mode1}s start {distance} km apart and travel {direction_text} at "
                f"{speed1} km/h and {speed2} km/h, respectively. How many hours will it take "
                "for them to meet?"
            )
        else:  # away
            statement = (
                f"Two {mode1}s start from the same point and travel {direction_text} at "
                f"{speed1} km/h and {speed2} km/h, respectively. How many hours will it take "
                f"for them to be {distance} km apart?"
            )
        
        solution_steps = [
            f"1. When objects move {direction_text}, their relative speed is " + 
                (f"the sum of their speeds: {speed1} + {speed2} = {combined_speed} km/h" 
                 if direction == 'toward' else 
                 f"the difference of their speeds: |{speed1} - {speed2}| = {combined_speed} km/h"),
            f"2. Use the formula: Time = Distance / Speed",
            f"3. Plug in the values: Time = {distance} km / {combined_speed} km/h",
            f"4. Calculate: {distance} / {combined_speed} = {time} hours"
        ]
        
        return Problem(
            statement=statement,
            answer=time,
            solution_steps=solution_steps,
            difficulty=difficulty,
            problem_type=f"drt_two_objects_{direction}"
        )
    
    def _generate_relative_speed_drt_problem(self, difficulty: str) -> Problem:
        """Generate a problem involving relative speed (overtaking/catching up)."""
        # Generate speeds ensuring speed1 > speed2 for overtaking
        if difficulty == 'intermediate':
            speed1 = random.randint(50, 80)  # km/h (faster object)
            speed2 = random.randint(20, speed1 - 10)  # km/h (slower object)
            head_start = random.randint(1, 4)  # hours
        else:  # hard
            speed1 = random.randint(60, 120)  # km/h (faster object)
            speed2 = random.randint(30, speed1 - 15)  # km/h (slower object)
            head_start = random.uniform(0.5, 3)  # hours (can be fractions)
        
        # Calculate time to catch up
        relative_speed = speed1 - speed2
        distance = speed2 * head_start  # Distance covered by the slower object
        time = distance / relative_speed
        
        # Round to 2 decimal places for display
        head_start = round(head_start, 2) if isinstance(head_start, float) else head_start
        time = round(time, 2)
        distance = round(distance, 2)
        
        # Transportation modes
        modes = [
            ('car', 'truck', 'leaves a rest stop'),
            ('train', 'freight train', 'departs a station'),
            ('runner', 'walker', 'starts walking'),
            ('bicycle', 'jogger', 'starts jogging')
        ]
        mode1, mode2, departure_verb = random.choice(modes)
        
        # Generate the problem
        statement = (
            f"A {mode1} traveling at {speed1} km/h starts chasing a {mode2} that "
            f"{departure_verb} {head_start} hours earlier. If the {mode2} is traveling at "
            f"{speed2} km/h, how many hours will it take for the {mode1} to catch up?"
        )
        
        solution_steps = [
            f"1. First, find the head start distance: {speed2} km/h × {head_start} h = {distance} km",
            f"2. The {mode1} gains on the {mode2} at a rate of: {speed1} km/h - {speed2} km/h = {relative_speed} km/h",
            f"3. Time to catch up = Head start distance / Relative speed",
            f"4. Calculate: {distance} km / {relative_speed} km/h = {time} hours"
        ]
        
        return Problem(
            statement=statement,
            answer=time,
            solution_steps=solution_steps,
            difficulty=difficulty,
            problem_type="drt_relative_speed"
        )

    def _generate_work_rate_problem(self, problem_type: str = None, difficulty: str = None) -> Problem:
        """
        Generate a work rate problem.
        
        Args:
            problem_type: Specific type of work rate problem to generate.
                         Options: 'basic', 'combined', 'efficiency'
            difficulty: 'intermediate' or 'hard'. If None, a random level is selected.
        
        Returns:
            Problem object with the generated problem and solution
        """
        if problem_type is None:
            problem_type = random.choice(['basic', 'combined', 'efficiency'])
            
        if difficulty is None:
            difficulty = random.choice(self.difficulty_levels)
        
        if problem_type == 'basic':
            return self._generate_basic_work_rate_problem()
        elif problem_type == 'combined':
            return self._generate_combined_work_rate_problem()
        elif problem_type == 'efficiency':
            return self._generate_efficiency_work_rate_problem(difficulty)
        else:
            raise ValueError(f"Unknown work rate problem type: {problem_type}")
    
    def _generate_basic_work_rate_problem(self) -> Problem:
        """Generate a basic work rate problem (intermediate difficulty)."""
        # Random work contexts
        contexts = [
            ('paint a room', 'painter', 'hours'),
            ('mow a lawn', 'gardener', 'hours'),
            ('write an essay', 'writer', 'hours'),
            ('bake a cake', 'baker', 'hours'),
            ('read a book', 'reader', 'hours')
        ]
        task, worker, time_unit = random.choice(contexts)
        
        # Generate random values
        time_taken = random.randint(2, 10)  # 2-10 hours
        work_done = random.randint(1, 4)    # 1-4 units of work
        
        # Calculate rate
        rate = work_done / time_taken
        
        # Generate problem
        problem = f"If a {worker} can {task} in {time_taken} {time_unit}, how much of the task can they complete in {work_done} {time_unit}?"
        
        # Calculate answer (work done in given time)
        answer = rate * work_done
        
        # Generate solution steps
        solution = [
            f"1. First, find the work rate: {work_done} units / {time_taken} {time_unit} = {rate:.2f} units per {time_unit}",
            f"2. Then, calculate work done in {work_done} {time_unit}: {rate:.2f} units/{time_unit} × {work_done} {time_unit} = {answer:.2f} units",
            f"3. The {worker} can complete {answer:.2f} units of the task in {work_done} {time_unit}."
        ]
        
        return Problem(
            statement=problem,
            answer=round(answer, 2),
            solution_steps=solution,
            difficulty='intermediate',
            problem_type='work_rate_basic'
        )
    
    def _generate_combined_work_rate_problem(self) -> Problem:
        """Generate a combined work rate problem (hard difficulty)."""
        # Worker types and tasks
        workers = [
            ('Alice', 'painter', 'paint a room'),
            ('Bob', 'gardener', 'mow a lawn'),
            ('Charlie', 'writer', 'write a report'),
            ('Diana', 'baker', 'bake a cake'),
            ('Eve', 'cleaner', 'clean a house')
        ]
        
        # Select two different workers
        worker1, worker2 = random.sample(workers, 2)
        name1, job1, task1 = worker1
        name2, job2, task2 = worker2
        
        # Generate random times (in hours)
        time1 = random.randint(2, 6)
        time2 = random.randint(2, 6)
        
        # Make sure times are different to avoid division by zero
        while time1 == time2:
            time2 = random.randint(2, 6)
        
        # Calculate combined rate
        rate1 = 1 / time1
        rate2 = 1 / time2
        combined_rate = rate1 + rate2
        time_together = 1 / combined_rate
        
        # Format time as fraction if needed
        if time_together.is_integer():
            time_str = f"{int(time_together)}"
        else:
            from fractions import Fraction
            time_frac = Fraction(time_together).limit_denominator()
            time_str = f"{time_frac.numerator}/{time_frac.denominator}"
        
        # Generate problem
        problem = f"{name1} can {task1} in {time1} hours. {name2} can {task2} in {time2} hours. " \
                 f"How long will it take them to complete one task if they work together?"
        
        # Generate solution steps
        solution = [
            f"1. {name1}'s rate: 1 task / {time1} hours = {1/time1:.3f} tasks per hour",
            f"2. {name2}'s rate: 1 task / {time2} hours = {1/time2:.3f} tasks per hour",
            f"3. Combined rate: {1/time1:.3f} + {1/time2:.3f} = {combined_rate:.3f} tasks per hour",
            f"4. Time to complete 1 task: 1 / {combined_rate:.3f} = {time_together:.2f} hours",
            f"5. Working together, they can complete the task in {time_str} hours ({time_together*60:.0f} minutes)."
        ]
        
        return Problem(
            statement=problem,
            answer=round(time_together, 2),
            solution_steps=solution,
            difficulty='hard',
            problem_type='work_rate_combined'
        )
    
    def _generate_efficiency_work_rate_problem(self, difficulty: str = 'intermediate') -> Problem:
        """Generate a work rate problem involving different efficiencies."""
        # Worker types and tasks
        workers = [
            ('Alice', 'painter'),
            ('Bob', 'gardener'),
            ('Charlie', 'carpenter'),
            ('Diana', 'baker'),
            ('Eve', 'cleaner')
        ]
        
        # Select two different workers
        worker1, worker2 = random.sample(workers, 2)
        name1, job1 = worker1
        name2, job2 = worker2
        
        # Generate random efficiency ratio (e.g., 2 means worker1 is twice as fast)
        if difficulty == 'intermediate':
            ratio = random.choice([2, 3, 4])  # Simple ratios for intermediate
        else:
            ratio = random.choice([1.5, 2.5, 3.5])  # More complex ratios for hard
        
        # Generate base time (in hours)
        base_time = random.randint(3, 8)
        
        # Calculate individual times
        time1 = base_time
        time2 = base_time * ratio
        
        # Calculate combined rate
        rate1 = 1 / time1
        rate2 = 1 / time2
        combined_rate = rate1 + rate2
        time_together = 1 / combined_rate
        
        # Format time as fraction if needed
        if time_together.is_integer():
            time_str = f"{int(time_together)}"
        else:
            from fractions import Fraction
            time_frac = Fraction(time_together).limit_denominator()
            time_str = f"{time_frac.numerator}/{time_frac.denominator}"
        
        # Generate problem
        problem = f"{name1} can complete a job in {time1} hours. {name2} is {ratio}x {'slower' if ratio > 1 else 'faster'}. " \
                 f"How long will it take them to complete the job if they work together?"
        
        # Generate solution steps
        solution = [
            f"1. {name1}'s rate: 1 job / {time1} hours = {1/time1:.3f} jobs per hour",
            f"2. Since {name2} is {ratio}x {'slower' if ratio > 1 else 'faster'}, their time is {time1} × {ratio} = {time2} hours",
            f"3. {name2}'s rate: 1 job / {time2} hours = {1/time2:.3f} jobs per hour",
            f"4. Combined rate: {1/time1:.3f} + {1/time2:.3f} = {combined_rate:.3f} jobs per hour",
            f"5. Time to complete 1 job: 1 / {combined_rate:.3f} = {time_together:.2f} hours",
            f"6. Working together, they can complete the job in {time_str} hours ({time_together*60:.0f} minutes)."
        ]
        
        return Problem(
            statement=problem,
            answer=round(time_together, 2),
            solution_steps=solution,
            difficulty=difficulty,
            problem_type='work_rate_efficiency'
        )

# Example usage
if __name__ == "__main__":
    generator = SimpleEquationsGenerator()
    
    # Generate a random problem
    print("Generating a random work rate problem:")
    problem = generator.generate_problem('work_rate')
    print(f"\nProblem: {problem.statement}")
    print(f"\nSolution steps:")
    for i, step in enumerate(problem.solution_steps, 1):
        print(f"{i}. {step}")
    print(f"\nAnswer: {problem.answer}")
    print(f"Type: {problem.problem_type}")
    print(f"Difficulty: {problem.difficulty}")
