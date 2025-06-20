import streamlit as st
from metadata_utils import extract_docx_metadata
import os
import json

st.set_page_config(page_title="Metadata Generator", page_icon="📄", layout="centered")

# Sidebar Info
with st.sidebar:
    st.title("🧠 MetaGen System")
    st.write("Auto-generate metadata from documents.")
    st.markdown("---")
    st.markdown("👤 Made by [Naman Malu](https://www.linkedin.com)")
    st.markdown("💻 [View GitHub Repo](https://github.com/YOUR_USERNAME/automated-metadata-generator)")
    st.markdown("📨 Contact: naman_m@ee.iitr.ac.in")

# Main Title
st.title("📄 Automated Metadata Generator")
st.caption("Upload a document (.docx/.pdf/.txt) and get smart, structured metadata instantly.")

# File uploader
uploaded_file = st.file_uploader("Upload your document file", type=["docx", "pdf", "txt"])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    
    # Save temp file
    with open("temp_file." + file_extension, "wb") as f:
        f.write(uploaded_file.read())
    
    # Extract Metadata
    if file_extension == "docx":
        metadata = extract_docx_metadata("temp_file.docx")
    else:
        metadata = {
            "filename": uploaded_file.name,
            "error": "Only DOCX supported currently. PDF/TXT support coming soon!"
        }

    # Display Output
    st.subheader("🧾 Extracted Metadata")
    st.json(metadata)

    # Preview document text
    try:
        with open("temp_file." + file_extension, "r", encoding="utf-8") as f:
            text_preview = f.read(700)
            st.subheader("📑 Document Preview")
            st.text(text_preview + "...")
    except:
        pass

    # Download Metadata JSON
    st.download_button("📥 Download Metadata (JSON)", json.dumps(metadata, indent=4), file_name="metadata.json", mime="application/json")

    # Clean up
    os.remove("temp_file." + file_extension)
