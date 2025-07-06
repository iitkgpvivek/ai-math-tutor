import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

# Ensure the worksheets directory exists
os.makedirs('worksheets', exist_ok=True)

def load_latest_worksheet():
    """Load the most recently generated worksheet."""
    if not os.path.exists('data'):
        print("No data directory found. Please generate a worksheet first.")
        return None
    
    try:
        files = [f for f in os.listdir('data') if f.endswith('.json')]
        if not files:
            print("No JSON worksheets found in the data directory.")
            return None
            
        # Get the most recent file
        latest_file = max(files, key=lambda x: os.path.getmtime(os.path.join('data', x)))
        with open(os.path.join('data', latest_file), 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading worksheet: {e}")
        return None

def create_pdf(worksheet, include_answers=False, output_path=None):
    """Create a PDF from the worksheet.
    
    Args:
        worksheet: Dictionary containing worksheet data
        include_answers: Whether to include answers in the PDF
        output_path: Custom output path for the PDF. If not provided, generates a default path.
    """
    if not worksheet:
        return
    
    # Set up the PDF document
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"worksheet_answers_{timestamp}.pdf" if include_answers else f"worksheet_questions_{timestamp}.pdf"
        output_path = os.path.join('worksheets', filename)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72, leftMargin=72,
        topMargin=72, bottomMargin=72
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Create custom styles only if they don't exist
    if 'Title' not in styles:
        styles.add(ParagraphStyle(
            name='Title',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER
        ))
    
    if 'Problem' not in styles:
        styles.add(ParagraphStyle(
            name='Problem',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            leading=16,
            alignment=TA_LEFT
        ))
    
    if 'Answer' not in styles:
        styles.add(ParagraphStyle(
            name='Answer',
            parent=styles['Italic'],
            fontSize=12,
            textColor=colors.darkgreen,
            spaceAfter=20,
            leading=16,
            alignment=TA_LEFT
        ))
    
    # Build the PDF content
    elements = []
    
    # Add title and metadata
    title = f"Grade 7 {worksheet.get('topic', 'Math')} Worksheet"
    elements.append(Paragraph(title, styles['Title']))
    elements.append(Spacer(1, 10))
    
    # Add difficulty and date
    difficulty = worksheet.get('difficulty', '').capitalize()
    date_str = worksheet.get('date', datetime.now().strftime("%Y-%m-%d"))
    
    elements.append(Paragraph(f"<b>Difficulty:</b> {difficulty}", styles['Normal']))
    elements.append(Paragraph(f"<b>Date:</b> {date_str}", styles['Normal']))
    
    # Add unit conversion reference
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<b>Unit Conversion Reference:</b>", styles['Normal']))
    elements.append(Paragraph("• Length: 1 m = 100 cm, 1 km = 1000 m", styles['Normal']))
    elements.append(Paragraph("• US Length: 1 yd = 3 ft, 1 ft = 12 in, 1 yd = 36 in", styles['Normal']))
    elements.append(Paragraph("• Volume: 1 L = 1000 mL, 1 gal = 3.785 L", styles['Normal']))
    elements.append(Paragraph("• Mass: 1 kg = 1000 g, 1 lb = 16 oz", styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Add problems
    for i, problem in enumerate(worksheet['problems'], 1):
        # Add problem number and text
        problem_text = f"<b>{i}.</b> {problem['problem']}"
        elements.append(Paragraph(problem_text, styles['Problem']))
        
        # Add answer if requested
        if include_answers:
            answer_text = f"<b>Answer:</b> {problem['answer']}"
            elements.append(Paragraph(answer_text, styles['Answer']))
        
        # Add some space between problems
        elements.append(Spacer(1, 10))
        
        # Add a page break after every 5 problems if not the last problem
        if i % 5 == 0 and i < len(worksheet['problems']):
            elements.append(PageBreak())
            # Add title on the new page
            elements.append(Paragraph(title + " (continued)", styles['Title']))
            elements.append(Spacer(1, 30))
    
    # Generate the PDF
    doc.build(elements)
    print(f"Generated {os.path.basename(output_path)}")

def main():
    # Load the latest worksheet
    worksheet = load_latest_worksheet()
    if not worksheet:
        print("No worksheet found. Please generate a worksheet first using generate_math_problems.py")
        return
    
    # Generate question and answer PDFs
    create_pdf(worksheet, include_answers=False)
    create_pdf(worksheet, include_answers=True)
    
    print("PDF generation complete! Check the 'worksheets' directory for your files.")

if __name__ == "__main__":
    main()
