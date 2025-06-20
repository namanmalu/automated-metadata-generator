import os
import re
import docx
import fitz  # PyMuPDF
from collections import Counter

def extract_docx_metadata(docx_path):
    doc = docx.Document(docx_path)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    title = doc.paragraphs[0].text.strip() if doc.paragraphs else "Untitled"
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}", full_text)
    authors = re.findall(r"\n([A-Z][a-z]+\s[A-Z][a-z]+)\s+\nElectrical Engineering", full_text)
    institution = "IIT Roorkee" if "IIT Roorkee" in full_text else "Unknown"
    words = re.findall(r'\\b\\w{4,}\\b', full_text.lower())
    common_words = Counter(words).most_common(10)
    metadata = {
        "filename": os.path.basename(docx_path),
        "title": title,
        "authors": list(set(authors)),
        "institution": institution,
        "email_ids": list(set(emails)),
        "word_count": len(words),
        "character_count": len(full_text),
        "top_keywords": [word for word, _ in common_words]
    }
    return metadata

def extract_pdf_metadata(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    words = re.findall(r'\\b\\w{4,}\\b', text.lower())
    common_words = Counter(words).most_common(10)
    metadata = {
        "filename": os.path.basename(pdf_path),
        "word_count": len(words),
        "character_count": len(text),
        "top_keywords": [word for word, _ in common_words]
    }
    return metadata

def extract_txt_metadata(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
    words = re.findall(r'\\b\\w{4,}\\b', text.lower())
    common_words = Counter(words).most_common(10)
    metadata = {
        "filename": os.path.basename(txt_path),
        "word_count": len(words),
        "character_count": len(text),
        "top_keywords": [word for word, _ in common_words]
    }
    return metadata
