import random
from typing import List, Tuple, Union
import os
import tempfile
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

class MathRenderer:
    """Helper class to render math expressions to images."""
    
    @staticmethod
    def render_math(expression: str, fontsize: int = 14) -> Image:
        """Render a math expression to an image."""
        # Create a figure with minimal padding
        fig = plt.figure(figsize=(5, 0.5))
        fig.patch.set_alpha(0.0)  # Transparent background
        
        # Add text with mathtext
        plt.text(0.5, 0.5, f'${expression}$', 
                fontsize=fontsize, 
                ha='center', 
                va='center',
                color='black')
        
        # Remove axes and margins
        plt.axis('off')
        plt.margins(0)
        
        # Save to a buffer
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, dpi=300, transparent=True)
        plt.close(fig)
        buf.seek(0)
        
        # Create and return an Image flowable
        return Image(buf, width=100, height=30)

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
    
    def format_fraction(self, numerator: int, denominator: int) -> str:
        """Format a fraction for display."""
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator
        return f"\\frac{{{numerator}}}{{{denominator}}}"
    
    def format_mixed_number(self, whole: int, numerator: int, denominator: int) -> str:
        """Format a mixed number for display."""
        if whole == 0:
            return self.format_fraction(numerator, denominator)
        return f"{whole}\\frac{{{numerator}}}{{{denominator}}}"
    
    def generate_problem(self) -> Tuple[str, str, str]:
        """Generate a single fraction problem with answer.
        Returns: (problem_text, problem_math, answer_math)
        """
        problem_type = random.choice(['simple', 'mixed', 'operation'])
        
        if problem_type == 'simple':
            # Simple fraction problem
            num, den = self.generate_fraction()
            problem_text = f"Simplify the fraction: {num}/{den}"
            problem_math = f"Simplify the fraction: {self.format_fraction(num, den)}"
            answer_math = self.format_fraction(num, den)
            return problem_text, problem_math, answer_math
            
        elif problem_type == 'mixed':
            # Mixed number problem
            whole, num, den = self.generate_mixed_number()
            problem_text = f"Convert to improper fraction: {whole} {num}/{den}"
            problem_math = f"Convert to improper fraction: {self.format_mixed_number(whole, num, den)}"
            imp_num = whole * den + num
            answer_math = self.format_fraction(imp_num, den)
            return problem_text, problem_math, answer_math
            
        else:  # operation
            # Fraction operation problem
            op = random.choice(self.operators)
            if random.random() < 0.5:
                # Two simple fractions
                num1, den1 = self.generate_fraction()
                num2, den2 = self.generate_fraction()
                frac1 = f"{num1}/{den1}"
                frac2 = f"{num2}/{den2}"
                problem_text = f"Calculate: {frac1} {op} {frac2}"
                problem_math = f"Calculate: {self.format_fraction(num1, den1)} {op} {self.format_fraction(num2, den2)}"
                
                # Simple answer (for demo, not actually calculated)
                answer_math = self.format_fraction(num1 + num2, den1)
                return problem_text, problem_math, answer_math
            else:
                # Mixed number operation
                whole1, num1, den1 = self.generate_mixed_number()
                whole2, num2, den2 = self.generate_mixed_number()
                mixed1 = f"{whole1} {num1}/{den1}"
                mixed2 = f"{whole2} {num2}/{den2}"
                problem_text = f"Calculate: {mixed1} {op} {mixed2}"
                problem_math = f"Calculate: {self.format_mixed_number(whole1, num1, den1)} {op} {self.format_mixed_number(whole2, num2, den2)}"
                
                # Simple answer (for demo, not actually calculated)
                answer_math = self.format_fraction(num1 + num2, den1)
                return problem_text, problem_math, answer_math

def generate_worksheet():
    """Generate a simple math worksheet with 10 problems."""
    # Set up the PDF document
    output_dir = 'math_worksheets'
    os.makedirs(output_dir, exist_ok=True)
    today = datetime.now().strftime('%Y-%m-%d')
    filename = os.path.join(output_dir, f'simple_worksheet_{today}.pdf')
    
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
    for i, (problem_text, problem_math, answer_math) in enumerate(problems, 1):
        # Add problem number and text
        content.append(Paragraph(f"{i}.", problem_style))
        
        # Add the problem with rendered math
        try:
            math_img = MathRenderer.render_math(problem_math)
            content.append(math_img)
        except Exception as e:
            # Fallback to text if math rendering fails
            content.append(Paragraph(problem_text, problem_style))
        
        content.append(Spacer(1, 20))
    
    # Add answer key
    content.append(PageBreak())
    content.append(Paragraph("Answer Key", title_style))
    content.append(Spacer(1, 20))
    
    for i, (_, _, answer_math) in enumerate(problems, 1):
        # Add answer number
        content.append(Paragraph(f"{i}.", answer_style))
        
        # Add the answer with rendered math
        try:
            math_img = MathRenderer.render_math(answer_math, fontsize=16)
            content.append(math_img)
        except Exception as e:
            # Fallback to text if math rendering fails
            clean_answer = answer_math.replace('\\frac{', '').replace('}{', '/').replace('}', '')
            content.append(Paragraph(clean_answer, answer_style))
    
    # Build the PDF
    doc.build(content)
    print(f"Worksheet generated: {os.path.abspath(filename)}")

if __name__ == "__main__":
    generate_worksheet()
