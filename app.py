import streamlit as st
from metadata_utils import extract_docx_metadata
import os

st.set_page_config(page_title="Automated Metadata Generator")
st.title("📄 Automated Metadata Generator")
st.write("Upload a DOCX file to generate structured metadata.")

uploaded_file = st.file_uploader("Choose a .docx file", type=["docx"])
if uploaded_file:
    with open("temp.docx", "wb") as f:
        f.write(uploaded_file.read())
    metadata = extract_docx_metadata("temp.docx")
    st.subheader("Extracted Metadata:")
    st.json(metadata)
    os.remove("temp.docx")