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
    
    def generate_problem(self) -> Tuple[str, str]:
        """Generate a single fraction problem with answer."""
        problem_type = random.choice(['simple', 'mixed', 'operation'])
        
        if problem_type == 'simple':
            # Simple fraction problem
            num, den = self.generate_fraction()
            problem = f"Simplify the fraction: {self.format_fraction(num, den, use_math=False)}"
            answer = self.format_fraction(num, den, use_math=True)
            
        elif problem_type == 'mixed':
            # Mixed number problem
            whole, num, den = self.generate_mixed_number()
            problem = f"Convert to improper fraction: {self.format_mixed_number(whole, num, den, use_math=False)}"
            imp_num = whole * den + num
            answer = self.format_fraction(imp_num, den, use_math=True)
            
        else:  # operation
            # Fraction operation problem
            op = random.choice(self.operators)
            if random.random() < 0.5:
                # Two simple fractions
                num1, den1 = self.generate_fraction()
                num2, den2 = self.generate_fraction()
                frac1 = self.format_fraction(num1, den1, use_math=False)
                frac2 = self.format_fraction(num2, den2, use_math=False)
                problem = f"Calculate: {frac1} {op} {frac2}"
                
                # Simple answer (for demo, not actually calculated)
                answer = self.format_fraction(num1 + num2, den1, use_math=True)
            else:
                # Mixed number operation
                whole1, num1, den1 = self.generate_mixed_number()
                whole2, num2, den2 = self.generate_mixed_number()
                mixed1 = self.format_mixed_number(whole1, num1, den1, use_math=False)
                mixed2 = self.format_mixed_number(whole2, num2, den2, use_math=False)
                problem = f"Calculate: {mixed1} {op} {mixed2}"
                
                # Simple answer (for demo, not actually calculated)
                answer = self.format_fraction(num1 + num2, den1, use_math=True)
        
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
