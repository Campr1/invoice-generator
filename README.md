# Invoice Generator (Python + ReportLab)

This project generates a sample PDF invoice using Python and the ReportLab library.

## Features
- PDF invoice generation from editable sample data
- Canadian tax (HST) calculation and total breakdown
- Structured layout for billing details, project scope, and payment terms
- Wrapped text handling for long descriptions

## Tech Stack
- Python
- ReportLab

## How to Run

1. Install dependencies:
   python3 -m pip install reportlab

2. Run the script:
   python3 invoice.py

3. The invoice PDF will be generated in the project folder.

## Notes

- All invoice content in this repo uses placeholder sample values
- Update the constants in `invoice.py` to customize the generated invoice
