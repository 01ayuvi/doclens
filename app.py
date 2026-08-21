import streamlit as st

from services.document_processor import process_document
from services.ai_analyzer import analyze_document


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

            document = process_document(
                file_bytes,
                uploaded_file.name,
            )

        st.success(
            "Document processed successfully."
        )

        # -----------------------------------------
        # DOCUMENT OVERVIEW
        # -----------------------------------------

        st.subheader(
            "Document Overview"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Pages",
                document["page_count"]
            )

        with col2:
            st.metric(
                "Words",
                f"{document['word_count']:,}"
            )

        with col3:
            st.metric(
                "Characters",
                f"{document['character_count']:,}"
            )

        st.caption(
            f"File: {document['filename']} | "
            f"Type: {document['file_type'].upper()}"
        )

        # -----------------------------------------
        # SUMMARY LENGTH
        # -----------------------------------------

        st.subheader(
            "AI Analysis"
        )

        summary_length = st.radio(
            "Summary length",
            options=[
                "short",
                "medium",
                "long",
            ],
            format_func=lambda value: value.capitalize(),
            horizontal=True,
        )

        analyze_button = st.button(
            "✨ Analyze Document",
            type="primary",
        )

        # -----------------------------------------
        # AI ANALYSIS
        # -----------------------------------------

        if analyze_button:

            document_text = "\n\n".join(
                page["text"]
                for page in document["pages"]
                if page["text"]
            )

            if not document_text.strip():

                st.warning(
                    "No text could be extracted "
                    "from this document."
                )

            else:

                with st.spinner(
                    "Generating document insights..."
                ):

                    analysis = analyze_document(
                        document_text,
                        summary_length=summary_length,
                    )

                st.success(
                    "Document analysis complete."
                )

                # ---------------------------------
                # SUMMARY
                # ---------------------------------

                st.subheader(
                    "📝 Summary"
                )

                st.write(
                    analysis["summary"]
                )

                # ---------------------------------
                # KEY POINTS
                # ---------------------------------

                st.subheader(
                    "🔑 Key Points"
                )

                for point in analysis[
                    "key_points"
                ]:

                    st.markdown(
                        f"- {point}"
                    )

                # ---------------------------------
                # IMPROVEMENTS
                # ---------------------------------

                st.subheader(
                    "💡 Improvement Suggestions"
                )

                for index, suggestion in enumerate(
                    analysis[
                        "improvement_suggestions"
                    ],
                    start=1,
                ):

                    st.markdown(
                        f"**{index}.** {suggestion}"
                    )

        # -----------------------------------------
        # RAW DOCUMENT
        # -----------------------------------------

        with st.expander(
            "View Extracted Document"
        ):

            for page in document["pages"]:

                st.markdown(
                    f"### Page {page['page_number']}"
                )

                if page["text"]:

                    st.text(
                        page["text"]
                    )

                else:

                    st.warning(
                        "No text detected on this page."
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