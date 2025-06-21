# Smart Metadata Generator

Smart Metadata Generator is a web-based application designed to automatically extract meaningful and structured metadata from documents such as DOCX, PDF, and TXT files. It aims to assist students, researchers, and professionals by providing quick insights about their documents without manual review.

Whether you’re preparing a research paper, validating document quality, or building an automated document processing system, this tool streamlines the process of extracting the most relevant information from unstructured content.

---

## What does this project do?

The system reads a user-uploaded document and intelligently generates metadata that includes:
- Word and character count
- Important keywords using TF-IDF
- Named entities such as people, organizations, dates, and places
- Summaries and objectives derived from content analysis
- Section-wise content breakdown (e.g., Introduction, Conclusion, etc.)
- OCR-based text extraction from scanned PDFs

This metadata can then be used for search indexing, content classification, or as a preprocessing step in larger NLP or ML pipelines.

---

## Key Features

- Automatic metadata generation without manual labeling
- Semantic section identification (summary, objective, etc.)
- Named entity recognition (NER) using spaCy
- OCR support for scanned PDFs via pytesseract
- Multi-format support for `.docx`, `.pdf`, and `.txt`
- Streamlit-powered UI for easy interaction and JSON export

---

## Technologies Used

- Python
- spaCy (for NLP and NER)
- TfidfVectorizer (for keyword extraction)
- PyMuPDF and pdf2image (for PDF parsing)
- pytesseract (for OCR)
- Streamlit (for the web app)

---

## Getting Started

Follow these steps to set up and run the project locally.



```bash
git clone https://github.com/namanmalu/automated-metadata-generator.git
cd automated-metadata-generator
pip install -r requirements.txt
streamlit run app.py

