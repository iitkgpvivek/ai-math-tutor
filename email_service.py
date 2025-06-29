import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv
from datetime import datetime
import schedule
import time
from typing import List, Optional, Dict, Any
import json
from pathlib import Path

# Load environment variables
load_dotenv()

class EmailService:
    def __init__(self):
        """Initialize email service with configuration from environment variables."""
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.from_email = os.getenv('SMTP_USERNAME')
        self.student_email = os.getenv('STUDENT_EMAIL')
        self.parent_email = os.getenv('PARENT_EMAIL')
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
        
    def send_email(self, to_email: str, subject: str, body: str, 
                  pdf_path: Optional[str] = None, is_html: bool = True) -> bool:
        """
        Send an email with optional PDF attachment.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body content
            pdf_path: Optional path to PDF file to attach
            is_html: Whether the body is HTML content
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        if not all([self.smtp_username, self.smtp_password]):
            print("Error: SMTP credentials not configured")
            return False
            
        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
        
        # Add PDF attachment if provided
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(pdf_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
            msg.attach(part)
        
        # Send email
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            print(f"Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_daily_problems(self) -> bool:
        """Generate and send daily math problems to the student."""
        from grade7_problems import Grade7ProblemGenerator
        
        try:
            # Generate problems - 5 fraction/decimal and 5 rational number problems
            generator = Grade7ProblemGenerator()
            problems = []
            for _ in range(5):
                problems.append(generator.generate_fraction_decimal_problem('medium'))
                problems.append(generator.generate_rational_number_problem('medium'))
            
            # Save problems to track answers
            problem_set = {
                'date': datetime.now().isoformat(),
                'problems': problems
            }
            
            # Save to file
            problem_set_path = self.data_dir / f"problems_{datetime.now().strftime('%Y%m%d')}.json"
            with open(problem_set_path, 'w') as f:
                json.dump(problem_set, f, indent=2)
            
            # Create PDF
            pdf_path = self._create_problems_pdf(problems)
            
            # Prepare email
            subject = f"📚 Your Daily Math Practice - {datetime.now().strftime('%A, %B %d')}"
            body = self._create_email_body(problems)
            
            # Send to student and parent
            student_sent = self.send_email(self.student_email, subject, body, pdf_path)
            parent_sent = self.send_email(self.parent_email, f"Copy: {subject}", body, pdf_path)
            
            return student_sent and parent_sent
        
        except Exception as e:
            print(f"Error generating daily problems: {e}")
            return False
        
        # Save to file
        problem_set_path = self.data_dir / f"problems_{datetime.now().strftime('%Y%m%d')}.json"
        with open(problem_set_path, 'w') as f:
            json.dump(problem_set, f, indent=2)
        
        # Create PDF
        pdf_path = self._create_problems_pdf(problems)
        
        # Prepare email
        subject = f"📚 Your Daily Math Practice - {datetime.now().strftime('%A, %B %d')}"
        body = self._create_email_body(problems)
        
        # Send to student and parent
        student_sent = self.send_email(self.student_email, subject, body, pdf_path)
        parent_sent = self.send_email(self.parent_email, f"Copy: {subject}", body, pdf_path)
        
        return student_sent and parent_sent
    
    def _create_problems_pdf(self, problems: List[Dict[str, Any]]) -> str:
        """Create a PDF with the daily math problems."""
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        
        # Create PDF
        pdf_path = self.data_dir / f"problems_{datetime.now().strftime('%Y%m%d')}.pdf"
        doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Custom styles
        styles.add(ParagraphStyle(
            name='Problem',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12,
        ))
        
        # Build content
        content = []
        content.append(Paragraph("Daily Math Practice", styles['Title']))
        content.append(Paragraph(f"Date: {datetime.now().strftime('%A, %B %d, %Y')}", styles['Normal']))
        content.append(Spacer(1, 20))
        
        # Add each problem
        for i, problem in enumerate(problems, 1):
            content.append(Paragraph(f"<b>Problem {i}:</b> {problem['question']}", styles['Problem']))
            content.append(Spacer(1, 10))
        
        # Add instructions
        content.append(Spacer(1, 20))
        content.append(Paragraph("<b>Instructions:</b>", styles['Normal']))
        content.append(Paragraph("1. Solve each problem and write down your answers.", styles['Normal']))
        content.append(Paragraph("2. Reply to this email with your answers.", styles['Normal']))
        content.append(Paragraph("3. Type 'hint' for a hint on any problem.", styles['Normal']))
        
        # Generate PDF
        doc.build(content)
        return str(pdf_path)
    
    def _create_email_body(self, problems: List[Dict[str, Any]]) -> str:
        """Create HTML email body with problems."""
        problems_html = ""
        for i, problem in enumerate(problems, 1):
            problems_html += f"""
            <div style="margin-bottom: 20px; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                <h3 style="margin-top: 0;">Problem {i}:</h3>
                <p style="font-size: 16px; margin-bottom: 10px;">{problem['question']}</p>
                <p style="font-size: 14px; color: #6c757d; margin: 0;">
                    <em>Hint: {problem.get('hint', 'No hint available')}</em>
                </p>
            </div>
            """
        
        return f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ text-align: center; margin-bottom: 20px; }}
                    .footer {{ margin-top: 30px; font-size: 12px; color: #6c757d; text-align: center; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1 style="color: #4a6baf;">📚 Daily Math Practice</h1>
                        <p>Hello! Here are your math problems for today.</p>
                    </div>
                    
                    {problems_html}
                    
                    <div class="footer">
                        <p>Reply to this email with your answers. Type 'hint' for an extra hint on any problem.</p>
                        <p>© {datetime.now().year} Math Tutor. All rights reserved.</p>
                    </div>
                </div>
            </body>
        </html>
        """
    
    def start_daily_schedule(self):
        """Start the scheduler to send daily emails."""
        print("Starting email scheduler...")
        
        # Schedule daily email (e.g., 4 PM)
        schedule.every().day.at("16:00").do(self.send_daily_problems)
        
        # Send immediately for testing
        self.send_daily_problems()
        
        # Keep the script running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    email_service = EmailService()
    email_service.start_daily_schedule()
