# Raw Data Directory

This directory contains the raw admission brochure files (PDFs) that will be processed by the data extraction module.

## Instructions

1. Place your MMMUT admission brochure PDF files in this directory
2. Supported formats: PDF files (.pdf)
3. The data extraction module will automatically process all PDF files in this directory

## Sample Data

If no PDF files are present, the system will create sample data based on typical MMMUT admission information.

## File Naming Convention

- Use descriptive names like: `MMMUT_UG_Admission_Brochure_2024.pdf`
- Avoid special characters and spaces in filenames
- Use underscores (_) instead of spaces

## Processing

Run the data extraction module to process files:
```bash
python src/data_extraction.py
```