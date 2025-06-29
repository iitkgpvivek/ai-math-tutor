import os
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus.flowables import KeepInFrame, Flowable
from reportlab.platypus.paragraph import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from grade7_problems import Grade7ProblemGenerator
from latex_renderer import latex_renderer
import random
import re
import os
from datetime import datetime
from pathlib import Path

# Register fonts that support mathematical symbols
try:
    # Try to register DejaVu Sans which has good Unicode support
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))
    DEFAULT_FONT = 'DejaVuSans'
except:
    try:
        # Fallback to Arial which is commonly available
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arial-Bold.ttf'))
        DEFAULT_FONT = 'Arial'
    except:
        # Final fallback to Helvetica which is a PDF standard font
        DEFAULT_FONT = 'Helvetica'

def create_paragraph_with_math(text, style):
    """Create a paragraph with embedded math expressions."""
    from reportlab.platypus import Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    
    # Process the text to find and render math expressions
    parts = latex_renderer.render_inline_math(text)
    
    # If no math was found, return a simple paragraph
    if len(parts) == 1 and isinstance(parts[0], str):
        return Paragraph(parts[0], style)
    
    # Create a table to hold the mixed content
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib import colors
    
    # Convert all parts to flowables
    flowables = []
    for part in parts:
        if isinstance(part, str):
            flowables.append(Paragraph(part, style))
        else:
            # It's an image flowable
            flowables.append(part)
    
    # Create a table with one row and multiple columns
    table = Table([flowables], colWidths=['*'] * len(flowables))
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    
    return table

# Simple math formatter for fractions and basic operations
class MathRenderer:
    @staticmethod
    def render_math(expr) -> str:
        """Convert math expressions to properly formatted strings."""
        if not isinstance(expr, str):
            # Convert non-string answers to string
            if isinstance(expr, float):
                # Format float to remove unnecessary decimal places
                if expr.is_integer():
                    return str(int(expr))
                return f"{expr:.2f}".rstrip('0').rstrip('.')
            return str(expr)
            
        # Remove any LaTeX formatting and replace with proper symbols
        expr = (expr.replace('\\times', '×')
                   .replace('\\div', '÷')
                   .replace('\\cdot', '·')
                   .replace('\\leq', '≤')
                   .replace('\\geq', '≥')
                   .replace('$', ''))  # Remove $ delimiters
        
        return expr
    
    @staticmethod
    def render_paragraph(text: str, style) -> Paragraph:
        """Render a paragraph with consistent formatting."""
        # Use a monospace font for better alignment of fractions
        style.fontName = 'Courier-Bold'
        return Paragraph(text, style)

# Create output directory with today's date
output_dir = Path('math_worksheets')
output_dir.mkdir(exist_ok=True)

def generate_worksheet(filename=None, num_problems=10):
    """Generate a PDF worksheet with math problems."""
    # Set up the PDF document
    if not filename:
        today = datetime.now().strftime('%Y-%m-%d')
        filename = output_dir / f'math_worksheet_{today}.pdf'
    else:
        filename = Path(filename)
    
    doc = SimpleDocTemplate(
        str(filename),
        pagesize=letter,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=72
    )
    
    # Register a nice font if available
    try:
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
        font_name = 'DejaVuSans'
    except:
        font_name = 'Helvetica'
    
    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontName=f'{DEFAULT_FONT}-Bold' if DEFAULT_FONT == 'DejaVuSans' else 'Helvetica-Bold',
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontName=f'{DEFAULT_FONT}-Bold' if DEFAULT_FONT == 'DejaVuSans' else 'Helvetica-Bold',
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=30
    )

    problem_style = ParagraphStyle(
        'Problem',
        parent=styles['Normal'],
        fontName=DEFAULT_FONT,
        fontSize=12,
        leading=16,
        spaceAfter=20
    )

    answer_style = ParagraphStyle(
        'Answer',
        parent=styles['Normal'],
        fontName=DEFAULT_FONT,
        fontSize=12,
        leading=16,
        spaceAfter=10
    )
    
    # Generate problems
    generator = Grade7ProblemGenerator()
    problems = []
    answers = []
    
    for i in range(num_problems // 2):
        # Fraction/decimal problem
        problem, answer = generator.generate_fraction_decimal_problem('hard')
        problems.append((f"{i*2 + 1}. {problem}", answer))
        
        # Rational number problem or percentage/ratio/discount problem
        if random.random() < 0.7:  # 70% chance of rational number problem
            problem, answer = generator.generate_rational_number_problem('hard')
        else:
            # 30% chance of percentage/ratio/discount problem
            problem_type = random.choice([
                generator._generate_percentage_problem,
                generator._generate_ratio_problem,
                generator._generate_discount_problem
            ])
            problem, answer = problem_type('hard')
            
        problems.append((f"{i*2 + 2}. {problem}", answer))
    
    # Build the PDF content
    content = []
    
    # Add title
    content.append(Paragraph("Daily Math Practice", title_style))
    content.append(Paragraph(f"Date: {datetime.now().strftime('%A, %B %d, %Y')}", 
                           subtitle_style))
    content.append(Spacer(1, 20))
    
    # Add problems with inline math rendering
    for i, (problem, answer) in enumerate(problems):
        problem_text = f"{i+1}. {problem}"
        
        # Create a paragraph with inline math
        problem_para = create_paragraph_with_math(problem_text, problem_style)
        
        # Create a table to hold the problem
        problem_table = Table([
            [problem_para]
        ], colWidths=[doc.width - 2*inch], rowHeights=[None])  # Auto height
        
        problem_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey)
        ]))
        
        content.append(problem_table)
        content.append(Spacer(1, 10))  # Add some space between problems
        
        # Add space for working out
        if i % 2 == 0:  # Add more space after every other problem
            content.append(Spacer(1, 30))
        else:
            content.append(Spacer(1, 20))
        
        # Add a page break after 4 problems (with space for working)
        if (i + 1) % 4 == 0 and (i + 1) < len(problems):
            content.append(PageBreak())
            content.append(Paragraph("Daily Math Practice (continued)", title_style))
            content.append(Spacer(1, 30))

    # Add answers on a new page with better formatting
    content.append(PageBreak())
    content.append(Paragraph("Answer Key", title_style))
    content.append(Spacer(1, 20))

    # Organize answers in two columns
    answers1 = []
    answers2 = []

    for i, (_, answer) in enumerate(problems):
        # Format the answer with inline math
        answer_text = f"{i + 1}. {answer}"
        answer_item = create_paragraph_with_math(answer_text, answer_style)

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
    
    # Add the answer table to content
    content.append(answer_table)
    
    # Generate the PDF
    doc.build(content)
    print(f"Generated worksheet: {filename}")
    return str(filename)

if __name__ == "__main__":
    # Generate a worksheet with 10 problems
    pdf_path = generate_worksheet(num_problems=10)
    print(f"Worksheet saved to: {os.path.abspath(pdf_path)}")
    print(f"You can open it with: open {os.path.abspath(pdf_path)}")
