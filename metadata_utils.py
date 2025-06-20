import os
import re
import docx
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from collections import Counter
import io
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_top_sentences(text, n=5):
    sentences = re.split(r'(?<=[.!?]) +', text)
    if len(sentences) <= n:
        return sentences
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(sentences)
    sim_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix).flatten()
    top_indices = sim_scores.argsort()[-n:][::-1]
    return [sentences[i] for i in top_indices if i < len(sentences)]

def structure_metadata(metadata_dict):
    structured = {}
    for key, value in metadata_dict.items():
        if isinstance(value, list):
            structured[key] = [str(v).strip() for v in value if str(v).strip()]
        else:
            structured[key] = str(value).strip()
    return structured

def extract_docx_metadata(docx_path):
    doc = docx.Document(docx_path)
    full_text = "\n".join([para.text for para in doc.paragraphs])
    title = doc.paragraphs[0].text.strip() if doc.paragraphs else "Untitled"
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", full_text)
    authors = re.findall(r"\n([A-Z][a-z]+\s[A-Z][a-z]+)\s+\nElectrical Engineering", full_text)
    institution = "IIT Roorkee" if "IIT Roorkee" in full_text else "Unknown"
    words = re.findall(r'\b\w{4,}\b', full_text.lower())
    common_words = Counter(words).most_common(10)
    top_sentences = get_top_sentences(full_text)
    metadata = {
        "filename": os.path.basename(docx_path),
        "title": title,
        "authors": list(set(authors)),
        "institution": institution,
        "email_ids": list(set(emails)),
        "word_count": len(words),
        "character_count": len(full_text),
        "top_keywords": [word for word, _ in common_words],
        "key_sentences": top_sentences
    }
    return structure_metadata(metadata)

def extract_pdf_metadata(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                page_text = page.get_text()
                if page_text.strip():
                    text += page_text
        if not text.strip():
            images = convert_from_path(pdf_path)
            for img in images:
                text += pytesseract.image_to_string(img)
    except Exception as e:
        text = f"Error reading PDF: {str(e)}"
    words = re.findall(r'\b\w{4,}\b', text.lower())
    common_words = Counter(words).most_common(10)
    top_sentences = get_top_sentences(text)
    metadata = {
        "filename": os.path.basename(pdf_path),
        "word_count": len(words),
        "character_count": len(text),
        "top_keywords": [word for word, _ in common_words],
        "key_sentences": top_sentences
    }
    return structure_metadata(metadata)

def extract_txt_metadata(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()
    words = re.findall(r'\b\w{4,}\b', text.lower())
    common_words = Counter(words).most_common(10)
    top_sentences = get_top_sentences(text)
    metadata = {
        "filename": os.path.basename(txt_path),
        "word_count": len(words),
        "character_count": len(text),
        "top_keywords": [word for word, _ in common_words],
        "key_sentences": top_sentences
    }
    return structure_metadata(metadata)

def extract_metadata(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_pdf_metadata(file_path)
    elif ext == ".docx":
        return extract_docx_metadata(file_path)
    elif ext == ".txt":
        return extract_txt_metadata(file_path)
    else:
        return structure_metadata({"error": "Unsupported file type", "filename": os.path.basename(file_path)})

def convert_metadata_to_csv(metadata):
    from io import StringIO
    import csv

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Field", "Value"])
    for key, value in metadata.items():
        if isinstance(value, list):
            value = ", ".join(map(str, value))
        writer.writerow([key, value])
    return output.getvalue()
