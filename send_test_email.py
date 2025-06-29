import os
from email_service import EmailService

# Initialize email service
email_service = EmailService()

# Send test email immediately
print("Sending test email...")
success = email_service.send_daily_problems()

if success:
    print("Test email sent successfully!")
else:
    print("Failed to send test email. Check the logs for errors.")
