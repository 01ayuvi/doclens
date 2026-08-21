# 📄 DocLens

### AI Document Intelligence Assistant

DocLens is an AI-powered document intelligence assistant that turns PDFs, scanned documents, and images into structured summaries, document insights, and grounded answers with source-aware evidence.

Instead of simply generating a summary, DocLens combines document extraction, OCR, AI analysis, and document-grounded question answering to help users understand complex documents faster.

---

## ✨ Features

### 📄 Multi-format Document Processing

DocLens supports:

- PDF documents
- Scanned PDFs
- PNG images
- JPG images
- JPEG images

The system automatically determines the appropriate extraction pipeline.

---

### 🔍 Page-level Text Extraction

Documents are processed while preserving page-level context.

For every page, DocLens maintains:

- Page number
- Extracted text
- Word count
- Character count

This allows downstream AI responses to remain connected to the original document structure.

---

### 👁️ OCR for Scanned Documents

For image-based documents and scanned PDFs, DocLens uses Optical Character Recognition (OCR) to extract readable text.

This allows the system to process documents that do not contain selectable PDF text.

---

### 📝 AI Document Summarization

DocLens can generate summaries with selectable lengths:

- Short
- Medium
- Long

The analysis also provides:

- Key points
- Improvement suggestions
- Main themes
- Key takeaway
- Actionable insights

---

### 🧠 Document Intelligence

DocLens goes beyond traditional summarization by extracting higher-level document intelligence.

The system identifies:

- Document type
- Primary topic
- Complexity
- Main themes
- Key takeaway
- Actionable insights

This provides a structured understanding of the document rather than only returning a block of generated text.

---

### 💬 Ask DocLens

Users can ask questions directly about an uploaded document.

The Q&A system is designed to answer using the uploaded document context rather than relying on unrelated external knowledge.

Example:

> How are code-signing certificates abused by attackers?

DocLens returns:

- Answer
- Confidence level
- Supporting source information

If the document does not contain enough information, DocLens is designed to indicate that the answer is not supported by the document.

---

### 📚 Document Evidence

DocLens maintains document-level context and supports source-aware answers.

Supporting evidence can be associated with specific document pages, allowing users to understand where an answer originated.

---

### 📊 Document Health

Before analysis, DocLens provides document processing information including:

- Number of pages
- Extracted words
- Extracted characters
- Text coverage
- Extraction status

This gives users visibility into the quality of the document processing pipeline.

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │     User Document    │
                    │ PDF / Scan / Image   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Document Processor   │
                    └──────────┬───────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼                         ▼
        ┌─────────────────┐       ┌─────────────────┐
        │ PDF Extraction  │       │       OCR       │
        │   PyMuPDF       │       │   Tesseract     │
        └────────┬────────┘       └────────┬────────┘
                 │                         │
                 └────────────┬────────────┘
                              ▼
                   ┌─────────────────────┐
                   │ Page-level Content  │
                   │ Text + Metadata     │
                   └──────────┬──────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
       ┌──────────────────┐      ┌──────────────────┐
       │  AI Analyzer     │      │   Ask DocLens    │
       │                  │      │                  │
       │ Summary          │      │ Question         │
       │ Key Points       │      │ Answer           │
       │ Intelligence     │      │ Confidence       │
       │ Insights         │      │ Evidence         │
       └────────┬─────────┘      └────────┬─────────┘
                │                         │
                └────────────┬────────────┘
                             ▼
                   ┌─────────────────────┐
                   │    Streamlit UI     │
                   │                     │
                   │ Dashboard           │
                   │ Analysis            │
                   │ Q&A                 │
                   │ Document Viewer     │
                   └─────────────────────┘
---
## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| UI | Streamlit |
| PDF Processing | PyMuPDF |
| OCR | Tesseract + Pytesseract |
| Generative AI | Google Gemini API |
| Configuration | python-dotenv |
| Version Control | Git + GitHub |
---

## ⚙️ How It Works

```text
Upload Document
      ↓
PDF Extraction / OCR
      ↓
Page-level Text + Metadata
      ↓
AI Analysis
      ↓
Summary + Document Intelligence
      ↓
Ask DocLens
      ↓
Grounded Answer + Evidence