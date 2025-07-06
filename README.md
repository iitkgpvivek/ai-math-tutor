# 📚 Grade 7 Math Worksheet Generator

A local math worksheet generator that creates practice problems for 7th grade students, focusing on fractions and decimals. The application generates worksheets in JSON format and can convert them to PDF with separate question and answer sheets.

![Math Worksheet Demo](https://img.shields.io/badge/Status-Active-brightgreen) 
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue) 
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- **Local Generation**: All worksheets are generated and stored locally
- **Focused Content**: Special emphasis on fractions and decimals
- **Multiple Difficulty Levels**: Problems range from basic to challenging
- **Answer Keys**: Automatically generated with each worksheet
- **PDF Export**: Convert worksheets to printable PDF format
- **Problem Types**:
  - Fraction operations (+, -, ×, ÷)
  - Decimal operations
  - Word problems
  - Fraction-decimal conversions
  - Mixed numbers

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/grade7-math-worksheets.git
   cd grade7-math-worksheets
   ```

2. **Create and activate a virtual environment (recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
## 📝 Usage

### Generating Worksheets

1. **Generate a new worksheet**:
   ```bash
   python generate_math_problems.py
   ```
   This will create a JSON file in the `data` directory with 10 math problems.

2. **View the generated worksheet**:
   ```bash
   python view_worksheet.py
   ```
   This will display the most recently generated worksheet in the console.

### Converting to PDF

To convert the JSON worksheet to a PDF with separate question and answer sheets:

1. **Install the required dependencies**:
   ```bash
   pip install reportlab
   ```

2. **Run the PDF generator**:
   ```bash
   python generate_pdf.py
   ```
   This will create two PDF files in the `worksheets` directory:
   - `worksheet_questions.pdf` - Contains just the problems
   - `worksheet_answers.pdf` - Contains the problems with answers

## 📁 Project Structure

```
grade7-math-worksheets/
├── data/                   # Directory for JSON worksheets
├── worksheets/             # Directory for PDF worksheets
├── grade7_problems.py      # Core problem generation logic
├── generate_math_problems.py  # Script to generate new worksheets
├── view_worksheet.py       # View worksheet in console
├── generate_pdf.py         # Convert JSON to PDF
└── requirements.txt        # Python dependencies
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
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
