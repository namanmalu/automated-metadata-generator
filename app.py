import streamlit as st
from metadata_utils import extract_docx_metadata
import os
import json

st.set_page_config(
    page_title="Smart Metadata Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Netflix-style CSS ---
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
    .feature-title {
        font-size: 1.15em;
        font-weight: 600;
        margin-bottom: 0.5em;
        color: #ff3c78;
        letter-spacing: 1px;
    }
    .feature-desc {
        font-size: 1em;
        color: #e0e7ef;
        font-weight: 400;
    }
    .sexy-card {
        background: linear-gradient(135deg, #23243a 60%, #3e206d 100%);
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(50, 50, 93, 0.22);
        padding: 28px 24px;
        margin-bottom: 24px;
        color: #fff;
        border: 1.5px solid #4B8BBE33;
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
    [data-testid="stSidebar"] {
        background: linear-gradient(120deg, #23243a 0%, #18181c 100%) !important;
        color: #fff !important;
    }
    .stAlert {
        margin-left: auto;
        margin-right: auto;
        width: 75%;
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
                    AI-powered, automatic, and beautifully simple — your documents, decoded.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- Features Row (Netflix-style cards) ---
st.markdown('<div class="features-row">', unsafe_allow_html=True)

features = [
    {
        "title": "Automating Metadata Generation",
        "desc": "The system automatically generates metadata for various unstructured document types."
    },
    {
        "title": "Content Extraction",
        "desc": "Extracts text content from diverse formats like PDF, DOCX, and TXT, with OCR where needed."
    },
    {
        "title": "Semantic Content Identification",
        "desc": "Identifies and leverages the most meaningful document sections for metadata generation."
    },
    {
        "title": "Structured Metadata Creation",
        "desc": "Produces structured, machine-readable metadata outputs for your documents."
    },
    {
        "title": "Intuitive User Interface",
        "desc": "A web interface for easy document upload and instant metadata viewing."
    },
    {
        "title": "Public Deployment",
        "desc": "Fully deployed for public accessibility and effortless use by everyone."
    }
]

for f in features:
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-title">{f['title']}</div>
            <div class="feature-desc">{f['desc']}</div>
        </div>
        """, unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

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

# --- Main Content: Upload & Metadata ---
st.markdown("<h3 style='color:#ff3c78; margin-bottom:0.5em;'>📂 Upload Your DOCX Document</h3>", unsafe_allow_html=True)

col_center = st.columns([0.15, 0.7, 0.15])[1]

with col_center:
    uploaded_file = st.file_uploader("Drag or click to upload a .docx file", type=["docx"])

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

        try:
            import docx
            doc = docx.Document(file_path)
            preview_text = "\n".join([p.text for p in doc.paragraphs[:5]])
            st.markdown("""
                <div class="sexy-card">
                    <h4 style='color:#ff3c78;'>📖 Preview of Document:</h4>
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
    <hr style="margin-top: 3em; margin-bottom: 1em; border: 1px solid #333;">
    <div style="text-align: center; color: #888; font-size: 0.9em;">
        Made with ❤️ using Streamlit & Python NLP · 2025
    </div>
""", unsafe_allow_html=True)


