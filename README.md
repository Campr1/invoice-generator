# Invoice Generator (Python + ReportLab)

This project generates a sample PDF invoice using Python and the ReportLab library.

## Features
- PDF invoice generation from editable sample data
- Canadian tax (HST) calculation and total breakdown
- Structured layout for billing details, project scope, and payment terms
- Wrapped text handling for long descriptions
- Simple AI helper to turn rough job notes into polished invoice scope bullet points

## Tech Stack
- Python
- ReportLab

## How to Run

1. Install dependencies:
   python3 -m pip install -r requirements.txt

2. Run the script:
   python3 invoice.py

3. The invoice PDF will be generated in the project folder.

## AI Feature (Experimental)

This project includes a simple AI-powered helper that converts rough job notes into clean invoice-ready scope descriptions.

Example:

Input:
`demo washroom, move toilet slightly, install vanity`

Output:
- Demolish existing washroom finishes
- Relocate toilet and complete necessary plumbing adjustments
- Install new vanity

Run:
`python3 ai_scope_test.py "your notes here"`

Setup:

1. Install the dependency:
   `python3 -m pip install -r requirements.txt`
2. Export your API key:
   `export OPENAI_API_KEY="your_api_key_here"`

## Notes

- All invoice content in this repo uses placeholder sample values
- Update the constants in `invoice.py` to customize the generated invoice
