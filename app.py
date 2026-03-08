"""
Academic Research Assistant
Built with LangChain + GROQ + Streamlit
Project 8 - Youssef Khaled Ismail
"""

import streamlit as st
import json
from datetime import datetime
from typing import List, Dict

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

st.set_page_config(
    page_title="Academic Research Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .research-header {
        background: linear-gradient(135deg, #1a237e 0%, #7b1fa2 100%);
        padding: 20px 30px; border-radius: 12px; color: white; margin-bottom: 20px;
    }
    .source-card { background: #f3e5f5; border-left: 4px solid #7b1fa2; padding: 12px 16px; border-radius: 8px; margin: 6px 0; }
    .relevance-high   { border-left-color: #4CAF50; background: #e8f5e9; }
    .relevance-medium { border-left-color: #FF9800; background: #fff8e1; }
    .relevance-low    { border-left-color: #f44336; background: #ffebee; }
</style>
""", unsafe_allow_html=True)

MOCK_PAPERS = {
    "machine learning": [
        {"title": "Attention Is All You Need", "authors": "Vaswani et al.", "year": 2017, "journal": "NeurIPS",
         "abstract": "We propose the Transformer, a model architecture based solely on attention mechanisms. Experiments show these models are superior in quality while being more parallelizable and requiring significantly less time to train.",
         "citations": 90000, "doi": "10.48550/arXiv.1706.03762", "relevance": 0.95},
        {"title": "BERT: Pre-training of Deep Bidirectional Transformers", "authors": "Devlin et al.", "year": 2018, "journal": "NAACL",
         "abstract": "We introduce BERT, designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context.",
         "citations": 75000, "doi": "10.48550/arXiv.1810.04805", "relevance": 0.88},
        {"title": "Deep Residual Learning for Image Recognition", "authors": "He et al.", "year": 2016, "journal": "CVPR",
         "abstract": "We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously.",
         "citations": 120000, "doi": "10.1109/CVPR.2016.90", "relevance": 0.82},
    ],
    "climate change": [
        {"title": "Global Warming of 1.5 Degrees - IPCC Special Report", "authors": "IPCC Working Group I", "year": 2018, "journal": "IPCC",
         "abstract": "An IPCC special report on the impacts of global warming of 1.5 degrees above pre-industrial levels and related global greenhouse gas emission pathways.",
         "citations": 25000, "doi": "10.1017/9781009157940", "relevance": 0.97},
        {"title": "Ocean Acidification and its Effects on Marine Ecosystems", "authors": "Orr et al.", "year": 2020, "journal": "Nature Climate Change",
         "abstract": "This review synthesizes evidence for the impacts of ocean acidification on marine organisms and ecosystems.",
         "citations": 4500, "doi": "10.1038/s41558-020-0869-0", "relevance": 0.85},
    ],
    "quantum computing": [
        {"title": "Quantum supremacy using a programmable superconducting processor", "authors": "Arute et al. (Google AI)", "year": 2019, "journal": "Nature",
         "abstract": "We developed a quantum processor using 53 programmable superconducting qubits that performed a target computation in 200 seconds.",
         "citations": 6000, "doi": "10.1038/s41586-019-1666-5", "relevance": 0.96},
        {"title": "Quantum Error Correction: An Introductory Guide", "authors": "Devitt et al.", "year": 2023, "journal": "Contemporary Physics",
         "abstract": "We review quantum error correction from threshold theorems and stabilizer codes to topological methods and fault-tolerant computation.",
         "citations": 2100, "doi": "10.1080/00107514.2013.810887", "relevance": 0.89},
    ],
    "artificial intelligence": [
        {"title": "Human-Level Control through Deep Reinforcement Learning", "authors": "Mnih et al. (DeepMind)", "year": 2015, "journal": "Nature",
         "abstract": "We present a model-free reinforcement learning algorithm that combines deep neural networks with Q-learning.",
         "citations": 18000, "doi": "10.1038/nature14236", "relevance": 0.91},
        {"title": "GPT-4 Technical Report", "authors": "OpenAI", "year": 2023, "journal": "arXiv",
         "abstract": "We report the development of GPT-4, a large multimodal model exhibiting human-level performance on various professional benchmarks.",
         "citations": 9000, "doi": "10.48550/arXiv.2303.08774", "relevance": 0.93},
    ],
    "blockchain": [
        {"title": "Bitcoin: A Peer-to-Peer Electronic Cash System", "authors": "Nakamoto, S.", "year": 2008, "journal": "White Paper",
         "abstract": "A purely peer-to-peer version of electronic cash allowing online payments without going through a financial institution.",
         "citations": 20000, "doi": "https://bitcoin.org/bitcoin.pdf", "relevance": 0.99},
    ],
}


def search_papers(query: str) -> List[Dict]:
    query_lower = query.lower()
    results = []
    for topic, papers in MOCK_PAPERS.items():
        if any(word in query_lower for word in topic.split()):
            results.extend(papers)
    if not results:
        results = MOCK_PAPERS.get("artificial intelligence", []) + MOCK_PAPERS.get("machine learning", [])[:1]
    seen, unique = set(), []
    for p in results:
        if p["title"] not in seen:
            seen.add(p["title"])
            unique.append(p)
    return unique[:5]


@tool
def search_academic_papers(query: str) -> str:
    """Search for academic papers and research articles on a given topic."""
    papers = search_papers(query)
    if not papers:
        return json.dumps({"message": "No papers found", "results": []})
    return json.dumps({"query": query, "total": len(papers), "papers": papers})


@tool
def search_recent_developments(topic: str) -> str:
    """Search for recent developments, trends, and breakthroughs in a research field."""
    developments = {
        "machine learning": "Recent: (1) GPT-4 achieving human-level performance. (2) Mixture-of-Experts reducing costs. (3) Constitutional AI for alignment. (4) LoRA enabling efficient fine-tuning.",
        "quantum computing": "Recent: (1) IBM 1000+ qubit processors. (2) Google quantum error correction below threshold. (3) Microsoft topological qubits.",
        "climate change": "Recent: (1) 2023 hottest year on record. (2) Arctic sea ice at historic minimum. (3) Carbon capture costs dropping 40%.",
        "artificial intelligence": "Recent: (1) Foundation models as general-purpose engines. (2) AI agents performing complex tasks. (3) Multimodal AI integrating vision and language.",
        "blockchain": "Recent: (1) Ethereum proof-of-stake reducing energy by 99.9%. (2) Layer-2 scaling achieving 100k+ TPS. (3) ZK-proofs enabling private transactions.",
    }
    topic_lower = topic.lower()
    for key, dev in developments.items():
        if key in topic_lower or any(word in topic_lower for word in key.split()):
            return json.dumps({"topic": topic, "developments": dev, "date": datetime.now().strftime("%B %Y")})
    return json.dumps({"topic": topic, "developments": "Active research field with significant 2023-2024 publications.", "date": datetime.now().strftime("%B %Y")})


@tool
def generate_citation(paper_title: str, authors: str, year: int, journal: str, doi: str = "") -> str:
    """Generate properly formatted citations in APA, MLA, and Chicago style."""
    apa     = f"{authors} ({year}). {paper_title}. {journal}. {f'https://doi.org/{doi}' if doi else ''}"
    mla     = f"{authors}. \"{paper_title}.\" {journal}, {year}. {f'DOI: {doi}' if doi else ''}"
    chicago = f"{authors}. \"{paper_title}.\" {journal} ({year}). {f'https://doi.org/{doi}' if doi else ''}"
    return json.dumps({"apa": apa, "mla": mla, "chicago": chicago})


@tool
def assess_paper_relevance(paper_abstract: str, research_question: str) -> str:
    """Assess how relevant a paper is to a specific research question."""
    stop = {'the','a','an','and','or','but','in','on','at','to','for','of','with','by','from',
            'is','are','was','were','be','been','how','what','why','when','where','which'}
    abstract_words = set(paper_abstract.lower().split())
    question_words = set(research_question.lower().split()) - stop
    overlap = abstract_words & question_words
    score   = min(len(overlap) / max(len(question_words), 1) * 100, 100)
    if score >= 60:
        level = "High"; rec = "Strongly recommended - directly relevant to your research question"
    elif score >= 30:
        level = "Medium"; rec = "Moderately relevant - covers related concepts"
    else:
        level = "Low"; rec = "Tangentially related - may provide background context only"
    return json.dumps({"relevance_score": round(score, 1), "level": level,
                       "recommendation": rec, "matching_concepts": list(overlap)[:10]})


TOOLS = [search_academic_papers, search_recent_developments, generate_citation, assess_paper_relevance]


def init_session():
    defaults = {
        "chat_history": [], "messages": [], "research_sessions": [],
        "current_sources": [], "generated_reports": [],
        "total_papers": 0, "agent_history": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def get_research_response(api_key: str, query: str, history: list, report_format: str, depth: str) -> str:
    # Run tools directly to gather data
    papers_raw = search_academic_papers.invoke({"query": query})
    papers_data = json.loads(papers_raw)

    developments_raw = search_recent_developments.invoke({"topic": query})
    dev_data = json.loads(developments_raw)

    # Build context from tool results
    context = "=== Academic Papers Found ===\n"
    for p in papers_data.get("papers", []):
        context += f"- {p['title']} by {p['authors']} ({p['year']}) in {p['journal']}\n"
        context += f"  Abstract: {p['abstract'][:200]}...\n"
        context += f"  Citations: {p.get('citations',0):,} | DOI: {p.get('doi','')}\n\n"
    context += f"\n=== Recent Developments ===\n{dev_data.get('developments','')}\n"

    llm = ChatGroq(api_key=api_key, model="llama-3.3-70b-versatile", temperature=0.3)

    system_text = (
        f"You are an expert Academic Research Assistant.\n"
        f"Report Format: {report_format} | Research Depth: {depth}\n"
        f"Current date: {datetime.now().strftime('%B %d, %Y')}\n\n"
        f"Instructions:\n"
        f"1. Use the provided research data to answer comprehensively\n"
        f"2. Cite sources using [Author Year] format\n"
        f"3. Present conflicting findings objectively\n"
        f"4. Suggest research gaps and future directions\n\n"
        f"RESEARCH DATA:\n{context}"
    )

    messages = [SystemMessage(content=system_text)] + list(history[-6:]) + [HumanMessage(content=query)]
    result = llm.invoke(messages)
    return result.content


def generate_full_report(api_key: str, topic: str, papers: List[Dict], report_format: str) -> str:
    llm = ChatGroq(api_key=api_key, model="llama-3.3-70b-versatile", temperature=0.2)
    sources_text = ""
    for i, p in enumerate(papers[:5], 1):
        sources_text += f"\n[{i}] {p.get('title','')} - {p.get('authors','')} ({p.get('year','')})\nAbstract: {p.get('abstract','')[:300]}...\n"

    format_map = {
        "Structured Report":      "Create a full academic report with: Title, Abstract, Introduction, Background, Key Findings, Analysis, Implications, Conclusion, References",
        "Literature Review":      "Create a literature review with: Introduction, Thematic Analysis, Historical Context, Current State, Research Gaps, Future Directions, References",
        "Executive Summary":      "Create an executive summary with: Overview, Top 5 Key Findings, Practical Implications, Recommended Actions, Sources",
        "Annotated Bibliography": "Create an annotated bibliography: intro paragraph, then for each source: full citation + 3-4 sentence annotation",
    }

    prompt = f"""Generate a comprehensive {report_format} on: "{topic}"

Sources:
{sources_text}

Instructions: {format_map.get(report_format, 'Write a well-structured academic document')}

Requirements:
- Use [Author Year] citation format
- Be specific and evidence-based
- Minimum 600 words
- Use markdown formatting with headers and structure
"""
    return llm.invoke(prompt).content


def main():
    init_session()

    st.markdown("""<div class="research-header">
        <h1>🎓 Academic Research Assistant</h1>
        <p style="margin:0;opacity:0.9">AI-powered research synthesis · Citation management · Multi-source analysis</p>
    </div>""", unsafe_allow_html=True)

    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input("GROQ API Key", type="password", placeholder="gsk_...")
        st.divider()
        st.subheader("📋 Report Settings")
        report_format  = st.selectbox("Report Format",  ["Structured Report", "Literature Review", "Executive Summary", "Annotated Bibliography"])
        research_depth = st.selectbox("Research Depth", ["Comprehensive", "Overview", "Deep Dive"])
        st.divider()
        st.subheader("📊 Session Stats")
        c1, c2 = st.columns(2)
        c1.metric("Searches", len(st.session_state.research_sessions))
        c2.metric("Papers",   st.session_state.total_papers)
        st.divider()
        st.subheader("💡 Quick Topics")
        for t in ["Machine learning in healthcare", "Climate change solutions",
                  "Quantum computing applications", "AI ethics and bias", "Blockchain in supply chain"]:
            if st.button(f"🔬 {t}", key=t, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": f"Research topic: {t}"})
                st.rerun()
        if st.button("🗑️ Clear Session", use_container_width=True):
            for k in ["messages", "chat_history", "current_sources", "agent_history", "research_sessions"]:
                st.session_state[k] = []
            st.rerun()

    tab1, tab2, tab3 = st.tabs(["🔍 Research Chat", "📄 Generate Report", "📚 Sources Library"])

    with tab1:
        st.subheader("Ask Your Research Question")
        if not st.session_state.messages:
            st.markdown("""<div style="text-align:center;padding:30px;color:#888;">
                <h3>🔬 Start Your Research</h3>
                <p>Ask me about any academic topic. I'll find papers, synthesize findings, and cite sources.</p>
            </div>""", unsafe_allow_html=True)

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="👨‍🎓" if msg["role"] == "user" else "🎓"):
                st.markdown(msg["content"])

        query = st.chat_input("Ask a research question...")
        if query:
            if not api_key:
                st.error("Please enter your GROQ API Key in the sidebar.")
            else:
                st.session_state.messages.append({"role": "user", "content": query})
                with st.chat_message("user", avatar="👨‍🎓"):
                    st.markdown(query)
                with st.chat_message("assistant", avatar="🎓"):
                    with st.spinner("🔍 Searching databases and synthesizing research..."):
                        try:
                            response = get_research_response(api_key, query, st.session_state.agent_history, report_format, research_depth)
                            papers = search_papers(query)
                            if papers:
                                st.session_state.current_sources.extend(papers)
                                st.session_state.current_sources = list({p['title']: p for p in st.session_state.current_sources}.values())
                                st.session_state.total_papers += len(papers)
                            st.markdown(response)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            st.session_state.research_sessions.append(query)
                            st.session_state.agent_history.append(HumanMessage(content=query))
                            st.session_state.agent_history.append(AIMessage(content=response))
                            if len(st.session_state.agent_history) > 16:
                                st.session_state.agent_history = st.session_state.agent_history[-16:]
                            if papers:
                                with st.expander(f"📊 Found {len(papers)} relevant papers"):
                                    for p in papers[:3]:
                                        rel = p.get("relevance", 0.5)
                                        rel_class = "relevance-high" if rel >= 0.85 else "relevance-medium" if rel >= 0.7 else "relevance-low"
                                        st.markdown(f"""<div class="source-card {rel_class}">
                                            <b>{p['title']}</b> - {p['authors']} ({p['year']})<br>
                                            <small>📰 {p['journal']} | 🔢 {p['citations']:,} citations | Relevance: {rel*100:.0f}%</small>
                                        </div>""", unsafe_allow_html=True)
                        except Exception as e:
                            err = f"Error: {str(e)}"
                            st.error(err)
                            st.session_state.messages.append({"role": "assistant", "content": err})

    with tab2:
        st.subheader(f"📄 Generate {report_format}")
        col1, col2 = st.columns([2, 1])
        with col1:
            report_topic = st.text_input("Research Topic", placeholder="e.g., Applications of Large Language Models in Education")
        with col2:
            min_papers = st.slider("Min papers", 1, 5, 3)
        if st.button("🚀 Generate Full Report", type="primary", use_container_width=True):
            if not api_key:
                st.error("Please enter your GROQ API Key.")
            elif not report_topic:
                st.warning("Please enter a research topic.")
            else:
                with st.spinner(f"📝 Generating {report_format}... this may take 30-60 seconds."):
                    try:
                        papers = search_papers(report_topic)
                        if len(papers) < min_papers:
                            papers += search_papers("artificial intelligence")
                        papers = list({p['title']: p for p in papers}.values())[:5]
                        report = generate_full_report(api_key, report_topic, papers, report_format)
                        st.session_state.generated_reports.append({"topic": report_topic, "format": report_format, "content": report, "generated_at": datetime.now().isoformat()})
                        st.markdown(report)
                        st.download_button("⬇️ Download Report (Markdown)", data=report,
                                           file_name=f"report_{report_topic[:30].replace(' ','_')}.md", mime="text/markdown")
                    except Exception as e:
                        st.error(f"Report generation failed: {str(e)}")

    with tab3:
        st.subheader("📚 Research Sources Library")
        if not st.session_state.current_sources:
            st.info("🔍 Sources will appear here as you research. Start by asking a question in the Chat tab.")
        else:
            col1, col2, col3 = st.columns(3)
            with col1: min_year      = st.number_input("Min Year",     min_value=1990, max_value=2024, value=2000)
            with col2: min_citations = st.number_input("Min Citations", min_value=0,    max_value=50000, value=0, step=500)
            with col3: sort_by       = st.selectbox("Sort By", ["Relevance", "Citations", "Year"])
            filtered = [p for p in st.session_state.current_sources if p.get("year", 0) >= min_year and p.get("citations", 0) >= min_citations]
            if sort_by == "Citations": filtered.sort(key=lambda x: x.get("citations", 0), reverse=True)
            elif sort_by == "Year":   filtered.sort(key=lambda x: x.get("year", 0),      reverse=True)
            else:                     filtered.sort(key=lambda x: x.get("relevance", 0), reverse=True)
            st.markdown(f"**Showing {len(filtered)} of {len(st.session_state.current_sources)} papers**")
            for paper in filtered:
                rel = paper.get("relevance", 0.5)
                rel_class = "relevance-high" if rel >= 0.85 else "relevance-medium" if rel >= 0.7 else "relevance-low"
                with st.expander(f"📄 {paper['title']} ({paper['year']})"):
                    st.markdown(f"""<div class="source-card {rel_class}">
                        <b>Authors:</b> {paper['authors']}<br>
                        <b>Journal:</b> {paper['journal']} | <b>Year:</b> {paper['year']} | <b>Citations:</b> {paper.get('citations',0):,}<br>
                        <b>Relevance:</b> {rel*100:.0f}%
                    </div>""", unsafe_allow_html=True)
                    st.markdown(f"**Abstract:** {paper['abstract']}")
                    st.markdown("**Citations:**")
                    st.code(f"APA: {paper['authors']} ({paper['year']}). {paper['title']}. {paper['journal']}.", language=None)
                    st.code(f"MLA: {paper['authors']}. \"{paper['title']}.\" {paper['journal']}, {paper['year']}.", language=None)
            if st.button("🗑️ Clear Sources Library"):
                st.session_state.current_sources = []
                st.rerun()


if __name__ == "__main__":
    main()
