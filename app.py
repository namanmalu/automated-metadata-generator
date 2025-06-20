import streamlit as st
import os
import json
from metadata_utils import extract_metadata

st.set_page_config(
    page_title="Smart Metadata Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
    <style>
    body, .stApp {
        background: linear-gradient(120deg, #18181c 0%, #23243a 100%) !important;
        color: #fff !important;
    }
    .main-banner {
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(90deg, #141e30 0%, #243b55 100%);
        border-radius: 24px;
        padding: 40px 32px;
        margin-bottom: 32px;
        box-shadow: 0 8px 40px 0 rgba(0,0,0,0.45);
    }
    .banner-title {
        font-size: 3em;
        font-weight: bold;
        color: #fff;
        margin-bottom: 0.2em;
        letter-spacing: 2px;
        text-shadow: 0 4px 32px #0008;
    }
    .banner-subtitle {
        font-size: 1.25em;
        color: #e0e7ef;
        margin-bottom: 0;
        font-weight: 400;
    }
    .features-row {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 32px;
        margin-bottom: 36px;
    }
    .feature-card {
        background: linear-gradient(135deg, #23243a 60%, #3e206d 100%);
        border-radius: 18px;
        box-shadow: 0 4px 32px 0 rgba(72,0,128,0.25);
        padding: 28px 30px 22px 30px;
        min-width: 280px;
        max-width: 340px;
        color: #fff;
        margin-bottom: 0;
        border: 1.5px solid #4B8BBE33;
        transition: transform 0.18s;
    }
    .feature-card:hover {
        transform: scale(1.04) translateY(-6px);
        box-shadow: 0 8px 48px 0 rgba(72,0,128,0.38);
        border: 1.5px solid #4B8BBE;
    }
    .stFileUploader > div > div {
        background-color: #23243a;
        padding: 14px;
        border-radius: 12px;
        border: 2px dashed #4B8BBE;
        color: #fff;
    }
    .stButton button {
        background: linear-gradient(90deg, #ff3c78, #4B8BBE);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 22px;
        font-weight: 600;
        font-size: 1em;
        box-shadow: 0 2px 8px rgba(50, 50, 93, 0.18);
        transition: 0.2s;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #4B8BBE, #ff3c78);
        color: #ffeb3b;
    }
    </style>
""", unsafe_allow_html=True)

# --- Main Banner ---
st.markdown("""
    <div class="main-banner">
        <div>
            <div class="banner-title">📄 Smart Metadata Generator</div>
            <div class="banner-subtitle">
                AI-powered, automatic, and beautifully simple — for DOCX, PDF, and TXT files.
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Features Section ---
st.markdown('<div class="features-row">', unsafe_allow_html=True)
features = [
    {"title": "Automating Metadata Generation", "desc": "Auto-generates metadata for diverse documents."},
    {"title": "Content Extraction", "desc": "Extracts text from PDF, DOCX, TXT using OCR where needed."},
    {"title": "Semantic Content Identification", "desc": "Leverages key sections of documents intelligently."},
    {"title": "Structured Metadata Creation", "desc": "Outputs clean, structured, machine-readable metadata."},
    {"title": "Easy-to-Use Interface", "desc": "Simple web app with beautiful design and usability."},
    {"title": "Supports Multiple Formats", "desc": "Works with .docx, .pdf, and .txt files."},
]
for f in features:
    st.markdown(f"""
        <div class="feature-card">
            <div class="feature-title">{f['title']}</div>
            <div class="feature-desc">{f['desc']}</div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- Upload + Metadata Display ---
st.markdown("<h3 style='color:#ff3c78;'>📂 Upload Your Document (DOCX / PDF / TXT)</h3>", unsafe_allow_html=True)
file = st.file_uploader("Drag or click to upload a file", type=["docx", "pdf", "txt"])

if file:
    file_ext = file.name.split(".")[-1].lower()
    temp_path = f"temp_uploaded.{file_ext}"
    with open(temp_path, "wb") as f:
        f.write(file.read())

    with st.spinner("🔍 Extracting metadata..."):
        metadata = extract_metadata(temp_path)
        if "filename" in metadata:
            metadata["filename"] = file.name
        metadata = {k: v for k, v in metadata.items() if v and v != [] and v != {} and v != "None"}

    if "error" in metadata:
        st.error(metadata["error"])
    else:
        st.markdown("""
            <div class="sexy-card">
                <h4 style='color:#4B8BBE;'>✅ Extracted Metadata:</h4>
        """, unsafe_allow_html=True)
        st.json(metadata)
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            "⬇️ Download Metadata (JSON)",
            json.dumps(metadata, indent=4),
            file_name="metadata.json",
            mime="application/json"
        )

    os.remove(temp_path)
else:
    st.info("Please upload a DOCX, PDF, or TXT file to get started.")

# --- Footer ---
st.markdown("""
    <hr style="margin-top: 3em; margin-bottom: 1em; border: 1px solid #333;">
    <div style="text-align: center; color: #888; font-size: 0.9em;">
        Made with ❤️ using Streamlit & Python NLP · 2025
    </div>
""", unsafe_allow_html=True)


