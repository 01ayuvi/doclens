import streamlit as st

from services.extractor import extract_pdf


st.set_page_config(
    page_title="DocLens",
    page_icon="📄",
    layout="wide",
)

st.title("📄 DocLens")
st.subheader("AI Document Intelligence Assistant")

st.write(
    "Turn complex documents into clear, actionable intelligence."
)

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
    help=(
        "Upload a text-based PDF. "
        "Scanned documents will be supported through OCR."
    ),
)


if uploaded_file is not None:

    file_bytes = uploaded_file.getvalue()

    try:

        with st.spinner("Analyzing document..."):
            result = extract_pdf(file_bytes)

        st.success("PDF processed successfully.")

        st.subheader("Document Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Pages",
                result["page_count"]
            )

        with col2:
            st.metric(
                "Words",
                f"{result['word_count']:,}"
            )

        with col3:
            st.metric(
                "Characters",
                f"{result['character_count']:,}"
            )

        st.subheader("Extracted Content")

        for page in result["pages"]:

            with st.expander(
                f"Page {page['page_number']} "
                f"({page['word_count']:,} words)"
            ):

                if page["text"]:

                    st.text(page["text"])

                else:

                    st.warning(
                        "No text was detected on this page. "
                        "OCR may be required."
                    )

    except Exception as error:

        st.error(
            f"Unable to process this PDF: {error}"
        )