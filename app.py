import textwrap

import streamlit as st

from services.document_processor import process_document
from services.ai_analyzer import analyze_document
from services.qa_service import answer_document_question


# =========================================================
# HELPERS
# =========================================================

def render_html(content: str):
    """
    Render standalone HTML safely using Streamlit's
    native HTML renderer.
    """
    st.html(textwrap.dedent(content).strip())


def reset_document_state():
    st.session_state.document = None
    st.session_state.analysis = None
    st.session_state.qa_answer = None


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="DocLens | Document Intelligence",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
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
# ENTERPRISE THEME
# =========================================================

st.markdown(
    """
    <style>
    :root {
        --bg: #080a0f;
        --surface: #0f1219;
        --surface-2: #151923;
        --surface-3: #1a1f2b;
        --border: rgba(255,255,255,0.085);
        --border-strong: rgba(129,140,248,0.28);
        --text: #f4f5f8;
        --muted: #9299aa;
        --subtle: #687083;
        --accent: #8b7cff;
        --accent-2: #6d5dfc;
        --success: #34d399;
        --warning: #fbbf24;
        --danger: #fb7185;
    }

    /* ---------- APP SHELL ---------- */
    .stApp {
        background:
            radial-gradient(circle at 50% -10%, rgba(109,93,252,0.09), transparent 32%),
            var(--bg);
        color: var(--text);
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1.25rem;
        padding-bottom: 5rem;
    }

    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    .stAppDeployButton {
        background: transparent !important;
    }

    /* ---------- NAV ---------- */
    .dl-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-height: 52px;
        padding: 0.25rem 0 1rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 3.1rem;
    }

    .dl-brand { display:flex; align-items:center; gap:.7rem; }
    .dl-logo {
        width:36px; height:36px; display:flex; align-items:center; justify-content:center;
        border-radius:10px; color:white; font-size:.9rem; font-weight:800;
        background:linear-gradient(135deg,var(--accent-2),#9b6cff);
        box-shadow:0 8px 25px rgba(109,93,252,.25);
    }
    .dl-brand-name { font-size:1rem; font-weight:760; letter-spacing:-.2px; }
    .dl-brand-caption { margin-top:2px; color:var(--muted); font-size:.62rem; }
    .dl-status { display:flex; align-items:center; gap:.45rem; color:var(--muted); font-size:.67rem; }
    .dl-status-dot { width:7px; height:7px; border-radius:50%; background:var(--success); box-shadow:0 0 10px rgba(52,211,153,.65); }

    /* ---------- HERO ---------- */
    .dl-eyebrow {
        margin-bottom:.65rem; color:#9b92ff; font-size:.62rem; font-weight:800;
        letter-spacing:1.7px; text-transform:uppercase;
    }
    .dl-hero-title {
        margin-bottom:.65rem; color:var(--text); font-size:2.45rem; font-weight:790;
        letter-spacing:-1.55px; line-height:1.08;
    }
    .dl-hero-subtitle {
        max-width:700px; color:var(--muted); font-size:.86rem; line-height:1.7;
    }

    /* ---------- SECTIONS ---------- */
    .dl-section { margin-top:2.8rem; }
    .dl-section-label, .dl-result-label {
        margin-bottom:.7rem; color:var(--subtle); font-size:.59rem; font-weight:800;
        letter-spacing:1.35px; text-transform:uppercase;
    }
    .dl-section-title {
        margin-bottom:.3rem; color:var(--text); font-size:1.35rem; font-weight:730;
        letter-spacing:-.5px;
    }
    .dl-section-description { margin-bottom:1rem; color:var(--muted); font-size:.72rem; line-height:1.55; }
    .dl-result-section { margin-top:1.7rem; }

    /* ---------- UPLOADER ---------- */
    [data-testid="stFileUploader"] {
        margin-top:.75rem; padding:.65rem; border:1px dashed rgba(139,124,255,.32);
        border-radius:13px; background:rgba(15,18,25,.78);
        transition:border-color .2s ease, background .2s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color:rgba(139,124,255,.65); background:rgba(21,25,35,.9);
    }
    [data-testid="stFileUploaderDropzone"] {
        min-height:100px; border-radius:9px; background:var(--surface-2) !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] { gap:.3rem; }
    [data-testid="stFileUploaderDropzoneInstructions"] > div:first-child { font-size:.78rem; font-weight:650; }
    [data-testid="stFileUploaderFile"] { background:var(--surface-3) !important; border:1px solid var(--border) !important; }

    /* ---------- METRICS ---------- */
    .dl-metric {
        min-height:112px; padding:1rem 1.05rem; border:1px solid var(--border);
        border-radius:12px; background:linear-gradient(145deg,var(--surface),rgba(15,18,25,.72));
        box-sizing:border-box; transition:transform .18s ease,border-color .18s ease,background .18s ease;
    }
    .dl-metric:hover { transform:translateY(-1px); border-color:var(--border-strong); background:var(--surface-2); }
    .dl-metric-label { margin-bottom:.4rem; color:var(--subtle); font-size:.58rem; font-weight:800; letter-spacing:1px; }
    .dl-metric-value { color:var(--text); font-size:1.62rem; font-weight:760; letter-spacing:-.7px; }
    .dl-metric-caption { margin-top:.25rem; color:var(--subtle); font-size:.62rem; }

    /* ---------- HEALTH ---------- */
    .dl-health {
        display:flex; align-items:center; gap:.8rem; padding:.9rem 1rem;
        border:1px solid rgba(52,211,153,.16); border-radius:11px; background:rgba(52,211,153,.035);
    }
    .dl-health-dot { width:8px; height:8px; flex-shrink:0; border-radius:50%; background:var(--success); box-shadow:0 0 9px rgba(52,211,153,.55); }
    .dl-health-title { color:#d8fbe9; font-size:.76rem; font-weight:680; }
    .dl-health-description { margin-top:.15rem; color:var(--muted); font-size:.65rem; }

    /* ---------- CARDS ---------- */
    .dl-card, .dl-answer {
        padding:1.15rem 1.2rem; border:1px solid var(--border); border-radius:12px;
        background:linear-gradient(145deg,var(--surface),rgba(15,18,25,.82)); color:#dfe2e9;
        font-size:.82rem; line-height:1.72;
    }
    .dl-point-card, .dl-improvement-card, .dl-insight {
        border:1px solid var(--border); border-radius:10px; background:var(--surface); color:#d8dce5;
        transition:border-color .18s ease,background .18s ease,transform .18s ease;
    }
    .dl-point-card { min-height:72px; margin-bottom:.55rem; padding:.85rem .95rem; font-size:.74rem; line-height:1.58; }
    .dl-point-card:hover, .dl-improvement-card:hover, .dl-insight:hover {
        border-color:var(--border-strong); background:var(--surface-2); transform:translateY(-1px);
    }
    .dl-improvement-card { display:flex; gap:.75rem; min-height:72px; margin-bottom:.55rem; padding:.85rem .95rem; font-size:.74rem; line-height:1.58; }
    .dl-improvement-number {
        display:flex; align-items:center; justify-content:center; flex-shrink:0; width:25px; height:25px;
        border-radius:7px; background:rgba(109,93,252,.12); color:#a9a0ff; font-size:.62rem; font-weight:800;
    }

    /* ---------- INTELLIGENCE ---------- */
    .dl-intel { min-height:92px; padding:1rem; border:1px solid var(--border); border-radius:11px; background:var(--surface); }
    .dl-intel-label { margin-bottom:.4rem; color:var(--subtle); font-size:.58rem; font-weight:800; letter-spacing:.9px; }
    .dl-intel-value { color:var(--text); font-size:.82rem; font-weight:650; line-height:1.45; }
    .dl-theme-list { display:flex; flex-wrap:wrap; gap:.45rem; margin-top:.4rem; }
    .dl-theme { padding:.4rem .65rem; border:1px solid rgba(139,124,255,.18); border-radius:7px; background:rgba(109,93,252,.055); color:#c4bfff; font-size:.64rem; font-weight:620; }
    .dl-takeaway {
        padding:1rem 1.05rem; border:1px solid rgba(139,124,255,.17); border-left:3px solid var(--accent);
        border-radius:9px; background:linear-gradient(90deg,rgba(109,93,252,.09),rgba(109,93,252,.025));
        color:#e1e3ea; font-size:.79rem; line-height:1.65;
    }
    .dl-insight { display:flex; align-items:flex-start; gap:.65rem; margin-bottom:.55rem; padding:.78rem .88rem; font-size:.74rem; line-height:1.55; }
    .dl-insight-arrow { color:var(--accent); font-weight:800; flex-shrink:0; }

    /* ---------- QA ---------- */
    .dl-qa-section { margin-top:3.4rem; }
    .dl-qa-header { display:flex; align-items:center; gap:.65rem; margin-bottom:.35rem; }
    .dl-qa-icon { width:30px; height:30px; display:flex; align-items:center; justify-content:center; border-radius:8px; background:rgba(109,93,252,.12); border:1px solid rgba(139,124,255,.18); color:var(--accent); font-size:.8rem; }
    .dl-qa-title { color:var(--text); font-size:1.35rem; font-weight:730; letter-spacing:-.5px; }
    .dl-qa-description { margin-bottom:1rem; color:var(--muted); font-size:.72rem; line-height:1.5; }
    .dl-question-box { padding:1rem; border:1px solid var(--border); border-radius:12px; background:var(--surface); }
    .dl-question-label { margin-bottom:.45rem; color:var(--subtle); font-size:.59rem; font-weight:800; letter-spacing:.9px; text-transform:uppercase; }
    .dl-answer-header { display:flex; align-items:center; justify-content:space-between; margin-top:1.8rem; margin-bottom:.65rem; }
    .dl-answer-label { color:var(--subtle); font-size:.59rem; font-weight:800; letter-spacing:1px; text-transform:uppercase; }
    .dl-confidence-row { display:flex; align-items:center; gap:.5rem; margin-top:.7rem; }
    .dl-confidence { display:inline-flex; align-items:center; padding:.28rem .55rem; border-radius:6px; font-size:.6rem; font-weight:800; letter-spacing:.35px; text-transform:uppercase; }
    .dl-confidence-high { color:var(--success); border:1px solid rgba(52,211,153,.15); background:rgba(52,211,153,.06); }
    .dl-confidence-medium { color:var(--warning); border:1px solid rgba(251,191,36,.15); background:rgba(251,191,36,.06); }
    .dl-confidence-low { color:var(--danger); border:1px solid rgba(251,113,133,.15); background:rgba(251,113,133,.06); }
    .dl-evidence-section { margin-top:1.7rem; }
    .dl-evidence-header { display:flex; align-items:center; gap:.55rem; margin-bottom:.75rem; }
    .dl-evidence-title { color:var(--text); font-size:.9rem; font-weight:680; }
    .dl-evidence-count { padding:.2rem .45rem; border-radius:5px; background:rgba(109,93,252,.1); color:var(--accent); font-size:.58rem; font-weight:800; }
    .dl-evidence { margin-bottom:.65rem; padding:.95rem 1rem; border:1px solid rgba(139,124,255,.14); border-radius:10px; background:rgba(109,93,252,.025); }
    .dl-evidence-page { margin-bottom:.42rem; color:#a9a0ff; font-size:.59rem; font-weight:800; letter-spacing:.9px; text-transform:uppercase; }
    .dl-evidence-quote { padding-left:.8rem; border-left:2px solid rgba(139,124,255,.38); color:#cbd0da; font-size:.74rem; line-height:1.62; }

    /* ---------- EMPTY / DOCUMENT CONTENT ---------- */
    .dl-empty { margin-top:2rem; padding:3rem 2rem; text-align:center; border:1px solid var(--border); border-radius:13px; background:linear-gradient(145deg,var(--surface),rgba(15,18,25,.72)); }
    .dl-empty-icon { width:44px; height:44px; margin:0 auto 1rem; display:flex; align-items:center; justify-content:center; border-radius:12px; background:rgba(109,93,252,.12); border:1px solid rgba(139,124,255,.2); color:#aaa1ff; font-size:1rem; }
    .dl-empty-title { margin-bottom:.35rem; color:var(--text); font-size:.95rem; font-weight:680; }
    .dl-empty-description { max-width:420px; margin:auto; color:var(--muted); font-size:.7rem; line-height:1.55; }
    .dl-document-shell { padding:1rem; border:1px solid var(--border); border-radius:12px; background:var(--surface); }
    .dl-document-meta { display:flex; justify-content:space-between; gap:1rem; margin-bottom:.8rem; color:var(--subtle); font-size:.62rem; }
    .dl-document-meta strong { color:#cbd0da; font-weight:650; }

    /* ---------- CONTROLS ---------- */
    .stButton > button { min-height:2.4rem; border-radius:8px !important; font-weight:650 !important; border:1px solid var(--border) !important; }
    .stButton > button[kind="primary"] { box-shadow:0 7px 22px rgba(109,93,252,.16); }
    div[data-baseweb="input"] { border-radius:9px; }
    div[data-baseweb="input"] > div { background:var(--surface-2); border-color:var(--border); }
    div[data-testid="stRadio"] [role="radiogroup"] { gap:.4rem; }
    div[data-testid="stRadio"] label { padding:.32rem .55rem; border:1px solid var(--border); border-radius:7px; background:var(--surface); }
    div[data-testid="stRadio"] label:has(input:checked) { border-color:rgba(139,124,255,.4); background:rgba(109,93,252,.1); }
    [data-testid="stExpander"] { border:1px solid var(--border); border-radius:10px; background:var(--surface); }
    .stTextArea textarea { background:var(--surface-2) !important; border:1px solid var(--border) !important; color:#dfe2e9 !important; border-radius:9px !important; font-family:ui-monospace,SFMono-Regular,Consolas,monospace !important; font-size:.73rem !important; line-height:1.65 !important; }
    .stSelectbox [data-baseweb="select"] > div { background:var(--surface-2); border-color:var(--border); border-radius:8px; }
    div[data-testid="stVerticalBlock"] { gap:.55rem; }

    /* ---------- FOOTER ---------- */
    .dl-footer { margin-top:4rem; padding-top:1.2rem; border-top:1px solid var(--border); text-align:center; color:var(--subtle); font-size:.6rem; }

    /* ---------- RESPONSIVE ---------- */
    @media (max-width: 800px) {
        .block-container { padding-left:1rem; padding-right:1rem; }
        .dl-hero-title { font-size:2rem; }
        .dl-nav { margin-bottom:2.2rem; }
        .dl-status { display:none; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# TOP NAVIGATION
# =========================================================

render_html(
    """
    <div class="dl-nav">

        <div class="dl-brand">

            <div class="dl-logo">
                D
            </div>

            <div>
                <div class="dl-brand-name">
                    DocLens
                </div>

                <div class="dl-brand-caption">
                    Document Intelligence
                </div>
            </div>

        </div>

        <div class="dl-status">
            <span class="dl-status-dot"></span>
            System Ready
        </div>

    </div>
    """
)


# =========================================================
# HERO
# =========================================================

render_html(
    """
    <div>

        <div class="dl-eyebrow">
            AI DOCUMENT WORKSPACE
        </div>

        <div class="dl-hero-title">
            Understand documents at a glance.
        </div>

        <div class="dl-hero-subtitle">
            Extract, analyze and interrogate complex
            documents with AI-powered intelligence
            grounded in the source material.
        </div>

    </div>
    """
)


# =========================================================
# UPLOAD SECTION
# =========================================================

render_html(
    """
    <div class="dl-section">

        <div class="dl-section-label">
            Document Workspace
        </div>

        <div class="dl-section-title">
            Upload a document
        </div>

        <div class="dl-section-description">
            PDF, scanned PDF, PNG, JPG and JPEG files are supported.
        </div>

    </div>
    """
)


uploaded_file = st.file_uploader(
    "Upload a document",
    type=[
        "pdf",
        "png",
        "jpg",
        "jpeg",
    ],
    help=(
        "Upload a PDF, scanned PDF, PNG, JPG "
        "or JPEG document."
    ),
)


# =========================================================
# DOCUMENT PROCESSING
# =========================================================

if uploaded_file is not None:

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

            reset_document_state()

        except Exception as error:

            st.error(
                "Something went wrong while processing "
                "the document."
            )

            st.exception(error)

            reset_document_state()


# =========================================================
# DOCUMENT
# =========================================================

document = st.session_state.document


if document is None:

    render_html(
        """
        <div class="dl-empty">

            <div class="dl-empty-icon">D</div>

            <div class="dl-empty-title">
                Your workspace is ready
            </div>

            <div class="dl-empty-description">
                Upload a document to extract its contents, generate structured intelligence, and ask grounded questions with DocLens.
            </div>

        </div>
        """
    )

    st.stop()


# =========================================================
# DOCUMENT OVERVIEW
# =========================================================

render_html(
    """
    <div class="dl-section">

        <div class="dl-section-label">
            Document Overview
        </div>

    </div>
    """
)


render_html(
    f"""
    <div class="dl-file">

        <span class="dl-file-icon">▣</span>

        <span>
            {document['filename']}
        </span>

        <span>•</span>

        <span>
            {document['file_type'].upper()}
        </span>

    </div>
    """
)


# =========================================================
# METRICS
# =========================================================

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

col1, col2, col3, col4 = st.columns(4)


with col1:

    render_html(
        f"""
        <div class="dl-metric">

            <div class="dl-metric-label">
                PAGES
            </div>

            <div class="dl-metric-value">
                {document['page_count']}
            </div>

            <div class="dl-metric-caption">
                Document length
            </div>

        </div>
        """
    )


with col2:

    render_html(
        f"""
        <div class="dl-metric">

            <div class="dl-metric-label">
                WORDS
            </div>

            <div class="dl-metric-value">
                {document['word_count']:,}
            </div>

            <div class="dl-metric-caption">
                Extracted words
            </div>

        </div>
        """
    )


with col3:

    render_html(
        f"""
        <div class="dl-metric">

            <div class="dl-metric-label">
                CHARACTERS
            </div>

            <div class="dl-metric-value">
                {document['character_count']:,}
            </div>

            <div class="dl-metric-caption">
                Extracted characters
            </div>

        </div>
        """
    )


with col4:

    render_html(
        f"""
        <div class="dl-metric">

            <div class="dl-metric-label">
                TEXT COVERAGE
            </div>

            <div class="dl-metric-value">
                {page_coverage:.0f}%
            </div>

            <div class="dl-metric-caption">
                Pages with extracted text
            </div>

        </div>
        """
    )


# =========================================================
# DOCUMENT HEALTH
# =========================================================

render_html(
    """
    <div class="dl-section">

        <div class="dl-section-label">
            Document Health
        </div>

    </div>
    """
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


render_html(
    f"""
    <div class="dl-health">

        <div class="dl-health-dot"></div>

        <div>

            <div class="dl-health-title">
                Extraction status: {health_label}
            </div>

            <div class="dl-health-description">
                {non_empty_pages} of {document['page_count']}
                pages contain extracted text
                · Average {average_words:.0f}
                words per page
            </div>

        </div>

    </div>
    """
)


# =========================================================
# AI ANALYSIS
# =========================================================

render_html(
    """
    <div class="dl-section">

        <div class="dl-section-title">
            AI Analysis
        </div>

        <div class="dl-section-description">
            Generate structured intelligence from the uploaded document.
        </div>

    </div>
    """
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


if analyze_button:

    document_text = "\n\n".join(
        page["text"]
        for page in document["pages"]
        if page["text"]
    )

    if not document_text.strip():

        st.warning(
            "No text could be extracted from this document."
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

            if "429" in str(error):

                st.warning(
                    "AI usage limit reached. "
                    "Please try again after the Gemini quota resets."
                )

            else:

                st.error(
                    "Something went wrong while generating "
                    "the analysis."
                )


# =========================================================
# ANALYSIS RESULT
# =========================================================

analysis = st.session_state.analysis


if analysis is not None:

    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    render_html(
        """
        <div class="dl-result-section">

            <div class="dl-section-title">
                Summary
            </div>

        </div>
        """
    )

    render_html(
        f"""
        <div class="dl-card">
            {analysis['summary']}
        </div>
        """
    )


    # -----------------------------------------------------
    # KEY POINTS + IMPROVEMENTS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        render_html(
            """
            <div class="dl-result-section">

                <div class="dl-result-label">
                    Key Points
                </div>

            </div>
            """
        )

        for point in analysis["key_points"]:

            render_html(
                f"""
                <div class="dl-point-card">
                    {point}
                </div>
                """
            )


    with col2:

        render_html(
            """
            <div class="dl-result-section">

                <div class="dl-result-label">
                    Improvement Suggestions
                </div>

            </div>
            """
        )

        for index, suggestion in enumerate(
            analysis["improvement_suggestions"],
            start=1,
        ):

            render_html(
                f"""
                <div class="dl-improvement-card">

                    <div class="dl-improvement-number">
                        {index:02d}
                    </div>

                    <div>
                        {suggestion}
                    </div>

                </div>
                """
            )


    # -----------------------------------------------------
    # DOCUMENT INTELLIGENCE
    # -----------------------------------------------------

    intelligence = analysis[
        "document_intelligence"
    ]


    render_html(
        """
        <div class="dl-result-section">

            <div class="dl-section-title">
                Document Intelligence
            </div>

            <div class="dl-section-description">
                Higher-level understanding derived from the document.
            </div>

        </div>
        """
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        render_html(
            f"""
            <div class="dl-intel">

                <div class="dl-intel-label">
                    DOCUMENT TYPE
                </div>

                <div class="dl-intel-value">
                    {intelligence['document_type']}
                </div>

            </div>
            """
        )


    with col2:

        render_html(
            f"""
            <div class="dl-intel">

                <div class="dl-intel-label">
                    PRIMARY TOPIC
                </div>

                <div class="dl-intel-value">
                    {intelligence['primary_topic']}
                </div>

            </div>
            """
        )


    with col3:

        render_html(
            f"""
            <div class="dl-intel">

                <div class="dl-intel-label">
                    COMPLEXITY
                </div>

                <div class="dl-intel-value">
                    {intelligence['complexity']}
                </div>

            </div>
            """
        )


    # -----------------------------------------------------
    # MAIN THEMES
    # -----------------------------------------------------

    render_html(
        """
        <div class="dl-result-section">

            <div class="dl-result-label">
                Main Themes
            </div>

            <div class="dl-theme-list">
        """
        +
        "".join(
            f"""
            <div class="dl-theme">
                {theme}
            </div>
            """
            for theme in intelligence["main_themes"]
        )
        +
        """
            </div>

        </div>
        """
    )


    # -----------------------------------------------------
    # KEY TAKEAWAY
    # -----------------------------------------------------

    render_html(
        """
        <div class="dl-result-section">

            <div class="dl-result-label">
                Key Takeaway
            </div>

        </div>
        """
    )


    render_html(
        f"""
        <div class="dl-takeaway">
            {intelligence['key_takeaway']}
        </div>
        """
    )


    # -----------------------------------------------------
    # ACTIONABLE INSIGHTS
    # -----------------------------------------------------

    render_html(
        """
        <div class="dl-result-section">

            <div class="dl-result-label">
                Actionable Insights
            </div>

        </div>
        """
    )


    for insight in intelligence[
        "actionable_insights"
    ]:

        render_html(
            f"""
            <div class="dl-insight">

                <div class="dl-insight-arrow">
                    →
                </div>

                <div>
                    {insight}
                </div>

            </div>
            """
        )

# =========================================================
# ASK DOCLENS
# =========================================================

render_html(
    """
    <div class="dl-section">

        <div class="dl-section-title">
            Ask DocLens
        </div>

        <div class="dl-section-description">
            Ask questions grounded only in the uploaded document.
        </div>

    </div>
    """
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

            if "429" in str(error):

                st.warning(
                    "AI usage limit reached. "
                    "Please try again after the Gemini quota resets."
                )

            else:

                st.error(
                    "Something went wrong while answering "
                    "the question."
                )


# =========================================================
# QA RESULT
# =========================================================

qa_answer = st.session_state.qa_answer


if qa_answer is not None:

    render_html(
        """
        <div class="dl-section">

            <div class="dl-section-label">
                Answer
            </div>

        </div>
        """
    )


    render_html(
        f"""
        <div class="dl-answer">

            {qa_answer['answer']}

        </div>
        """
    )


    confidence = qa_answer[
        "confidence"
    ]


    if confidence == "High":

        confidence_class = (
            "dl-confidence dl-confidence-high"
        )

    elif confidence == "Medium":

        confidence_class = (
            "dl-confidence dl-confidence-medium"
        )

    else:

        confidence_class = (
            "dl-confidence dl-confidence-low"
        )


    render_html(
        f"""
        <span class="{confidence_class}">
            Confidence: {confidence}
        </span>
        """
    )


    # =====================================================
    # EVIDENCE
    # =====================================================

    sources = qa_answer.get(
        "sources",
        [],
    )


    if sources:

        render_html(
            """
            <div class="dl-section">

                <div class="dl-section-label">
                    Verified Evidence
                </div>

            </div>
            """
        )


        for source in sources:

            page_number = source["page"]
            quote = source["quote"]


            render_html(
                f"""
                <div class="dl-evidence">

                    <div class="dl-evidence-page">
                        Page {page_number}
                    </div>

                    <div class="dl-evidence-quote">
                        “{quote}”
                    </div>

                </div>
                """
            )


    else:

        st.info(
            "This answer is not supported by the uploaded document."
        )


# =========================================================
# DOCUMENT CONTENT
# =========================================================

render_html(
    """
    <div class="dl-section">

        <div class="dl-section-label">
            Document Content
        </div>

        <div class="dl-section-title">
            Extracted document
        </div>

        <div class="dl-section-description">
            Review the text extracted from the uploaded document, page by page.
        </div>

    </div>
    """
)

page_numbers = [
    page["page_number"]
    for page in document["pages"]
]

content_col1, content_col2 = st.columns([1, 3])

with content_col1:
    selected_page = st.selectbox(
        "Page",
        page_numbers,
        format_func=lambda page: f"Page {page}",
    )

selected_page_data = next(
    page
    for page in document["pages"]
    if page["page_number"] == selected_page
)

page_text = selected_page_data.get("text", "")
page_words = len(page_text.split()) if page_text else 0
page_chars = len(page_text) if page_text else 0

with content_col2:
    render_html(
        f"""
        <div class="dl-document-meta">
            <span><strong>PAGE {selected_page}</strong></span>
            <span>{page_words:,} words &nbsp; · &nbsp; {page_chars:,} characters</span>
        </div>
        """
    )

if page_text:
    st.text_area(
        "Extracted text",
        value=page_text,
        height=430,
        disabled=True,
        label_visibility="collapsed",
    )
else:
    st.warning("No text detected on this page.")

render_html(
    """
    <div class="dl-footer">
        DocLens · Document Intelligence · Grounded AI analysis
    </div>
    """
)
