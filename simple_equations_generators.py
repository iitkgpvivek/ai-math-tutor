"""
Simple Equations Word Problem Generators for Grade 7 Math

This module provides a collection of word problem generators focused on simple equations.
The problems are designed to help students practice setting up and solving equations
in various real-world contexts.
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
                         Currently supports 'age_related', 'number', and 'consecutive_integers'.
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
            # Age-related problems
            'age_sum': (self._generate_age_sum_problem, False),
            'age_difference': (self._generate_age_difference_problem, False),
            'age_ratio': (self._generate_age_ratio_problem, False),
            'age_ratio_change': (self._generate_age_ratio_change_problem, True),
            'age_three_people': (self._generate_age_three_people_problem, True),
            'age_combined_conditions': (self._generate_age_combined_conditions_problem, True),
            
            # Number problems
            'number': (self._generate_basic_number_problem, False),
            'consecutive_integers': (self._generate_consecutive_integers_problem, False),
            'number_reversal': (self._generate_number_reversal_problem, False),
            
            # Money problems
            'money_basic': (self._generate_basic_money_problem, False),
            'money_discount': (self._generate_discount_problem, False),
            'money_profit_loss': (self._generate_profit_loss_problem, False),
            
            # Geometry problems
            'rectangle_perimeter': (self._generate_rectangle_perimeter_problem, False),
            'rectangle_area': (self._generate_rectangle_area_problem, False),
            'square_perimeter': (self._generate_square_perimeter_problem, False),
            'square_area': (self._generate_square_area_problem, False),
            'triangle_perimeter': (self._generate_triangle_perimeter_problem, False),
            'triangle_area': (self._generate_triangle_area_problem, False),
            'circle_circumference': (self._generate_circle_circumference_problem, False),
            'circle_area': (self._generate_circle_area_problem, False),
            'geometry': (self._generate_geometry_problem, False)  # Random geometry problem
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

# Example usage
if __name__ == "__main__":
    generator = SimpleEquationsGenerator()
    
    # Generate a random problem
    print("Generating a random age-related problem:")
    problem = generator.generate_problem('age_related')
    print(f"\nProblem: {problem.statement}")
    print(f"\nSolution steps:")
    for i, step in enumerate(problem.solution_steps, 1):
        print(f"{i}. {step}")
    print(f"\nAnswer: {problem.answer}")
