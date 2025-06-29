# 📚 AI Math Tutor

An intelligent math practice system designed to help students master mathematics through personalized learning paths, adaptive difficulty, and a wide variety of problem types. The application includes both a web interface and automated email delivery of daily problem sets.

![Math Practice Demo](https://img.shields.io/badge/Status-Active-brightgreen) 
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue) 
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- **Daily Problem Sets**: Automatically sends 10 math problems via email every day
- **Interactive Web Interface**: Practice problems directly in your browser
- **Adaptive Learning**: Adjusts difficulty based on performance
- **Comprehensive Coverage**: Covers Grade 7 math topics including:
  - Number System
  - Algebra
  - Geometry
  - Data Handling
- **Progress Tracking**: Monitors performance and identifies weak areas
- **Multiple Problem Types**:
  - Arithmetic operations
  - Word problems
  - Geometry problems
  - Data interpretation
  - And more!
- **Email Notifications**:
  - Daily problem sets
  - Reminders for unanswered problems
  - Hints and solutions

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Gmail account (for email functionality)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/iitkgpvivek/ai-math-tutor.git
   cd ai-math-tutor
   ```

2. **Run the setup script**:
   ```bash
   ./setup.sh
   ```
   This will:
   - Create a virtual environment
   - Install all dependencies
   - Create a `.env` file from the example
   - Create necessary directories

3. **Configure your email settings**:
   - Open the `.env` file
   - Update the email configuration with your Gmail credentials
   - For Gmail, you'll need to create an App Password: 
     1. Go to your Google Account settings
     2. Navigate to Security > 2-Step Verification > App passwords
     3. Generate a new app password and use it in the `.env` file

### Running the Application

1. **Start the application**:
   ```bash
   # Activate the virtual environment if not already active
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Start the application
   python main.py
   ```

2. **Access the web interface**:
   Open your browser and go to: http://localhost:5000

3. **Daily Emails**:
   - The application will automatically send daily problem sets at 4:00 PM
   - Students can reply to the email with their answers

## 📝 Project Structure

```
ai-math-tutor/
├── data/                   # Data storage for problems and user progress
├── web/                    # Web application files
│   ├── static/             # CSS, JS, and other static files
│   ├── templates/          # HTML templates
│   └── app.py              # Flask web application
├── email_service.py        # Email sending functionality
├── grade7_problems.py      # Problem generators
├── learning_tracker.py     # Progress tracking
├── problem_discovery.py    # Web search for new problems
├── requirements.txt        # Python dependencies
├── main.py                 # Main application entry point
├── setup.sh                # Setup script
├── .env.example            # Example environment variables
└── README.md               # This file
```

## 🔧 Configuration

Edit the `.env` file to configure:

```ini
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_specific_password

# Email Recipients
STUDENT_EMAIL=student@example.com
PARENT_EMAIL=parent@example.com

# Email Schedule (24-hour format)
DAILY_EMAIL_TIME=16:00  # Sends at 4:00 PM

# Security
SECRET_KEY=your_secret_key_here
SOLUTION_PDF_PASSWORD=parent_secret_code
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with ❤️ for students everywhere
- Special thanks to the open-source community for their invaluable contributions
- Inspired by the need for personalized math education

---

📧 **Contact**: [Your Email]  
🌐 **Website**: [Your Website]

---

📧 **Contact**: [Your Email]  
🌐 **Website**: [Your Website]
