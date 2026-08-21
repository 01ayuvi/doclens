import streamlit as st

from services.document_processor import process_document
from services.ai_analyzer import analyze_document
from services.qa_service import answer_document_question


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="DocLens",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM STYLING
# =========================================================

st.markdown(
    """
    <style>

    /* Main page */

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* Hero */

    .hero {
        padding: 1.5rem 0 2rem 0;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 750;
        margin-bottom: 0.25rem;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        opacity: 0.72;
        margin-bottom: 0.4rem;
    }

    .hero-description {
        opacity: 0.55;
        font-size: 0.95rem;
    }


    /* Metric cards */

    .metric-card {
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 14px;
        padding: 1.1rem 1.2rem;
        background: rgba(255,255,255,0.035);
        min-height: 115px;
    }

    .metric-label {
        font-size: 0.82rem;
        opacity: 0.6;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        font-size: 1.9rem;
        font-weight: 700;
    }

    .metric-description {
        font-size: 0.75rem;
        opacity: 0.5;
        margin-top: 0.2rem;
    }


    /* Section titles */

    .section-title {
        font-size: 1.45rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 0.8rem;
    }


    /* Intelligence cards */

    .intel-card {
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 14px;
        padding: 1rem;
        background: rgba(255,255,255,0.035);
        min-height: 105px;
    }

    .intel-label {
        font-size: 0.75rem;
        opacity: 0.55;
        margin-bottom: 0.35rem;
    }

    .intel-value {
        font-size: 1rem;
        font-weight: 650;
    }


    /* Evidence */

    .evidence-card {
        border-left: 3px solid rgba(255,255,255,0.35);
        padding: 0.7rem 1rem;
        margin: 0.5rem 0;
        background: rgba(255,255,255,0.025);
        border-radius: 0 8px 8px 0;
    }


    /* Health */

    .health-good {
        border: 1px solid rgba(50,205,100,0.25);
        border-radius: 14px;
        padding: 1rem;
        background: rgba(50,205,100,0.06);
    }


    /* Upload area */

    [data-testid="stFileUploader"] {
        border-radius: 14px;
    }


    /* Buttons */

    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "document" not in st.session_state:
    st.session_state.document = None

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "qa_answer" not in st.session_state:
    st.session_state.qa_answer = None

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">📄 DocLens</div>
        <div class="hero-subtitle">
            AI Document Intelligence Assistant
        </div>
        <div class="hero-description">
            Turn complex documents into clear, actionable intelligence.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# UPLOAD
# =========================================================

st.markdown(
    '<div class="section-title">Upload Document</div>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload a PDF or image",
    type=["pdf", "png", "jpg", "jpeg"],
    help=(
        "DocLens supports PDFs, scanned PDFs, "
        "PNG, JPG and JPEG documents."
    ),
)


# =========================================================
# DOCUMENT PROCESSING
# =========================================================

if uploaded_file is not None:

    # Detect a new document
    if (
        st.session_state.uploaded_filename
        != uploaded_file.name
    ):

        st.session_state.uploaded_filename = (
            uploaded_file.name
        )

        st.session_state.analysis = None
        st.session_state.qa_answer = None

        file_bytes = uploaded_file.getvalue()

        try:

            with st.spinner(
                "Processing document..."
            ):

                st.session_state.document = (
                    process_document(
                        file_bytes,
                        uploaded_file.name,
                    )
                )

            st.success(
                "Document processed successfully."
            )

        except ValueError as error:

            st.error(str(error))
            st.session_state.document = None

        except Exception as error:

            st.error(
                "Something went wrong while processing "
                "the document."
            )

            st.exception(error)


# =========================================================
# MAIN APPLICATION
# =========================================================

document = st.session_state.document


if document is not None:

    # =====================================================
    # DOCUMENT HEADER
    # =====================================================

    st.markdown(
        '<div class="section-title">Document Overview</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        f"📄 {document['filename']}  •  "
        f"{document['file_type'].upper()}"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">PAGES</div>
                <div class="metric-value">
                    {document['page_count']}
                </div>
                <div class="metric-description">
                    Document length
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">WORDS</div>
                <div class="metric-value">
                    {document['word_count']:,}
                </div>
                <div class="metric-description">
                    Extracted words
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">CHARACTERS</div>
                <div class="metric-value">
                    {document['character_count']:,}
                </div>
                <div class="metric-description">
                    Extracted characters
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:

        non_empty_pages = sum(
            1
            for page in document["pages"]
            if page["text"].strip()
        )

        page_coverage = (
            non_empty_pages
            / document["page_count"]
            * 100
            if document["page_count"]
            else 0
        )

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    TEXT COVERAGE
                </div>
                <div class="metric-value">
                    {page_coverage:.0f}%
                </div>
                <div class="metric-description">
                    Pages with extracted text
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    # =====================================================
    # DOCUMENT HEALTH
    # =====================================================

    st.markdown(
        '<div class="section-title">Document Health</div>',
        unsafe_allow_html=True,
    )

    average_words = (
        document["word_count"]
        / document["page_count"]
        if document["page_count"]
        else 0
    )

    if page_coverage >= 90:

        health_label = "Excellent"

    elif page_coverage >= 70:

        health_label = "Good"

    elif page_coverage >= 40:

        health_label = "Partial"

    else:

        health_label = "Limited"

    st.markdown(
        f"""
        <div class="health-good">
            <strong>Extraction status: {health_label}</strong>
            <br>
            <span style="opacity:0.65;">
                {non_empty_pages} of {document['page_count']}
                pages contain extracted text.
                Average {average_words:.0f} words per page.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # =====================================================
    # AI ANALYSIS
    # =====================================================

    st.markdown(
        '<div class="section-title">AI Analysis</div>',
        unsafe_allow_html=True,
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
        use_container_width=False,
    )


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

            try:

                with st.spinner(
                    "Generating document intelligence..."
                ):

                    st.session_state.analysis = (
                        analyze_document(
                            document_text,
                            summary_length=summary_length,
                        )
                    )

                st.success(
                    "Document analysis complete."
                )

            except ValueError as error:

                st.error(str(error))

            except Exception as error:

                error_text = str(error)

                if "429" in error_text:

                    st.warning(
                        "AI usage limit reached. "
                        "The Gemini API quota is temporarily "
                        "exhausted. Your document and extracted "
                        "content are still available."
                    )

                else:

                    st.error(
                        "Something went wrong while "
                        "generating the analysis."
                    )

                    st.exception(error)


    # =====================================================
    # DISPLAY AI ANALYSIS
    # =====================================================

    analysis = st.session_state.analysis


    if analysis is not None:

        # -------------------------------------------------
        # SUMMARY
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">📝 Summary</div>',
            unsafe_allow_html=True,
        )

        st.write(
            analysis["summary"]
        )


        # -------------------------------------------------
        # KEY POINTS
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">🔑 Key Points</div>',
            unsafe_allow_html=True,
        )

        for point in analysis["key_points"]:

            st.markdown(
                f"• {point}"
            )


        # -------------------------------------------------
        # IMPROVEMENTS
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '💡 Improvement Suggestions'
            '</div>',
            unsafe_allow_html=True,
        )

        for index, suggestion in enumerate(
            analysis["improvement_suggestions"],
            start=1,
        ):

            st.markdown(
                f"**{index}.** {suggestion}"
            )


        # -------------------------------------------------
        # DOCUMENT INTELLIGENCE
        # -------------------------------------------------

        intelligence = analysis[
            "document_intelligence"
        ]

        st.markdown(
            '<div class="section-title">'
            '🧠 Document Intelligence'
            '</div>',
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(
                f"""
                <div class="intel-card">
                    <div class="intel-label">
                        DOCUMENT TYPE
                    </div>
                    <div class="intel-value">
                        {intelligence['document_type']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:

            st.markdown(
                f"""
                <div class="intel-card">
                    <div class="intel-label">
                        PRIMARY TOPIC
                    </div>
                    <div class="intel-value">
                        {intelligence['primary_topic']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:

            st.markdown(
                f"""
                <div class="intel-card">
                    <div class="intel-label">
                        COMPLEXITY
                    </div>
                    <div class="intel-value">
                        {intelligence['complexity']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


        # -------------------------------------------------
        # THEMES
        # -------------------------------------------------

        st.markdown(
            "### Main Themes"
        )

        for theme in intelligence[
            "main_themes"
        ]:

            st.markdown(
                f"• {theme}"
            )


        # -------------------------------------------------
        # TAKEAWAY
        # -------------------------------------------------

        st.markdown(
            "### 🎯 Key Takeaway"
        )

        st.info(
            intelligence["key_takeaway"]
        )


        # -------------------------------------------------
        # ACTIONABLE INSIGHTS
        # -------------------------------------------------

        st.markdown(
            "### ⚡ Actionable Insights"
        )

        for insight in intelligence[
            "actionable_insights"
        ]:

            st.markdown(
                f"→ {insight}"
            )


    # =====================================================
    # ASK DOCLENS
    # =====================================================

    st.markdown(
        '<div class="section-title">💬 Ask DocLens</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Ask questions grounded only in the uploaded document."
    )

    question = st.text_input(
        "Your question",
        placeholder=(
            "e.g. What are the major research gaps?"
        ),
    )

    ask_button = st.button(
        "🔎 Ask Document",
    )


    if ask_button:

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            try:

                with st.spinner(
                    "Searching the document..."
                ):

                    st.session_state.qa_answer = (
                        answer_document_question(
                            document["pages"],
                            question,
                        )
                    )

            except ValueError as error:

                st.error(str(error))

            except Exception as error:

                error_text = str(error)

                if "429" in error_text:

                    st.warning(
                        "AI usage limit reached. "
                        "Please try again after the "
                        "Gemini API quota resets."
                    )

                else:

                    st.error(
                        "Something went wrong while "
                        "answering the question."
                    )

                    st.exception(error)


    # =====================================================
    # DISPLAY Q&A
    # =====================================================

    qa_answer = st.session_state.qa_answer


    if qa_answer is not None:

        st.markdown(
            "### Answer"
        )

        st.write(
            qa_answer["answer"]
        )

        confidence = qa_answer[
            "confidence"
        ]

        st.caption(
            f"Confidence: {confidence}"
        )


        # -------------------------------------------------
        # VERIFIED SOURCES
        # -------------------------------------------------

        sources = qa_answer.get(
            "sources",
            [],
        )

        if sources:

            st.markdown(
                "### 📚 Evidence from the document"
            )

            for source in sources:

                page_number = source[
                    "page"
                ]

                quote = source[
                    "quote"
                ]

                with st.expander(
                    f"📄 Page {page_number}"
                ):

                    st.markdown(
                        f"> {quote}"
                    )

        else:

            st.info(
                "This answer is not supported "
                "by the uploaded document."
            )


    # =====================================================
    # EXTRACTED DOCUMENT
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '📖 Document Text'
        '</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Review the text DocLens extracted from each page."
    )

    with st.expander(
        "View extracted document"
    ):

        page_numbers = [
            page["page_number"]
            for page in document["pages"]
        ]

        selected_page = st.selectbox(
            "Select page",
            page_numbers,
        )

        selected_page_data = next(
            page
            for page in document["pages"]
            if page["page_number"]
            == selected_page
        )

        st.markdown(
            f"### Page {selected_page}"
        )

        if selected_page_data["text"]:

            st.text(
                selected_page_data["text"]
            )

        else:

            st.warning(
                "No text detected on this page."
            )


# =========================================================
# EMPTY STATE
# =========================================================

else:

    st.info(
        "Upload a PDF or image to begin."
    )