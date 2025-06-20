import streamlit as st
from metadata_utils import extract_docx_metadata
import os
import json
from PIL import Image

# Page config
st.set_page_config(
    page_title="Smart Metadata Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for sexy design
st.markdown("""
    <style>
    /* Banner */
    .main-banner {
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(90deg, #4B8BBE 0%, #306998 100%);
        border-radius: 20px;
        padding: 32px 24px;
        margin-bottom: 32px;
        box-shadow: 0 6px 24px rgba(50, 50, 93, 0.08);
    }
    .banner-title {
        font-size: 2.8em;
        font-weight: bold;
        color: white;
        margin-bottom: 0.2em;
        letter-spacing: 1px;
    }
    .banner-subtitle {
        font-size: 1.2em;
        color: #e0e7ef;
        margin-bottom: 0;
    }
    /* Card styling */
    .sexy-card {
        background: linear-gradient(135deg, #e0e7ff 0%, #f0f4f8 100%);
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(50, 50, 93, 0.10);
        padding: 28px 24px;
        margin-bottom: 24px;
    }
    /* File uploader */
    .stFileUploader > div > div {
        background-color: #f0f4f8;
        padding: 14px;
        border-radius: 12px;
        border: 2px dashed #4B8BBE;
    }
    /* Buttons */
    .stButton button {
        background: linear-gradient(90deg, #4B8BBE, #306998);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 22px;
        font-weight: 600;
        font-size: 1em;
        box-shadow: 0 2px 8px rgba(50, 50, 93, 0.10);
        transition: 0.2s;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #306998, #4B8BBE);
        color: #ffeb3b;
    }
    </style>
""", unsafe_allow_html=True)

# --- Main Banner ---
with st.container():
    st.markdown("""
        <div class="main-banner">
            <div>
                <div class="banner-title">📄 Smart Metadata Generator</div>
                <div class="banner-subtitle">
                    Understand your documents at a glance with NLP-powered metadata extraction.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://i.imgur.com/6M513eV.png", width=140)
    st.markdown("## 📘 About")
    st.write("""
    - 🚀 Extracts title, authors, word count, keywords, etc.
    - 📄 Supports `.docx` files (PDF/TXT coming soon)
    - 🌐 Powered by Streamlit + Python NLP
    """)
    st.markdown("---")
    st.write("👤 [Naman Malu](https://www.linkedin.com)")
    st.write("🔗 [GitHub](https://github.com/YOUR_USERNAME/automated-metadata-generator)")
    st.write("✉️ naman_m@ee.iitr.ac.in")

# --- Main Content ---
st.markdown("<h3 style='color:#4B8BBE;'>📂 Upload Your DOCX Document</h3>", unsafe_allow_html=True)

main_col1, main_col2 = st.columns([1,2])

with main_col1:
    uploaded_file = st.file_uploader("Drag or click to upload a .docx file", type=["docx"])

with main_col2:
    if uploaded_file:
        ext = uploaded_file.name.split(".")[-1].lower()
        file_path = f"temp_file.{ext}"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        with st.spinner("Extracting metadata..."):
            if ext == "docx":
                metadata = extract_docx_metadata(file_path)
            else:
                metadata = {"error": "Only DOCX files are supported at this time."}

        st.markdown("""
            <div class="sexy-card">
                <h4 style='color:#2E8B57;'>✅ Extracted Metadata:</h4>
            """, unsafe_allow_html=True)
        st.json(metadata)
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            "⬇️ Download Metadata (JSON)",
            json.dumps(metadata, indent=4),
            file_name="metadata.json",
            mime="application/json"
        )

        try:
            import docx
            doc = docx.Document(file_path)
            preview_text = "\n".join([p.text for p in doc.paragraphs[:5]])
            st.markdown("""
                <div class="sexy-card">
                    <h4 style='color:#1c4c96;'>📖 Preview of Document:</h4>
            """, unsafe_allow_html=True)
            st.code(preview_text)
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.warning("Could not preview document.")

        os.remove(file_path)
    else:
        st.info("Please upload a .docx file to get started.")

# --- Footer ---
st.markdown("""
    <hr style="margin-top: 3em; margin-bottom: 1em;">
    <div style="text-align: center; color: #888; font-size: 0.9em;">
        Made with ❤️ using Streamlit & Python NLP · 2025
    </div>
""", unsafe_allow_html=True)

