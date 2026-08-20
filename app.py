import streamlit as st

from services.document_processor import process_document


st.set_page_config(
    page_title="DocLens",
    page_icon="📄",
    layout="wide",
)

st.title("📄 DocLens")

st.subheader(
    "AI Document Intelligence Assistant"
)

st.write(
    "Turn complex documents into clear, actionable intelligence."
)


uploaded_file = st.file_uploader(
    "Upload a document",
    type=["pdf", "png", "jpg", "jpeg"],
    help=(
        "Upload a PDF, scanned PDF, PNG, JPG, "
        "or JPEG document."
    ),
)


if uploaded_file is not None:

    file_bytes = uploaded_file.getvalue()

    try:

        with st.spinner(
            "Processing document..."
        ):

            result = process_document(
                file_bytes,
                uploaded_file.name,
            )

        st.success(
            "Document processed successfully."
        )

        st.subheader(
            "Document Overview"
        )

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

        st.caption(
            f"File type: {result['file_type'].upper()}"
        )

        st.subheader(
            "Extracted Content"
        )

        for page in result["pages"]:

            with st.expander(
                f"Page {page['page_number']} "
                f"({page['word_count']:,} words)"
            ):

                if page["text"]:

                    st.text(
                        page["text"]
                    )

                else:

                    st.warning(
                        "No text could be extracted "
                        "from this page."
                    )

    except ValueError as error:

        st.error(
            str(error)
        )

    except Exception as error:

        st.error(
            "Something went wrong while processing "
            "the document."
        )

        st.exception(error)