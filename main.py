#!/usr/bin/env python3
"""
Math Tutor - Main Application

This is the entry point for the Math Tutor application.
It starts both the email scheduler and the web interface.
"""
import threading
import os
import signal
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def start_email_service():
    """Start the email service in a separate thread."""
    from email_service import EmailService
    print("Starting email service...")
    email_service = EmailService()
    email_service.start_daily_schedule()

def start_web_app():
    """Start the Flask web application."""
    from web.app import app
    print("Starting web application...")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    print("\nShutting down Math Tutor...")
    sys.exit(0)

if __name__ == "__main__":
    # Create necessary directories
    Path('data').mkdir(exist_ok=True)
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Start email service in a separate thread
    email_thread = threading.Thread(target=start_email_service, daemon=True)
    email_thread.start()
    
    # Start the web application in the main thread
    start_web_app()
