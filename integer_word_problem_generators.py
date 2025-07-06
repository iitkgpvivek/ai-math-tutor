"""
Integer Word Problem Generators for Grade 7 Math

This module provides a collection of word problem generators that focus on integer operations
in real-world contexts. The problems are designed to be engaging and relevant to 7th-grade students.
"""
import random
from typing import Tuple, Union, List, Dict, Any

class IntegerWordProblemGenerator:
    """Generator for integer word problems with varying difficulty levels."""
    
    def generate_problem(self, difficulty: str = 'medium') -> Tuple[str, Union[int, str, float]]:
        """Generate a word problem of the specified difficulty.
        
        Args:
            difficulty: 'easy', 'medium', or 'hard'
            
        Returns:
            Tuple of (problem_statement, answer)
        """
        problem_type = random.choice([
            'temperature', 'elevation', 'money', 'sequence', 'average',
            'quiz_scoring', 'sports', 'financial', 'academic_competition',
            'real_world', 'advanced_challenge', 'classroom', 'puzzle',
            'multi_step', 'assessment', 'real_life_scenario'
        ])
        
        if problem_type == 'temperature':
            return self._generate_temperature_problem(difficulty)
        elif problem_type == 'elevation':
            return self._generate_elevation_problem(difficulty)
        elif problem_type == 'money':
            return self._generate_money_problem(difficulty)
        elif problem_type == 'sequence':
            return self._generate_sequence_problem(difficulty)
        elif problem_type == 'average':
            return self._generate_average_problem(difficulty)
        elif problem_type == 'quiz_scoring':
            return self._generate_quiz_scoring_problem(difficulty)
        elif problem_type == 'sports':
            return self._generate_sports_games_problem(difficulty)
        elif problem_type == 'financial':
            return self._generate_financial_problem(difficulty)
        elif problem_type == 'academic_competition':
            return self._generate_academic_competition_problem(difficulty)
        elif problem_type == 'real_world':
            return self._generate_real_world_problem(difficulty)
        elif problem_type == 'advanced_challenge':
            return self._generate_advanced_challenge_problem(difficulty)
        elif problem_type == 'classroom':
            return self._generate_classroom_problem(difficulty)
        elif problem_type == 'puzzle':
            return self._generate_puzzle_problem(difficulty)
        elif problem_type == 'multi_step':
            return self._generate_multi_step_problem(difficulty)
        elif problem_type == 'assessment':
            return self._generate_assessment_problem(difficulty)
        else:  # real_life_scenario
            return self._generate_real_life_scenario(difficulty)
    
    def _generate_temperature_problem(self, difficulty: str) -> Tuple[str, int]:
        """Generate temperature change problems."""
        if difficulty == 'easy':
            temp1 = random.randint(-10, 10)
            change = random.randint(1, 10)
            direction = random.choice(['increased', 'decreased'])
            if direction == 'increased':
                temp2 = temp1 + change
            else:
                temp2 = temp1 - change
            problem = f"The temperature was {temp1}°C. It then {direction} by {change}°C. What is the new temperature?"
            return problem, temp2
            
        elif difficulty == 'medium':
            temp1 = random.randint(-20, 20)
            changes = [random.randint(1, 5) for _ in range(2)]
            directions = [random.choice(['rose', 'fell']) for _ in range(2)]
            
            temp = temp1
            problem = f"The temperature was {temp1}°C. "
            for i in range(2):
                if directions[i] == 'rose':
                    temp += changes[i]
                else:
                    temp -= changes[i]
                problem += f"Then it {directions[i]} by {changes[i]}°C. "
            problem += "What is the final temperature?"
            return problem, temp
            
        else:  # hard
            days = random.randint(3, 5)
            temps = [random.randint(-15, 15) for _ in range(days)]
            avg = sum(temps) / days
            problem = f"Over {days} days, the temperatures were: {', '.join(map(str, temps))}°C. "
            problem += "What was the average temperature?"
            return problem, round(avg, 1)
    
    def _generate_elevation_problem(self, difficulty: str) -> Tuple[str, int]:
        """Generate elevation change problems."""
        if difficulty == 'easy':
            elevation = random.randint(0, 1000)
            change = random.randint(10, 100)
            direction = random.choice(['climbed', 'descended'])
            if direction == 'climbed':
                new_elevation = elevation + change
            else:
                new_elevation = max(0, elevation - change)
            problem = f"A hiker starts at {elevation}m above sea level. "
            problem += f"After {direction} {change}m, what is the new elevation?"
            return problem, new_elevation
            
        elif difficulty == 'medium':
            elevation = random.randint(0, 2000)
            changes = [random.randint(20, 200) for _ in range(2)]
            directions = [random.choice(['climbed', 'descended']) for _ in range(2)]
            
            current = elevation
            problem = f"A mountain climber starts at {elevation}m. "
            for i in range(2):
                if directions[i] == 'climbed':
                    current += changes[i]
                else:
                    current = max(0, current - changes[i])
                problem += f"Then {directions[i]} {changes[i]}m. "
            problem += "What is the final elevation?"
            return problem, current
            
        else:  # hard
            elevation = random.randint(0, 3000)
            num_changes = random.randint(3, 5)
            changes = [random.randint(50, 300) for _ in range(num_changes)]
            directions = [random.choice(['climbed', 'descended']) for _ in range(num_changes)]
            
            current = elevation
            problem = f"A scientific expedition starts at {elevation}m. "
            for i in range(num_changes):
                if directions[i] == 'climbed':
                    current += changes[i]
                else:
                    current = max(0, current - changes[i])
                problem += f"Then {directions[i]} {changes[i]}m. "
            problem += f"By how many meters did the elevation change overall?"
            return problem, current - elevation
    
    def _generate_money_problem(self, difficulty: str) -> Tuple[str, Union[int, str]]:
        """Generate money-related problems."""
        if difficulty == 'easy':
            amount = random.randint(5, 20)
            spent = random.randint(1, amount-1)
            remaining = amount - spent
            problem = f"You have ₹{amount}. You spend ₹{spent}. How much do you have left?"
            return problem, remaining
            
        elif difficulty == 'medium':
            items = [
                ('notebook', 25, 50), ('pens', 5, 20), ('pencils', 3, 15),
                ('eraser', 2, 10), ('ruler', 15, 30)
            ]
            item_name, min_p, max_p = random.choice(items)
            price = random.randint(min_p, max_p)
            quantity = random.randint(2, 5)
            total = price * quantity
            problem = f"A {item_name} costs ₹{price}. How much do {quantity} {item_name}s cost?"
            return problem, total
            
        else:  # hard
            items = [
                ('textbook', 200, 500), ('calculator', 500, 1500),
                ('geometry set', 150, 400), ('school bag', 400, 1000)
            ]
            selected = random.sample(items, 2)
            total = sum(random.randint(min_p, max_p) for _, min_p, max_p in selected)
            discount = random.randint(5, 20)
            discount_amt = (total * discount) // 100
            final_price = total - discount_amt
            
            problem = f"You're buying school supplies: {', '.join(item[0] for item in selected)}. "
            problem += f"The total is ₹{total}. You get a {discount}% discount. "
            problem += "How much do you pay after the discount?"
            return problem, final_price
    
    def _generate_sequence_problem(self, difficulty: str) -> Tuple[str, List[int]]:
        """Generate number sequence problems."""
        if difficulty == 'easy':
            start = random.randint(1, 10)
            step = random.randint(1, 5)
            sequence = [start + i*step for i in range(5)]
            problem = f"Find the next 3 numbers in the sequence: {sequence[0]}, {sequence[1]}, {sequence[2]}, ..."
            return problem, sequence[3:]
            
        elif difficulty == 'medium':
            start = random.randint(-10, 10)
            step = random.randint(-5, -1) if random.random() < 0.5 else random.randint(1, 5)
            sequence = [start + i*step for i in range(4)]
            problem = f"Find the next 3 numbers in the sequence: {sequence[0]}, {sequence[1]}, {sequence[2]}, {sequence[3]}, ..."
            return problem, [sequence[-1] + step, sequence[-1] + 2*step, sequence[-1] + 3*step]
            
        else:  # hard
            # Fibonacci-like sequence
            a, b = random.randint(1, 5), random.randint(1, 5)
            sequence = [a, b, a+b, b+(a+b)]
            problem = f"Find the next 3 numbers in the sequence: {sequence[0]}, {sequence[1]}, {sequence[2]}, {sequence[3]}, ..."
            next1 = sequence[-2] + sequence[-1]
            next2 = sequence[-1] + next1
            next3 = next1 + next2
            return problem, [next1, next2, next3]
    
    def _generate_average_problem(self, difficulty: str) -> Tuple[str, Union[int, float]]:
        """Generate average calculation problems."""
        if difficulty == 'easy':
            numbers = [random.randint(1, 10) for _ in range(3)]
            avg = sum(numbers) / len(numbers)
            problem = f"Find the average of {', '.join(map(str, numbers))}."
            return problem, avg
            
        elif difficulty == 'medium':
            count = random.randint(4, 6)
            numbers = [random.randint(1, 20) for _ in range(count)]
            avg = sum(numbers) / len(numbers)
            problem = f"Calculate the average of {', '.join(map(str, numbers))}."
            return problem, round(avg, 2)
            
        else:  # hard
            count = random.randint(5, 8)
            numbers = [random.randint(-15, 15) for _ in range(count)]
            avg = sum(numbers) / len(numbers)
            problem = f"Find the average of these numbers (some may be negative): {', '.join(map(str, numbers))}."
            return problem, round(avg, 2)
    
    def _generate_quiz_scoring_problem(self, difficulty: str) -> Tuple[str, Union[int, str]]:
        """Generate quiz/test scoring problems."""
        if difficulty == 'easy':
            correct = random.randint(5, 10)
            total = random.randint(correct, correct + 5)
            score = f"{correct}/{total}"
            problem = f"In a quiz with {total} questions, you got {correct} correct. What's your score as a fraction?"
            return problem, score
            
        elif difficulty == 'medium':
            correct = random.randint(8, 15)
            incorrect = random.randint(1, 5)
            total = correct + incorrect
            percentage = (correct / total) * 100
            problem = f"In a test with {total} questions, you got {correct} correct and {incorrect} wrong. What's your percentage score?"
            return problem, round(percentage, 1)
            
        else:  # hard
            total = random.randint(10, 20)
            correct = random.randint(5, total - 2)
            incorrect = random.randint(1, total - correct)
            unanswered = total - correct - incorrect
            points = correct * 4 - incorrect  # 4 points per correct, -1 per incorrect
            
            problem = f"A test has {total} questions. You answered {correct} correctly, "
            problem += f"got {incorrect} wrong, and left {unanswered} unanswered. "
            problem += "If correct answers give +4 points and incorrect answers -1 point, what's your total score?"
            return problem, points
    
    def _generate_sports_games_problem(self, difficulty: str) -> Tuple[str, Union[int, str]]:
        """Generate sports and games scoring problems."""
        sports = [
            ('basketball', [1, 2, 3]),  # free throw, field goal, 3-pointer
            ('football', [1, 3, 6]),    # extra point, field goal, touchdown
            ('hockey', [1, 2]),         # goal, assist
            ('cricket', [1, 4, 6])      # single, boundary, six
        ]
        sport, points = random.choice(sports)
        
        if difficulty == 'easy':
            score = random.choice(points)
            problem = f"In {sport}, what's the value of a {self._get_score_name(score, sport)}?"
            return problem, score
            
        elif difficulty == 'medium':
            num_scores = random.randint(2, 3)
            scores = random.choices(points, k=num_scores)
            total = sum(scores)
            problem = f"In a {sport} game, a team scores "
            problem += ", ".join([f"a {self._get_score_name(s, sport)}" for s in scores[:-1]])
            problem += f", and a {self._get_score_name(scores[-1], sport)}. What's their total score?"
            return problem, total
            
        else:  # hard
            team1 = sum(random.choices(points, k=random.randint(3, 6)))
            team2 = sum(random.choices(points, k=random.randint(3, 6)))
            winner = "Team A" if team1 > team2 else "Team B" if team2 > team1 else "It's a tie"
            problem = f"In a {sport} game, Team A scored {team1} points and Team B scored {team2} points. Who won?"
            return problem, winner
    
    def _get_score_name(self, points: int, sport: str) -> str:
        """Helper to get the name of a score in a sport."""
        if sport == 'basketball':
            return {1: 'free throw', 2: 'two-point shot', 3: 'three-pointer'}.get(points, f"{points}-point shot")
        elif sport == 'football':
            return {1: 'extra point', 3: 'field goal', 6: 'touchdown'}.get(points, f"{points}-point play")
        elif sport == 'hockey':
            return {1: 'goal', 2: 'assist'}.get(points, f"{points}-point play")
        elif sport == 'cricket':
            return {1: 'single', 4: 'boundary', 6: 'six'}.get(points, f"{points} runs")
        return f"{points}-point score"
    
    def _generate_financial_problem(self, difficulty: str) -> Tuple[str, Union[int, float]]:
        """Generate financial literacy problems."""
        if difficulty == 'easy':
            allowance = random.randint(50, 100)
            spent = random.randint(10, allowance-1)
            remaining = allowance - spent
            problem = f"You get ₹{allowance} weekly allowance. You spent ₹{spent}. How much do you have left?"
            return problem, remaining
            
        elif difficulty == 'medium':
            principal = random.randint(1000, 5000)
            rate = random.choice([2, 3, 5, 7])
            time = random.choice([1, 2, 3])
            interest = (principal * rate * time) // 100
            total = principal + interest
            problem = f"You deposit ₹{principal} in a savings account with {rate}% annual interest. "
            problem += f"How much interest will you earn in {time} year{'s' if time > 1 else ''}?"
            return problem, interest
            
        else:  # hard
            item_price = random.randint(500, 2000)
            discount = random.choice([10, 15, 20, 25])
            discount_amt = (item_price * discount) // 100
            final_price = item_price - discount_amt
            tax_rate = random.choice([5, 8, 12, 18])
            tax = (final_price * tax_rate) // 100
            total = final_price + tax
            
            problem = f"A laptop costs ₹{item_price}. There's a {discount}% discount, "
            problem += f"and then {tax_rate}% tax is added. What's the final price?"
            return problem, total
    
    def _generate_academic_competition_problem(self, difficulty: str) -> Tuple[str, Union[int, str]]:
        """Generate academic competition problems."""
        subjects = ['math', 'science', 'history', 'geography', 'spelling']
        subject = random.choice(subjects)
        
        if difficulty == 'easy':
            points = random.randint(5, 20)
            problem = f"In a {subject} bee, you get {points} points for each correct answer. "
            problem += f"If you answer 3 questions correctly, how many points do you get?"
            return problem, points * 3
            
        elif difficulty == 'medium':
            base_points = random.randint(10, 20)
            bonus = random.randint(5, 10)
            questions = random.randint(5, 10)
            correct = random.randint(3, questions-1)
            total = (base_points * correct) + (bonus if correct == questions else 0)
            
            problem = f"In a {subject} competition, each correct answer is worth {base_points} points. "
            problem += f"Getting all {questions} questions right gives a {bonus}-point bonus. "
            problem += f"If you got {correct} right, what's your score?"
            return problem, total
            
        else:  # hard
            teams = random.randint(3, 6)
            rounds = random.randint(3, 5)
            scores = [[random.randint(0, 10) for _ in range(teams)] for _ in range(rounds)]
            totals = [sum(round_scores[i] for round_scores in scores) for i in range(teams)]
            winning_score = max(totals)
            winner = totals.index(winning_score) + 1
            
            problem = f"In a {subject} bowl with {teams} teams over {rounds} rounds, "
            problem += f"the scores are: {', '.join(f'Team {i+1}: {total}' for i, total in enumerate(totals))}. "
            problem += "Which team won and with what score?"
            return problem, f"Team {winner} with {winning_score} points"
    
    def _find_smallest_number_greater_than(self, n: int, a: int, rem_a: int, b: int, rem_b: int) -> int:
        """Find the smallest number > n that leaves remainder rem_a when divided by a and rem_b when divided by b."""
        x = n + 1
        while True:
            if x % a == rem_a and x % b == rem_b:
                return x
            x += 1
            # Safety check to prevent infinite loops
            if x > n + 1000:
                return -1

    def _generate_real_world_problem(self, difficulty: str) -> Tuple[str, Union[int, str]]:
        """Generate real-world application problems with increased complexity."""
        scenarios = [
            # Elevator with multiple stops
            ('elevator', 'floors', 1, 30, 1, 5, 
             'An elevator starts at floor {}. It goes up {} floors, down {} floors, then up {} more floors. On which floor does it stop?'),
            
            # Temperature change with multiple steps
            ('temperature', '°C', -15, 40, 2, 15, 
             'The temperature is {}°C at 6 AM. By 9 AM it rises by {}°C, then falls by {}°C by noon. ' 
             'In the afternoon, it rises by {}°C. What is the final temperature?'),
            
            # Financial scenario
            ('bank account', 'dollars', 100, 1000, 10, 100,
             'You have ${} in your bank account. You deposit ${} on Monday, withdraw ${} on Wednesday, ' 
             'and deposit another ${} on Friday. What is your final balance?')
        ]
        scenario, unit, min_start, max_start, min_change, max_change, template = random.choice(scenarios)
        
        if difficulty == 'easy':
            start = random.randint(min_start, max_start)
            changes = [random.randint(min_change, max_change) for _ in range(3)]
            
            if scenario == 'elevator':
                answer = start + changes[0] - changes[1] + changes[2]
                problem = template.format(start, changes[0], changes[1], changes[2])
            elif scenario == 'temperature':
                answer = start + changes[0] - changes[1] + changes[2]
                problem = template.format(start, changes[0], changes[1], changes[2])
            else:  # bank account
                answer = start + changes[0] - changes[1] + changes[2]
                problem = template.format(start, changes[0], changes[1], changes[2])
                
            return problem, answer
            
        elif difficulty == 'medium':
            start = random.randint(min_start, max_start)
            changes = [random.randint(min_change, max_change) for _ in range(2)]
            
            if scenario == 'elevator':
                answer = start + changes[0] - changes[1]
                problem = template.format(start, changes[0], changes[1], 0)
            elif scenario == 'temperature':
                answer = start + changes[0] - changes[1]
                problem = template.format(start, changes[0], changes[1], 0)
            else:  # bank account
                answer = start + changes[0] - changes[1]
                problem = template.format(start, changes[0], changes[1], 0)
                
            return problem, answer
            
        else:  # hard
            start = random.randint(min_start, max_start)
            num_changes = random.randint(3, 5)
            changes = [random.randint(min_change, max_change) for _ in range(num_changes)]
            
            current = start
            problem = f"A {scenario} starts at {start} {unit}. "
            for i in range(num_changes):
                if scenario == 'elevator':
                    current += changes[i]
                elif scenario == 'temperature':
                    current += changes[i]
                else:  # bank account
                    if i % 2 == 0:
                        current += changes[i]
                    else:
                        current -= changes[i]
                problem += f"It goes {changes[i]} {unit}. "
            problem += f"What's the final {unit.split()[0]}?"
            return problem, current
    
    def _generate_advanced_challenge_problem(self, difficulty: str) -> Tuple[str, Union[int, float, str]]:
        """Generate advanced challenge problems involving multiple operations and concepts."""
        if difficulty == 'easy':
            # Three-step problems with larger numbers
            a, b, c, d = [random.randint(10, 50) for _ in range(4)]
            ops = random.choice([
                (('+', '+', '-'), f"Add {a} and {b}, then add {c}, and finally subtract {d}"),
                (('*', '+', '-'), f"Multiply {a} by {b}, add {c}, then subtract {d}"),
                (('+', '*', '-'), f"Add {a} and {b}, multiply by {c}, then subtract {d}")
            ])
            
            op1, op2, op3 = ops[0]
            problem = f"{ops[1]}. What is the result?"
            
            # Calculate answer
            if op1 == '+':
                result = a + b
            elif op1 == '*':
                result = a * b
                
            if op2 == '+':
                result += c
            elif op2 == '*':
                result *= c
                
            if op3 == '-':
                result -= d
            elif op3 == '+':
                result += d
                
            return problem, result
        
        elif difficulty == 'medium':
            # Problems with multiplication/division and addition/subtraction
            a, b, c = random.randint(2, 12), random.randint(2, 12), random.randint(1, 20)
            op1, op2 = random.choice([('×', '+'), ('×', '-'), ('÷', '+'), ('÷', '-')])
            
            if op1 == '×' and op2 == '+':
                answer = a * b + c
                problem = f"Multiply {a} by {b}, then add {c}."
            elif op1 == '×' and op2 == '-':
                answer = a * b - c
                problem = f"Multiply {a} by {b}, then subtract {c}."
            elif op1 == '÷' and op2 == '+':
                # Ensure integer division
                a = b * random.randint(1, 5)
                answer = a // b + c
                problem = f"Divide {a} by {b}, then add {c}."
            else:  # '÷' and '-'
                # Ensure positive result
                a = b * random.randint(2, 5)
                c = random.randint(1, a//b - 1)
                answer = a // b - c
                problem = f"Divide {a} by {b}, then subtract {c}."
                
        else:  # hard
            # Complex multi-step problems with order of operations and larger numbers
            nums = [random.randint(5, 40) for _ in range(6)]
            
            # Choose between different problem structures
            problem_type = random.choice([
                # Nested operations with fractions
                (f"Calculate: (({nums[0]} + {nums[1]}) × {nums[2]}) - ({nums[3]} × {nums[4]}) + {nums[5]}",
                 lambda: ((nums[0] + nums[1]) * nums[2]) - (nums[3] * nums[4]) + nums[5]),
                 
                # Multi-step with division and multiplication
                (f"A train travels {nums[0]} km in {nums[1]} hours, then {nums[2]} km in {nums[3]} hours. "
                 f"What's the average speed for the entire journey in km/h?",
                 lambda: round((nums[0] + nums[2]) / ((nums[1] + nums[3])), 2)),
                 
                # Real-world scenario with multiple operations
                (f"A store sells items for ${nums[0]}, ${nums[1]}, and ${nums[2]}. "
                 f"If you buy {nums[3]} of the first item, {nums[4]} of the second, "
                 f"and {nums[5]} of the third, how much do you spend in total?",
                 lambda: (nums[0] * nums[3]) + (nums[1] * nums[4]) + (nums[2] * nums[5])),
                 
                # Number theory problem
                (f"Find the smallest number greater than {nums[0]} that leaves a remainder of {nums[1]%5} "
                 f"when divided by 5 and a remainder of {nums[2]%7} when divided by 7.",
                 lambda: self._find_smallest_number_greater_than(nums[0], 5, nums[1]%5, 7, nums[2]%7))
            ])
            
            problem, answer_func = problem_type
            return problem, answer_func()
        
        return problem, answer
    
    def _generate_classroom_problem(self, difficulty: str) -> Tuple[str, Union[int, str]]:
        """Generate classroom management problems."""
        if difficulty == 'easy':
            students = random.randint(20, 30)
            groups = random.choice([2, 4, 5])
            per_group = students // groups
            problem = f"A class has {students} students. If they are divided into {groups} equal groups, how many students are in each group?"
            return problem, per_group
            
        elif difficulty == 'medium':
            points = random.randint(50, 100)
            lost = random.randint(5, 15)
            remaining = points - lost
            problem = f"Your class starts with {points} behavior points. If they lose {lost} points, how many points remain?"
            return problem, remaining
            
        else:  # hard
            books = random.randint(20, 40)
            students = random.randint(5, 10)
            books_per = books // students
            remainder = books % students
            problem = f"A teacher has {books} books to distribute equally among {students} students. "
            problem += f"How many books does each student get, and how many are left over?"
            return problem, f"{books_per} books each with {remainder} left over"
    
    def _generate_puzzle_problem(self, difficulty: str) -> Tuple[str, Union[int, str]]:
        """Generate puzzle problems like number line jumps, code breaking, or magic squares."""
        if difficulty == 'easy':
            # Number line jumps
            start = random.randint(-5, 5)
            jumps = random.randint(2, 4)
            direction = random.choice(['left', 'right'])
            distance = random.randint(1, 3)
            
            if direction == 'right':
                end = start + (jumps * distance)
            else:
                end = start - (jumps * distance)
                
            problem = f"Start at {start} on a number line. Jump {distance} units to the {direction} {jumps} times. Where do you land?"
            return problem, end
            
        elif difficulty == 'medium':
            # Simple code breaking
            code = random.sample('ABCDEF', 4)
            values = {c: random.randint(1, 5) for c in code}
            total = sum(values.values())
            
            problem = "If "
            problem += ", ".join([f"{c} = {v}" for c, v in values.items()])
            problem += f", what is {' + '.join(code)}?"
            return problem, total
            
        else:  # hard
            # Magic square (3x3 with numbers 1-9)
            # All rows, columns, and diagonals sum to 15
            magic_square = [
                [8, 1, 6],
                [3, 5, 7],
                [4, 9, 2]
            ]
            # Randomly rotate or flip the square
            if random.random() < 0.5:
                magic_square = [row[::-1] for row in magic_square]  # Flip horizontally
            if random.random() < 0.5:
                magic_square = magic_square[::-1]  # Flip vertically
            if random.random() < 0.5:
                # Transpose (swap rows and columns)
                magic_square = [list(row) for row in zip(*magic_square)]
            
            # Hide some numbers
            hidden = []
            for i in range(3):
                for j in range(3):
                    if random.random() < 0.5:  # 50% chance to hide each number
                        hidden.append((i, j, magic_square[i][j]))
                        magic_square[i][j] = '?'
            
            problem = "Complete the magic square (each row, column, and diagonal sums to 15):\n"
            problem += "\n".join([" ".join(map(str, row)) for row in magic_square])
            problem += "\nWhat number goes in the position with '?'?"
            
            # If multiple numbers are hidden, just ask about the first one
            if hidden:
                return problem, hidden[0][2]
            else:
                return "All numbers are visible in the magic square!", 15
    
    def _generate_multi_step_problem(self, difficulty: str) -> Tuple[str, Union[int, float]]:
        """Generate multi-step word problems."""
        if difficulty == 'easy':
            # Simple two-step problem
            a = random.randint(5, 15)
            b = random.randint(1, 5)
            c = random.randint(1, 5)
            answer = (a + b) * c
            problem = f"Add {a} and {b}, then multiply the result by {c}. What's the answer?"
            return problem, answer
            
        elif difficulty == 'medium':
            # Three-step problem
            a = random.randint(10, 20)
            b = random.randint(1, 5)
            c = random.randint(5, 10)
            d = random.randint(1, 4)
            answer = (a - b) * c // d
            problem = f"Start with {a}, subtract {b}, multiply by {c}, then divide by {d}. What's the result?"
            return problem, answer
            
        else:  # hard
            # Four-step problem with multiple operations
            a = random.randint(20, 50)
            b = random.randint(5, 10)
            c = random.randint(2, 5)
            d = random.randint(3, 6)
            e = random.randint(2, 4)
            answer = ((a // b) + c) * d - e
            problem = f"Divide {a} by {b}, add {c}, multiply by {d}, then subtract {e}. What's the final answer?"
            return problem, answer
    
    def _generate_assessment_problem(self, difficulty: str) -> Tuple[str, Union[str, int, List[str]]]:
        """Generate assessment-style problems (MCQ, T/F, fill-in, matching)."""
        problem_types = ['mcq', 'true_false', 'fill_in', 'matching']
        problem_type = random.choice(problem_types)
        
        if problem_type == 'mcq':
            a, b = random.randint(1, 20), random.randint(1, 20)
            op = random.choice(['+', '-', '×', '÷'])
            
            if op == '+':
                answer = a + b
                problem = f"What is {a} + {b}?"
            elif op == '-':
                answer = a - b
                problem = f"What is {a} - {b}?"
            elif op == '×':
                answer = a * b
                problem = f"What is {a} × {b}?"
            else:  # ÷
                # Ensure integer division
                a = b * random.randint(1, 10)
                answer = a // b
                problem = f"What is {a} ÷ {b}?"
            
            # Generate distractors
            if difficulty == 'easy':
                options = [answer, answer + 1, answer - 1, answer + 2]
            elif difficulty == 'medium':
                options = [answer, answer + random.randint(1, 3), 
                          answer - random.randint(1, 3), answer + random.choice([-1, 1]) * random.randint(2, 4)]
            else:  # hard
                options = [answer, answer + random.choice([-1, 1]) * random.randint(1, 3),
                          answer + random.choice([-1, 1]) * random.randint(1, 3),
                          answer + random.choice([-2, 2, -3, 3])]
            
            # Remove duplicates and ensure 4 options
            options = list(set(options))
            while len(options) < 4:
                new_option = answer + random.choice([-1, 1]) * random.randint(1, 5)
                if new_option not in options:
                    options.append(new_option)
            
            random.shuffle(options)
            letters = ['A', 'B', 'C', 'D']
            problem += "\n" + "\n".join([f"{letters[i]}. {option}" for i, option in enumerate(options)])
            correct_letter = letters[options.index(answer)]
            return problem, correct_letter
            
        elif problem_type == 'true_false':
            a, b = random.randint(1, 20), random.randint(1, 20)
            op = random.choice(['+', '-', '×', '÷', '>', '<', '='])
            
            if op == '>':
                answer = a > b
                problem = f"True or False: {a} > {b}"
            elif op == '<':
                answer = a < b
                problem = f"True or False: {a} < {b}"
            elif op == '=':
                answer = a == b
                problem = f"True or False: {a} = {b}"
            elif op == '+':
                answer = a + b == random.choice([a + b, a + b + random.choice([-1, 1])])
                problem = f"True or False: {a} + {b} = {a + b if answer else a + b + random.choice([-1, 1])}"
            elif op == '-':
                answer = a - b == random.choice([a - b, a - b + random.choice([-1, 1])])
                problem = f"True or False: {a} - {b} = {a - b if answer else a - b + random.choice([-1, 1])}"
            elif op == '×':
                answer = a * b == random.choice([a * b, a * b + random.choice([-1, 1])])
                problem = f"True or False: {a} × {b} = {a * b if answer else a * b + random.choice([-1, 1])}"
            else:  # ÷
                # Ensure integer division
                a = b * random.randint(1, 10)
                answer = (a // b) == random.choice([a // b, a // b + random.choice([-1, 1])])
                problem = f"True or False: {a} ÷ {b} = {a // b if answer else a // b + random.choice([-1, 1])}"
            
            return problem, "True" if answer else "False"
            
        elif problem_type == 'fill_in':
            a, b = random.randint(1, 20), random.randint(1, 20)
            op = random.choice(['+', '-', '×', '÷'])
            
            if op == '+':
                answer = a + b
                problem = f"Fill in the blank: {a} + {b} = ____"
            elif op == '-':
                answer = a - b
                problem = f"Fill in the blank: {a} - {b} = ____"
            elif op == '×':
                answer = a * b
                problem = f"Fill in the blank: {a} × {b} = ____"
            else:  # ÷
                # Ensure integer division
                a = b * random.randint(1, 10)
                answer = a // b
                problem = f"Fill in the blank: {a} ÷ {b} = ____"
            
            return problem, answer
            
        else:  # matching
            # Create matching pairs of problems and answers
            num_pairs = 4
            operations = random.sample(['+', '-', '×', '÷'], 2) * 2
            pairs = []
            
            for op in operations:
                a, b = random.randint(1, 10), random.randint(1, 10)
                if op == '+':
                    answer = a + b
                elif op == '-':
                    answer = a - b
                elif op == '×':
                    answer = a * b
                else:  # ÷
                    a = b * random.randint(1, 5)
                    answer = a // b
                pairs.append((f"{a} {op} {b}", str(answer)))
            
            random.shuffle(pairs)
            problems = [p[0] for p in pairs]
            answers = [p[1] for p in pairs]
            random.shuffle(answers)
            
            problem = "Match each problem with its answer:\n"
            problem += "\n".join([f"{i+1}. {p}" for i, p in enumerate(problems)])
            problem += "\n\nAnswers:\n"
            problem += "\n".join([f"{chr(65+i)}. {a}" for i, a in enumerate(answers)])
            
            # Create the matching (problem index -> answer letter)
            correct_matches = []
            for i, p in enumerate(problems):
                correct_answer = next(a for a in pairs if a[0] == p)[1]
                correct_letter = chr(65 + answers.index(correct_answer))
                correct_matches.append(f"{i+1} -> {correct_letter}")
            
            return problem, correct_matches
    
    def _generate_real_life_scenario(self, difficulty: str) -> Tuple[str, Union[int, str]]:
        """Generate real-life scenario problems."""
        scenarios = [
            self._generate_time_zone_problem,
            self._generate_height_change_problem,
            self._generate_game_scoring_problem
        ]
        return random.choice(scenarios)(difficulty)
    
    def _generate_time_zone_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate time zone conversion problems."""
        cities = [
            ('New York', -5), ('London', 0), ('Tokyo', 9), 
            ('Sydney', 10), ('Los Angeles', -8), ('Mumbai', 5.5)
        ]
        city1, tz1 = random.choice(cities)
        city2, tz2 = random.choice([c for c in cities if c[0] != city1])
        
        if difficulty == 'easy':
            hour = random.randint(1, 12)
            ampm = random.choice(['AM', 'PM'])
            time_diff = abs(tz2 - tz1)
            
            if tz2 > tz1:
                new_hour = (hour + time_diff) % 12 or 12
                if hour + time_diff >= 12 and ampm == 'AM':
                    new_ampm = 'PM'
                elif hour + time_diff >= 12 and ampm == 'PM':
                    new_ampm = 'AM'
                else:
                    new_ampm = ampm
                problem = f"If it's {hour} {ampm} in {city1}, what time is it in {city2}?"
                return problem, f"{new_hour} {new_ampm}"
            else:
                new_hour = (hour - time_diff) % 12 or 12
                if hour - time_diff <= 0 and ampm == 'AM':
                    new_ampm = 'PM'
                elif hour - time_diff <= 0 and ampm == 'PM':
                    new_ampm = 'AM'
                else:
                    new_ampm = ampm
                problem = f"If it's {hour} {ampm} in {city1}, what time is it in {city2}?"
                return problem, f"{new_hour} {new_ampm}"
                
        elif difficulty == 'medium':
            hour = random.randint(1, 12)
            minute = random.choice([0, 15, 30, 45])
            ampm = random.choice(['AM', 'PM'])
            time_diff = abs(tz2 - tz1)
            
            if tz2 > tz1:
                new_hour = (hour + time_diff) % 12 or 12
                if hour + time_diff >= 12 and ampm == 'AM':
                    new_ampm = 'PM'
                elif hour + time_diff >= 12 and ampm == 'PM':
                    new_ampm = 'AM'
                else:
                    new_ampm = ampm
                problem = f"If it's {hour}:{minute:02d} {ampm} in {city1}, what time is it in {city2}?"
                return problem, f"{new_hour}:{minute:02d} {new_ampm}"
            else:
                new_hour = (hour - time_diff) % 12 or 12
                if hour - time_diff <= 0 and ampm == 'AM':
                    new_ampm = 'PM'
                elif hour - time_diff <= 0 and ampm == 'PM':
                    new_ampm = 'AM'
                else:
                    new_ampm = ampm
                problem = f"If it's {hour}:{minute:02d} {ampm} in {city1}, what time is it in {city2}?"
                return problem, f"{new_hour}:{minute:02d} {new_ampm}"
                
        else:  # hard
            # Flight duration across time zones
            city1, tz1 = random.choice(cities)
            city2, tz2 = random.choice([c for c in cities if c[0] != city1])
            depart_hour = random.randint(1, 12)
            depart_ampm = random.choice(['AM', 'PM'])
            flight_hours = random.randint(1, 15)
            flight_mins = random.choice([0, 15, 30, 45])
            
            # Calculate arrival time
            if depart_ampm == 'PM' and depart_hour != 12:
                depart_hour_24 = depart_hour + 12
            elif depart_ampm == 'AM' and depart_hour == 12:
                depart_hour_24 = 0
            else:
                depart_hour_24 = depart_hour
                
            arrive_hour_24 = (depart_hour_24 + flight_hours) % 24
            arrive_minute = flight_mins  # Assuming no minutes in departure time for simplicity
            
            # Convert to 12-hour format
            if arrive_hour_24 == 0:
                arrive_hour = 12
                arrive_ampm = 'AM'
            elif arrive_hour_24 < 12:
                arrive_hour = arrive_hour_24
                arrive_ampm = 'AM'
            elif arrive_hour_24 == 12:
                arrive_hour = 12
                arrive_ampm = 'PM'
            else:
                arrive_hour = arrive_hour_24 - 12
                arrive_ampm = 'PM'
            
            # Format time difference for display
            time_diff_hours = abs(tz2 - tz1)
            time_diff_minutes = int((time_diff_hours % 1) * 60)
            time_diff_str = f"{int(time_diff_hours)} hours"
            if time_diff_minutes > 0:
                time_diff_str = f"{int(time_diff_hours)} hours and {time_diff_minutes} minutes"
                
            direction = "ahead of" if tz2 > tz1 else "behind"
            
            problem = f"A flight leaves {city1} (UTC{tz1:+g}) at {depart_hour}:00 {depart_ampm} and takes {flight_hours} hours and {flight_mins} minutes "
            problem += f"to reach {city2} (UTC{tz2:+g}). {city2} is {time_diff_str} {direction} {city1}. What time is it in {city2} when the flight arrives?"
            
            # Adjust for time zone difference
            time_diff = tz2 - tz1
            arrive_hour_24_tz = (arrive_hour_24 + int(time_diff)) % 24
            
            if arrive_hour_24_tz == 0:
                final_hour = 12
                final_ampm = 'AM'
            elif arrive_hour_24_tz < 12:
                final_hour = arrive_hour_24_tz
                final_ampm = 'AM'
            elif arrive_hour_24_tz == 12:
                final_hour = 12
                final_ampm = 'PM'
            else:
                final_hour = arrive_hour_24_tz - 12
                final_ampm = 'PM'
            
            return problem, f"{final_hour}:{arrive_minute:02d} {final_ampm}"
    
    def _generate_height_change_problem(self, difficulty: str) -> Tuple[str, str]:
        """Generate height change problems."""
        people = [
            'Alex', 'Taylor', 'Jordan', 'Casey', 'Riley',
            'Jamie', 'Morgan', 'Quinn', 'Avery', 'Peyton'
        ]
        person1, person2 = random.sample(people, 2)
        
        if difficulty == 'easy':
            height1 = random.randint(140, 180)
            diff = random.randint(5, 20)
            height2 = height1 + diff
            problem = f"{person1} is {height1} cm tall. {person2} is {diff} cm taller than {person1}. How tall is {person2}?"
            return problem, f"{height2} cm"
            
        elif difficulty == 'medium':
            height1 = random.randint(140, 180)
            height2 = random.randint(140, 180)
            diff = abs(height1 - height2)
            taller = person1 if height1 > height2 else person2
            shorter = person2 if taller == person1 else person1
            
            problem = f"{person1} is {height1} cm tall. {person2} is {height2} cm tall. "
            problem += f"How much taller is {taller} than {shorter}?"
            return problem, f"{diff} cm"
            
        else:  # hard
            heights = {p: random.randint(140, 190) for p in people[:4]}
            sorted_people = sorted(heights.items(), key=lambda x: x[1], reverse=True)
            
            problem = "Arrange these people from tallest to shortest: "
            problem += ", ".join([f"{p} ({h} cm)" for p, h in heights.items()]) + "."
            
            correct_order = ", ".join([f"{p[0]} ({p[1]} cm)" for p in sorted_people])
            return problem, correct_order
    
    def _generate_game_scoring_problem(self, difficulty: str) -> Tuple[str, Union[int, str]]:
        """Generate game scoring problems."""
        games = ['basketball', 'soccer', 'hockey', 'volleyball', 'tennis']
        game = random.choice(games)
        
        if difficulty == 'easy':
            team1 = random.randint(50, 100)
            team2 = random.randint(50, 100)
            winner = "Team A" if team1 > team2 else "Team B" if team2 > team1 else "It's a tie"
            problem = f"In a {game} game, Team A scored {team1} points and Team B scored {team2} points. Who won?"
            return problem, winner
            
        elif difficulty == 'medium':
            scores = [random.randint(0, 30) for _ in range(4)]
            total = sum(scores)
            average = total / len(scores)
            problem = f"In a {game} tournament, a player scored {', '.join(map(str, scores))} points in 4 games. "
            problem += f"What was their average score per game?"
            return problem, f"{average:.1f} points"
            
        else:  # hard
            quarters = [random.randint(10, 30) for _ in range(4)]
            total = sum(quarters)
            max_quarter = max(quarters)
            min_quarter = min(quarters)
            difference = max_quarter - min_quarter
            
            problem = f"A {game} team scored {', '.join(map(str, quarters))} points in 4 quarters. "
            problem += f"What was the difference between their highest and lowest scoring quarters?"
            return problem, f"{difference} points"
