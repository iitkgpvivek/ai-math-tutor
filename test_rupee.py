#!/usr/bin/env python3
"""Test script to verify Rupee symbol display in PDF."""

import json
import os
from generate_pdf import create_pdf

# Create a test worksheet with Rupee symbol
test_worksheet = {
    'topic': 'Currency Test',
    'difficulty': 'Test',
    'date': '2025-08-13',
    'problems': [
        {
            'problem': 'A book costs Rs. 250. If Riya has Rs. 1000, how many books can she buy?',
            'answer': '4 books',
            'type': 'test',
            'difficulty': 'easy'
        },
        {
            'problem': 'The price of a notebook is Rs. 45.50. How much will 8 such notebooks cost?',
            'answer': 'Rs. 364.00',
            'type': 'test',
            'difficulty': 'easy'
        }
    ]
}

# Create test directory if it doesn't exist
test_dir = 'test_output'
os.makedirs(test_dir, exist_ok=True)

# Generate the PDF
output_path = os.path.join(test_dir, 'rupee_test.pdf')
create_pdf(test_worksheet, include_answers=True, output_path=output_path)
print(f"Test PDF generated at: {os.path.abspath(output_path)}")
