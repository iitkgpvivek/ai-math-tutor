#!/usr/bin/env python3
"""
Generate an integer worksheet and convert it to PDF.
"""
from generate_integer_worksheet import generate_integer_worksheet
from generate_pdf import load_latest_worksheet, create_pdf

def main():
    # Generate a new integer worksheet
    print("Generating integer worksheet...")
    json_file = generate_integer_worksheet(count=15, difficulty='hard')
    
    # Load the generated worksheet
    worksheet = load_latest_worksheet()
    if not worksheet:
        print("Error: Could not load the generated worksheet.")
        return
    
    # Generate PDFs
    print("Creating PDFs...")
    create_pdf(worksheet, include_answers=False)
    create_pdf(worksheet, include_answers=True)
    
    print("\nInteger worksheet generation complete!")
    print(f"- JSON file: {json_file}")
    print("- PDF files are in the 'worksheets' directory")

if __name__ == "__main__":
    main()
