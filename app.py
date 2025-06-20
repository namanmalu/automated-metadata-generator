import streamlit as st
from metadata_utils import extract_docx_metadata
import os
import json
from PIL import Image

st.set_page_config(page_title="Smart Metadata Generator", page_icon="📄", layout="wide")

# Add a banner with gradient and animation
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 3em;
        font-weight: bold;
        background: -webkit-linear-gradient(#4B8BBE, #306998);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        color: #555;
    }
    .stFileUploader > div > div {
        background-color: #f0f4f8;
        padding: 12px;
        border-radius: 10px;
        border: 2px dashed #4B8BBE;
    }
    .stButton button {
        background-color: #4B8BBE;
        color: white;
        border-radius: 6px;
        border: none;
        padding: 8px 16px;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    <div class='main-title'>📄 Smart Metadata Generator</div>
    <div class='subtitle'>Understand your documents at a glance with NLP-powered metadata extraction</div>
    <br>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://i.imgur.com/6M513eV.png", width=160)
    st.title("📘 About")
    st.write("""
        - 🚀 Extracts title, authors, word count, keywords, etc.
        - 📄 Supports `.docx` files (PDF/TXT coming soon)
        - 🌐 Powered by Streamlit + Python NLP
    """)
    st.markdown("---")
    st.write("👤 [Naman Malu](https://www.linkedin.com)")
    st.write("🔗 [GitHub](https://github.com/YOUR_USERNAME/automated-metadata-generator)")
    st.write("✉️ naman_m@ee.iitr.ac.in")

# Main uploader section
st.markdown("""
    <h3 style='color:#4B8BBE;'>📂 Upload Your DOCX Document</h3>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Drag or click to upload a .docx file", type=["docx"])

if uploaded_file:
    ext = uploaded_file.name.split(".")[-1].lower()
    file_path = f"temp_file.{ext}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    if ext == "docx":
        metadata = extract_docx_metadata(file_path)
    else:
        metadata = {"error": "Only DOCX files are supported at this time."}

    st.markdown("""
        <h3 style='color:#2E8B57;'>✅ Extracted Metadata:</h3>
    """, unsafe_allow_html=True)
    st.json(metadata)

    st.download_button("⬇️ Download Metadata (JSON)", json.dumps(metadata, indent=4), file_name="metadata.json", mime="application/json")

    try:
        import docx
        doc = docx.Document(file_path)
        preview_text = "\n".join([p.text for p in doc.paragraphs[:5]])
        st.markdown("""
            <h4 style='color:#1c4c96;'>📖 Preview of Document:</h4>
        """, unsafe_allow_html=True)
        st.code(preview_text)
    except:
        pass

    os.remove(file_path)
else:
    st.info("Please upload a .docx file to get started.")
