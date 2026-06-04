
import streamlit as st
from pdf2docx import Converter
import io

st.set_page_config(layout="wide", page_title="PDF to DOCX Converter")
st.title("PDF to DOCX Converter")

st.markdown("Upload your PDF file below to convert it to a DOCX file.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.success("PDF file uploaded successfully!")

    # Create in-memory file-like objects
    pdf_file_in_memory = io.BytesIO(uploaded_file.getvalue())
    docx_file_in_memory = io.BytesIO()

    try:
        with st.spinner("Converting PDF to DOCX..."):
            cv = Converter(pdf_file_in_memory)
            cv.convert(docx_file_in_memory)
            cv.close()
        st.success("Conversion complete!")

        docx_file_in_memory.seek(0)
        st.download_button(
            label="Download DOCX File",
            data=docx_file_in_memory.getvalue(),
            file_name=uploaded_file.name.replace(".pdf", ".docx"),
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    except Exception as e:
        st.error(f"An error occurred during conversion: {e}")
        st.info("Please ensure the PDF is not password-protected or corrupted.")
