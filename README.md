# 🎓 Academic Research Assistant

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://research-assistant-ahu4swtfbdnpkb4kruhenr.streamlit.app/)

> **Live Demo:** https://research-assistant-ahu4swtfbdnpkb4kruhenr.streamlit.app/

An AI-powered academic research assistant built with **GROQ API** and **Streamlit**. Synthesizes information from multiple sources, generates citations, and produces structured academic reports.

---

## ✨ Features

- 🔍 **Multi-source Research** — Searches academic papers across 5 knowledge domains
- 📊 **Paper Relevance Scoring** — Filters and ranks papers by relevance
- 📝 **4 Report Formats** — Structured Report, Literature Review, Executive Summary, Annotated Bibliography
- 🔖 **Citation Management** — APA, MLA, and Chicago citation styles
- 📚 **Sources Library** — Filter by year, citations, and relevance
- 💬 **Conversational Interface** — Multi-turn research chat with memory

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| LLM | llama-3.3-70b-versatile (GROQ) |
| API | GROQ REST API via requests |
| Deployment | Streamlit Cloud |

---

## 🚀 Run Locally

```bash
git clone https://github.com/YoussefK-Ismail/research-assistant.git
cd research-assistant
pip install streamlit
streamlit run app.py
```

Enter your GROQ API Key in the sidebar to start.

---

## 🧪 Example Queries

| Query | Feature Tested |
|-------|---------------|
| `What are the latest breakthroughs in quantum computing?` | Paper search + synthesis |
| `How is AI being used in climate change research?` | Multi-source analysis |
| `Find papers about transformer models and generate APA citations` | Citation generation |
| Generate Report → `Large Language Models in Education` | Full report generation |

---

## 📐 Architecture

```
User Query
    │
    ▼
search_papers() ──► Mock Knowledge Base (5 domains)
    │
    ▼
get_developments() ──► Recent Trends Database
    │
    ▼
GROQ API (llama-3.3-70b-versatile)
    │
    ▼
Structured Academic Response
    │
    ├── Research Chat Tab
    ├── Generate Report Tab (4 formats)
    └── Sources Library Tab
```

---

## 📋 Assignment Requirements

- [x] Implementation of at least two research tools/sources
- [x] Information synthesis using appropriate chain types
- [x] Structured report generation with configurable formats
- [x] Source tracking and citation management
- [x] Filtering mechanism for information relevance

---

## 👨‍💻 Author

**Youssef Khaled Ismail**  
Project 8 — Academic Research Assistant  
Advanced LangChain Applications Assignment
