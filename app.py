import streamlit as st
from pdf2docx import Converter
import tempfile
import os

st.set_page_config(layout="wide", page_title="PDF to DOCX Converter")
st.title("PDF to DOCX Converter")

st.markdown("Upload your PDF file below to convert it to a DOCX file.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.success("PDF file uploaded successfully!")

    try:
        with st.spinner("Converting PDF to DOCX..."):
            # Save uploaded PDF to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf.write(uploaded_file.getvalue())
                tmp_pdf_path = tmp_pdf.name

            # Create a temporary file path for the output DOCX
            tmp_docx_path = tmp_pdf_path.replace(".pdf", ".docx")

            # Convert using file paths
            cv = Converter(tmp_pdf_path)
            cv.convert(tmp_docx_path)
            cv.close()

        st.success("Conversion complete!")

        # Read the converted DOCX file for download
        with open(tmp_docx_path, "rb") as f:
            docx_data = f.read()

        st.download_button(
            label="Download DOCX File",
            data=docx_data,
            file_name=uploaded_file.name.replace(".pdf", ".docx"),
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        # Clean up temporary files
        os.unlink(tmp_pdf_path)
        if os.path.exists(tmp_docx_path):
            os.unlink(tmp_docx_path)

    except Exception as e:
        st.error(f"An error occurred during conversion: {e}")
        st.info("Please ensure the PDF is not password-protected or corrupted.")
