import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_smtp_connection():
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = os.getenv('SMTP_USERNAME')
        msg['To'] = os.getenv('PARENT_EMAIL')
        msg['Subject'] = 'SMTP Test Email'
        
        # Add message body
        body = 'This is a test email to verify SMTP settings.'
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to SMTP server
        with smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT'))) as server:
            server.starttls()
            print("Attempting to log in...")
            server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
            print("Login successful!")
            
            # Send email
            print("Sending test email...")
            server.send_message(msg)
            print(f"Test email sent to {os.getenv('PARENT_EMAIL')}")
            return True
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing SMTP connection...")
    if test_smtp_connection():
        print("SMTP test successful!")
    else:
        print("SMTP test failed. Please check your credentials and settings.")
