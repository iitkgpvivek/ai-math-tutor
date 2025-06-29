import random
from typing import List, Tuple
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

class FractionProblemGenerator:
    def __init__(self):
        self.operators = ['+', '-', '×', '÷']
        self.fraction_operations = ['+', '-', '×', '÷']
        self.decimal_operations = ['+', '-', '×', '÷']
        self.comparison_operators = ['<', '>', '=']
    
    def generate_fraction(self, max_denominator=12) -> Tuple[int, int]:
        """Generate a simple fraction."""
        denominator = random.randint(2, max_denominator)
        numerator = random.randint(1, denominator - 1)
        return numerator, denominator
    
    def generate_mixed_number(self, max_whole=5, max_denominator=12) -> Tuple[int, int, int]:
        """Generate a mixed number."""
        whole = random.randint(1, max_whole)
        numerator, denominator = self.generate_fraction(max_denominator)
        return whole, numerator, denominator
    
    def format_fraction(self, numerator: int, denominator: int, use_math: bool = False) -> str:
        """Format a fraction, with optional math formatting."""
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator
        return f"{numerator}/{denominator}"
    
    def format_mixed_number(self, whole: int, numerator: int, denominator: int, use_math: bool = False) -> str:
        """Format a mixed number, with optional math formatting."""
        if whole == 0:
            return self.format_fraction(numerator, denominator, use_math)
        return f"{whole} {numerator}/{denominator}"
    
    def generate_decimal(self, max_whole=10, max_decimal=2) -> float:
        """Generate a random decimal number."""
        whole = random.randint(0, max_whole)
        decimal = random.randint(1, 10**max_decimal - 1)
        return float(f"{whole}.{decimal:0{max_decimal}}")
    
    def simplify_fraction(self, numerator: int, denominator: int) -> Tuple[int, int]:
        """Simplify a fraction to its lowest terms."""
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a
        common_divisor = gcd(numerator, denominator)
        return numerator // common_divisor, denominator // common_divisor
    
    def generate_equivalent_fractions(self, numerator: int, denominator: int, count: int = 4) -> List[Tuple[int, int]]:
        """Generate equivalent fractions."""
        multiplier = random.randint(2, 5)
        return [(numerator * i, denominator * i) for i in range(1, count + 1)]
    
    def generate_problem(self) -> Tuple[str, str]:
        """Generate a single math problem with answer."""
        problem_types = [
            'simple_fraction', 'mixed_number', 'fraction_operation',
            'decimal_operation', 'fraction_to_decimal', 'decimal_to_fraction',
            'compare_fractions', 'word_problem_fraction', 'word_problem_decimal',
            'equivalent_fractions', 'fraction_of_quantity', 'decimal_ordering'
        ]
        problem_type = random.choice(problem_types)
        
        if problem_type == 'simple_fraction':
            # Simple fraction simplification
            num, den = self.generate_fraction()
            simplified_num, simplified_den = self.simplify_fraction(num, den)
            problem = f"Simplify the fraction: {num}/{den}"
            if simplified_den == 1:
                answer = f"{simplified_num}"
            else:
                answer = f"{simplified_num}/{simplified_den}"
            
        elif problem_type == 'mixed_number':
            # Mixed number to improper fraction
            whole, num, den = self.generate_mixed_number()
            problem = f"Convert to improper fraction: {whole} {num}/{den}"
            imp_num = whole * den + num
            answer = f"{imp_num}/{den}"
            
        elif problem_type == 'fraction_operation':
            # Operation with two fractions
            op = random.choice(self.fraction_operations)
            if op in ['+', '-']:
                # For addition/subtraction, use common denominator
                den1 = random.randint(2, 12)
                num1 = random.randint(1, den1 - 1)
                den2 = random.randint(2, 12)
                num2 = random.randint(1, den2 - 1)
                lcm = den1 * den2 // self.gcd(den1, den2)
                if op == '+':
                    res_num = num1 * (lcm // den1) + num2 * (lcm // den2)
                else:
                    res_num = num1 * (lcm // den1) - num2 * (lcm // den2)
                res_den = lcm
            else:  # × or ÷
                num1, den1 = self.generate_fraction()
                num2, den2 = self.generate_fraction()
                if op == '×':
                    res_num = num1 * num2
                    res_den = den1 * den2
                else:  # ÷
                    res_num = num1 * den2
                    res_den = den1 * num2
            
            # Simplify result
            res_num, res_den = self.simplify_fraction(res_num, res_den)
            problem = f"Calculate: {num1}/{den1} {op} {num2}/{den2}"
            if res_den == 1:
                answer = f"{res_num}"
            else:
                answer = f"{res_num}/{res_den}"
                
        elif problem_type == 'decimal_operation':
            # Operation with two decimals
            op = random.choice(self.decimal_operations)
            dec1 = self.generate_decimal()
            dec2 = self.generate_decimal()
            
            if op == '+':
                result = round(dec1 + dec2, 2)
            elif op == '-':
                result = round(dec1 - dec2, 2)
            elif op == '×':
                result = round(dec1 * dec2, 2)
            else:  # ÷
                result = round(dec1 / dec2, 2) if dec2 != 0 else "Undefined"
                
            problem = f"Calculate: {dec1} {op} {dec2}"
            answer = str(result) if result != "Undefined" else result
            
        elif problem_type == 'fraction_to_decimal':
            # Convert fraction to decimal
            num, den = self.generate_fraction()
            decimal = round(num / den, 3)
            problem = f"Convert to decimal: {num}/{den}"
            answer = str(decimal).rstrip('0').rstrip('.')
            
        elif problem_type == 'decimal_to_fraction':
            # Convert terminating decimal to fraction
            decimal = self.generate_decimal(max_whole=10, max_decimal=2)
            denominator = 10 ** len(str(decimal).split('.')[1])
            numerator = int(decimal * denominator)
            problem = f"Convert to fraction: {decimal}"
            answer = f"{numerator}/{denominator}"
            
        elif problem_type == 'compare_fractions':
            # Compare two fractions
            num1, den1 = self.generate_fraction()
            num2, den2 = self.generate_fraction()
            value1 = num1 / den1
            value2 = num2 / den2
            
            if abs(value1 - value2) < 0.0001:  # Account for floating point precision
                op = '='
            elif value1 < value2:
                op = '<'
            else:
                op = '>'
                
            problem = f"Compare: {num1}/{den1} _ {num2}/{den2} (use <, >, or =)"
            answer = op
            
        elif problem_type == 'equivalent_fractions':
            # Find equivalent fractions
            num, den = self.generate_fraction()
            equiv_fractions = self.generate_equivalent_fractions(num, den, count=3)
            equiv_fractions_str = ', '.join(f"{n}/{d}" for n, d in equiv_fractions[1:])
            problem = f"Find three fractions equivalent to {num}/{den}. Example: {equiv_fractions_str}, ..."
            answer = ", ".join(f"{n}/{d}" for n, d in equiv_fractions)
            
        elif problem_type == 'fraction_of_quantity':
            # Fraction of a quantity word problem
            quantity = random.randint(10, 100)
            num, den = self.generate_fraction()
            result = (num / den) * quantity
            
            problem = f"Find {num}/{den} of {quantity}"
            answer = str(round(result, 2)).rstrip('0').rstrip('.')
            
        elif problem_type == 'decimal_ordering':
            # Ordering decimals
            decimals = sorted([round(random.uniform(0.1, 9.9), 2) for _ in range(3)])
            if random.choice([True, False]):
                problem = f"Arrange in ascending order: {', '.join(str(d) for d in decimals)}"
                answer = ", ".join(sorted([str(d) for d in decimals], key=float))
            else:
                problem = f"Arrange in descending order: {', '.join(str(d) for d in decimals)}"
                answer = ", ".join(sorted([str(d) for d in decimals], key=float, reverse=True))
            
        # Add word problems for variety
        if problem_type == 'word_problem_fraction':
            problem_types = [
                (f"A recipe needs {random.randint(2, 5)}/{random.randint(2, 8)} cups of sugar. "
                 f"If you want to make {random.randint(2, 4)} batches, how much sugar do you need?"),
                (f"A pizza is cut into {random.randint(4, 12)} equal slices. You eat {random.randint(1, 3)} slices. "
                 f"What fraction of the pizza did you eat?"),
                (f"You have {random.randint(2, 5)}/{random.randint(6, 12)} of a cake. "
                 f"Your friend gives you {random.randint(1, 4)}/{random.randint(6, 12)} more. "
                 "How much cake do you have now?")
            ]
            problem = random.choice(problem_types)
            # Note: For a complete solution, we'd need to parse and solve these problems
            answer = "[Word problem solution]"
            
        elif problem_type == 'word_problem_decimal':
            price = round(random.uniform(1, 10), 2)
            quantity = random.randint(2, 10)
            total = round(price * quantity, 2)
            
            problem_types = [
                f"If one book costs ${price}, how much do {quantity} books cost?",
                f"A box contains {quantity} identical items. The total weight is {total} kg. What is the weight of each item?",
                f"You walk {total} km in {quantity} hours. What is your average speed in km per hour?"
            ]
            problem = random.choice(problem_types)
            # Note: For a complete solution, we'd need to parse and solve these problems
            answer = f"{price}" if quantity == 1 else f"{total}"
        
        return problem, answer

def generate_worksheet():
    """Generate a simple math worksheet with 10 problems."""
    # Set up the PDF document
    output_dir = 'math_worksheets'
    os.makedirs(output_dir, exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')
    filename = os.path.join(output_dir, f'final_worksheet_{today}.pdf')
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=72
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center aligned
    )
    
    problem_style = ParagraphStyle(
        'Problem',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        spaceAfter=20,
        leftIndent=20
    )
    
    answer_style = ParagraphStyle(
        'Answer',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        spaceAfter=10,
        leftIndent=40,
        textColor=colors.blue
    )
    
    # Generate content
    content = []
    
    # Add title
    content.append(Paragraph("Daily Math Practice", title_style))
    content.append(Paragraph(f"Date: {today}", styles['Normal']))
    content.append(Spacer(1, 30))
    
    # Generate problems
    generator = FractionProblemGenerator()
    problems = [generator.generate_problem() for _ in range(10)]
    
    # Add problems to content
    for i, (problem, _) in enumerate(problems, 1):
        content.append(Paragraph(f"{i}. {problem}", problem_style))
        content.append(Spacer(1, 10))
        
        # Add space for working out
        if i % 2 == 0:  # Add more space after every other problem
            content.append(Spacer(1, 30))
        else:
            content.append(Spacer(1, 10))
        
        # Add page break after 5 problems
        if i == 5:
            content.append(PageBreak())
            content.append(Paragraph("Daily Math Practice (continued)", title_style))
            content.append(Spacer(1, 30))
    
    # Add answer key
    content.append(PageBreak())
    content.append(Paragraph("Answer Key", title_style))
    content.append(Spacer(1, 20))
    
    # Organize answers in two columns
    answers1 = []
    answers2 = []
    
    for i, (_, answer) in enumerate(problems):
        # Format the answer with math notation
        answer_item = Paragraph(f"{i + 1}. {answer}", answer_style)
        
        if i % 2 == 0:
            answers1.append([answer_item])
        else:
            answers2.append([answer_item])
    
    # Create a table with two columns for answers
    max_rows = max(len(answers1), len(answers2))
    answer_table_data = []
    
    for i in range(max_rows):
        row = []
        # Add first column answer if it exists
        if i < len(answers1):
            row.append(answers1[i][0])
        else:
            row.append('')
            
        # Add second column answer if it exists
        if i < len(answers2):
            row.append(answers2[i][0])
        else:
            row.append('')
            
        answer_table_data.append(row)
    
    # Create the table with proper column widths
    col_width = (doc.width - 2*inch) / 2  # Two columns with margins
    answer_table = Table(
        answer_table_data, 
        colWidths=[col_width, col_width], 
        rowHeights=[None] * len(answer_table_data)  # Auto height for rows
    )
    
    # Style the answer table
    answer_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey)
    ]))
    
    content.append(answer_table)
    
    # Generate the PDF
    doc.build(content)
    print(f"Worksheet generated: {os.path.abspath(filename)}")

if __name__ == "__main__":
    generate_worksheet()
