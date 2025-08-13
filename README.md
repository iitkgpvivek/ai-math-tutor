# 🧮 AI Math Worksheet Generator

An AI-powered math worksheet generator for 7th grade students, using local LLM (Ollama) to create customized practice problems with detailed solutions. The tool supports multiple problem types and difficulty levels, with PDF export capabilities.

![Status](https://img.shields.io/badge/Status-Active-brightgreen) 
![Python](https://img.shields.io/badge/Python-3.8%2B-blue) 
![License](https://img.shields.io/badge/License-MIT-green)
![AI](https://img.shields.io/badge/AI-Powered-FFD700)

## ✨ Features

- **AI-Powered**: Uses local LLM (Ollama) for problem generation
- **Multiple Problem Types**:
  - Integer operations
  - Simple equations
  - Word problems
  - Real-life applications
- **Customizable Difficulty**: Easy, Intermediate, Hard
- **PDF Export**: Generate printable worksheets with solutions
- **Interactive CLI**: User-friendly interface

## 🚀 Quick Start

1. **Install Ollama** (if not already installed):
   ```bash
   # Follow instructions at https://ollama.ai/
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the generator**:
   ```bash
   python custom_worksheet_creator.py
   ```
## 📝 Usage

1. **Interactive Mode**:
   ```bash
   python custom_worksheet_creator.py
   ```
   - Follow the prompts to select topics and difficulty
   - Worksheets are saved in the `worksheets` directory

2. **Command Line Options**:
   ```bash
   python custom_worksheet_creator.py --topic integers --count 5 --difficulty medium
   ```

## 📁 Key Files

- `custom_worksheet_creator.py` - Main application
- `local_llm_integration.py` - LLM communication
- `problem_importer.py` - Problem management
- `generate_pdf.py` - PDF generation
- `data/` - Problem storage
- `worksheets/` - Generated PDFs
```

## 🤝 Contributing

Contributions are welcome! Please submit a PR or open an issue.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.
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
