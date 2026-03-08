"""
Academic Research Assistant
Built with GROQ API + Streamlit
Project 8 - Youssef Khaled Ismail
"""

import subprocess, sys
subprocess.run([sys.executable, '-m', 'pip', 'install', 'groq==0.9.0', '-q'], check=False)

import streamlit as st
import json
from datetime import datetime
from typing import List, Dict
from groq import Groq

st.set_page_config(page_title="Academic Research Assistant", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

st.markdown("""<style>
.research-header{background:linear-gradient(135deg,#1a237e 0%,#7b1fa2 100%);padding:20px 30px;border-radius:12px;color:white;margin-bottom:20px;}
.source-card{background:#f3e5f5;border-left:4px solid #7b1fa2;padding:12px 16px;border-radius:8px;margin:6px 0;}
.relevance-high{border-left-color:#4CAF50;background:#e8f5e9;}
.relevance-medium{border-left-color:#FF9800;background:#fff8e1;}
.relevance-low{border-left-color:#f44336;background:#ffebee;}
</style>""", unsafe_allow_html=True)

MOCK_PAPERS = {
    "machine learning": [
        {"title":"Attention Is All You Need","authors":"Vaswani et al.","year":2017,"journal":"NeurIPS","abstract":"We propose the Transformer, a model architecture based solely on attention mechanisms. Experiments show these models are superior in quality while being more parallelizable.","citations":90000,"doi":"10.48550/arXiv.1706.03762","relevance":0.95},
        {"title":"BERT: Pre-training of Deep Bidirectional Transformers","authors":"Devlin et al.","year":2018,"journal":"NAACL","abstract":"We introduce BERT, designed to pre-train deep bidirectional representations from unlabeled text by jointly conditioning on both left and right context.","citations":75000,"doi":"10.48550/arXiv.1810.04805","relevance":0.88},
        {"title":"Deep Residual Learning for Image Recognition","authors":"He et al.","year":2016,"journal":"CVPR","abstract":"We present a residual learning framework to ease the training of networks substantially deeper than those used previously.","citations":120000,"doi":"10.1109/CVPR.2016.90","relevance":0.82},
    ],
    "climate change": [
        {"title":"Global Warming of 1.5 Degrees - IPCC Special Report","authors":"IPCC Working Group I","year":2018,"journal":"IPCC","abstract":"An IPCC special report on the impacts of global warming of 1.5 degrees above pre-industrial levels and related global greenhouse gas emission pathways.","citations":25000,"doi":"10.1017/9781009157940","relevance":0.97},
        {"title":"Ocean Acidification and its Effects on Marine Ecosystems","authors":"Orr et al.","year":2020,"journal":"Nature Climate Change","abstract":"This review synthesizes evidence for the impacts of ocean acidification on marine organisms and ecosystems.","citations":4500,"doi":"10.1038/s41558-020-0869-0","relevance":0.85},
    ],
    "quantum computing": [
        {"title":"Quantum supremacy using a programmable superconducting processor","authors":"Arute et al. (Google AI)","year":2019,"journal":"Nature","abstract":"We developed a quantum processor using 53 programmable superconducting qubits that performed a target computation in 200 seconds.","citations":6000,"doi":"10.1038/s41586-019-1666-5","relevance":0.96},
        {"title":"Quantum Error Correction: An Introductory Guide","authors":"Devitt et al.","year":2023,"journal":"Contemporary Physics","abstract":"We review quantum error correction from threshold theorems and stabilizer codes to topological methods and fault-tolerant computation.","citations":2100,"doi":"10.1080/00107514.2013.810887","relevance":0.89},
    ],
    "artificial intelligence": [
        {"title":"Human-Level Control through Deep Reinforcement Learning","authors":"Mnih et al. (DeepMind)","year":2015,"journal":"Nature","abstract":"We present a model-free reinforcement learning algorithm combining deep neural networks with Q-learning.","citations":18000,"doi":"10.1038/nature14236","relevance":0.91},
        {"title":"GPT-4 Technical Report","authors":"OpenAI","year":2023,"journal":"arXiv","abstract":"We report the development of GPT-4, a large multimodal model exhibiting human-level performance on various professional benchmarks.","citations":9000,"doi":"10.48550/arXiv.2303.08774","relevance":0.93},
    ],
    "blockchain": [
        {"title":"Bitcoin: A Peer-to-Peer Electronic Cash System","authors":"Nakamoto, S.","year":2008,"journal":"White Paper","abstract":"A purely peer-to-peer version of electronic cash allowing online payments without a financial institution.","citations":20000,"doi":"https://bitcoin.org/bitcoin.pdf","relevance":0.99},
    ],
}

DEVELOPMENTS = {
    "machine learning": "Recent: (1) GPT-4 achieving human-level performance. (2) Mixture-of-Experts reducing costs. (3) Constitutional AI for alignment. (4) LoRA enabling efficient fine-tuning.",
    "quantum computing": "Recent: (1) IBM 1000+ qubit processors. (2) Google quantum error correction below threshold. (3) Microsoft topological qubits approach.",
    "climate change": "Recent: (1) 2023 hottest year on record. (2) Arctic sea ice at historic minimum. (3) Carbon capture costs dropping 40%.",
    "artificial intelligence": "Recent: (1) Foundation models as general-purpose engines. (2) AI agents performing complex tasks. (3) Multimodal AI integrating vision and language.",
    "blockchain": "Recent: (1) Ethereum proof-of-stake reducing energy by 99.9%. (2) Layer-2 scaling. (3) ZK-proofs enabling private transactions.",
}

def search_papers(query: str) -> List[Dict]:
    q = query.lower()
    results = []
    for topic, papers in MOCK_PAPERS.items():
        if any(word in q for word in topic.split()):
            results.extend(papers)
    if not results:
        results = MOCK_PAPERS.get("artificial intelligence", []) + MOCK_PAPERS.get("machine learning", [])[:1]
    seen, unique = set(), []
    for p in results:
        if p["title"] not in seen:
            seen.add(p["title"])
            unique.append(p)
    return unique[:5]

def get_developments(query: str) -> str:
    q = query.lower()
    for key, dev in DEVELOPMENTS.items():
        if key in q or any(word in q for word in key.split()):
            return dev
    return "Active research field with significant 2023-2024 publications."

def call_groq(api_key: str, system: str, user: str, history=None) -> str:
    client = Groq(api_key=api_key)
    messages = [{"role": "system", "content": system}]
    if history:
        messages.extend(history[-6:])
    messages.append({"role": "user", "content": user})
    resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, temperature=0.3, max_tokens=2000)
    return resp.choices[0].message.content

def get_research_response(api_key, query, history, report_format, depth):
    papers = search_papers(query)
    devs = get_developments(query)
    context = "=== Academic Papers ===\n"
    for p in papers:
        context += f"- {p['title']} by {p['authors']} ({p['year']}) in {p['journal']}\n"
        context += f"  Abstract: {p['abstract'][:200]}...\n"
        context += f"  Citations: {p.get('citations',0):,} | DOI: {p.get('doi','')}\n\n"
    context += f"\n=== Recent Developments ===\n{devs}\n"
    system = (f"You are an expert Academic Research Assistant.\nReport Format: {report_format} | Depth: {depth}\n"
              f"Date: {datetime.now().strftime('%B %d, %Y')}\n\nInstructions:\n"
              f"1. Use the provided data to answer comprehensively\n2. Cite with [Author Year] format\n"
              f"3. Present conflicting findings objectively\n4. Suggest research gaps\n5. Be academic and thorough\n\n"
              f"RESEARCH DATA:\n{context}")
    return call_groq(api_key, system, query, history)

def generate_full_report(api_key, topic, papers, report_format):
    sources = ""
    for i, p in enumerate(papers[:5], 1):
        sources += f"\n[{i}] {p.get('title','')} - {p.get('authors','')} ({p.get('year','')})\nAbstract: {p.get('abstract','')[:300]}...\n"
    fmap = {
        "Structured Report": "Create: Title, Abstract, Introduction, Background, Key Findings, Analysis, Implications, Conclusion, References",
        "Literature Review": "Create: Introduction, Thematic Analysis, Historical Context, Current State, Research Gaps, Future Directions, References",
        "Executive Summary": "Create: Overview, Top 5 Key Findings, Practical Implications, Recommended Actions, Sources",
        "Annotated Bibliography": "Create: intro paragraph, then for each source: full citation + 3-4 sentence annotation",
    }
    system = "You are an expert academic writer. Generate comprehensive, well-structured academic documents."
    user = (f"Generate a comprehensive {report_format} on: \"{topic}\"\n\nSources:\n{sources}\n\n"
            f"Instructions: {fmap.get(report_format,'Write a well-structured academic document')}\n\n"
            f"Requirements: Use [Author Year] citations, minimum 600 words, markdown formatting with headers.")
    return call_groq(api_key, system, user)

def init_session():
    for k, v in {"messages":[],"research_sessions":[],"current_sources":[],"total_papers":0,"chat_history":[]}.items():
        if k not in st.session_state:
            st.session_state[k] = v

def main():
    init_session()
    st.markdown('<div class="research-header"><h1>🎓 Academic Research Assistant</h1><p style="margin:0;opacity:0.9">AI-powered research synthesis · Citation management · Multi-source analysis</p></div>', unsafe_allow_html=True)

    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input("GROQ API Key", type="password", placeholder="gsk_...")
        st.divider()
        st.subheader("📋 Report Settings")
        report_format = st.selectbox("Report Format", ["Structured Report","Literature Review","Executive Summary","Annotated Bibliography"])
        research_depth = st.selectbox("Research Depth", ["Comprehensive","Overview","Deep Dive"])
        st.divider()
        st.subheader("📊 Session Stats")
        c1, c2 = st.columns(2)
        c1.metric("Searches", len(st.session_state.research_sessions))
        c2.metric("Papers", st.session_state.total_papers)
        st.divider()
        st.subheader("💡 Quick Topics")
        for t in ["Machine learning in healthcare","Climate change solutions","Quantum computing applications","AI ethics and bias","Blockchain in supply chain"]:
            if st.button(f"🔬 {t}", key=t, use_container_width=True):
                st.session_state.messages.append({"role":"user","content":f"Research topic: {t}"})
                st.rerun()
        if st.button("🗑️ Clear Session", use_container_width=True):
            for k in ["messages","chat_history","current_sources","research_sessions"]:
                st.session_state[k] = []
            st.rerun()

    tab1, tab2, tab3 = st.tabs(["🔍 Research Chat","📄 Generate Report","📚 Sources Library"])

    with tab1:
        st.subheader("Ask Your Research Question")
        if not st.session_state.messages:
            st.markdown('<div style="text-align:center;padding:30px;color:#888;"><h3>🔬 Start Your Research</h3><p>Ask me about any academic topic.</p></div>', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"], avatar="👨‍🎓" if msg["role"]=="user" else "🎓"):
                st.markdown(msg["content"])
        query = st.chat_input("Ask a research question...")
        if query:
            if not api_key:
                st.error("Please enter your GROQ API Key in the sidebar.")
            else:
                st.session_state.messages.append({"role":"user","content":query})
                with st.chat_message("user", avatar="👨‍🎓"): st.markdown(query)
                with st.chat_message("assistant", avatar="🎓"):
                    with st.spinner("🔍 Searching databases and synthesizing research..."):
                        try:
                            response = get_research_response(api_key, query, st.session_state.chat_history, report_format, research_depth)
                            papers = search_papers(query)
                            if papers:
                                st.session_state.current_sources.extend(papers)
                                st.session_state.current_sources = list({p['title']:p for p in st.session_state.current_sources}.values())
                                st.session_state.total_papers += len(papers)
                            st.markdown(response)
                            st.session_state.messages.append({"role":"assistant","content":response})
                            st.session_state.research_sessions.append(query)
                            st.session_state.chat_history.append({"role":"user","content":query})
                            st.session_state.chat_history.append({"role":"assistant","content":response})
                            if len(st.session_state.chat_history) > 12:
                                st.session_state.chat_history = st.session_state.chat_history[-12:]
                            if papers:
                                with st.expander(f"📊 Found {len(papers)} relevant papers"):
                                    for p in papers[:3]:
                                        rel = p.get("relevance",0.5)
                                        rc = "relevance-high" if rel>=0.85 else "relevance-medium" if rel>=0.7 else "relevance-low"
                                        st.markdown(f'<div class="source-card {rc}"><b>{p["title"]}</b> - {p["authors"]} ({p["year"]})<br><small>📰 {p["journal"]} | 🔢 {p.get("citations",0):,} citations | Relevance: {rel*100:.0f}%</small></div>', unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

    with tab2:
        st.subheader(f"📄 Generate {report_format}")
        col1, col2 = st.columns([2,1])
        with col1: report_topic = st.text_input("Research Topic", placeholder="e.g., Applications of LLMs in Education")
        with col2: min_papers = st.slider("Min papers", 1, 5, 3)
        if st.button("🚀 Generate Full Report", type="primary", use_container_width=True):
            if not api_key: st.error("Please enter your GROQ API Key.")
            elif not report_topic: st.warning("Please enter a research topic.")
            else:
                with st.spinner(f"📝 Generating {report_format}..."):
                    try:
                        papers = search_papers(report_topic)
                        if len(papers) < min_papers: papers += search_papers("artificial intelligence")
                        papers = list({p['title']:p for p in papers}.values())[:5]
                        report = generate_full_report(api_key, report_topic, papers, report_format)
                        st.markdown(report)
                        st.download_button("⬇️ Download Report (Markdown)", data=report, file_name=f"report_{report_topic[:30].replace(' ','_')}.md", mime="text/markdown")
                    except Exception as e:
                        st.error(f"Report generation failed: {str(e)}")

    with tab3:
        st.subheader("📚 Research Sources Library")
        if not st.session_state.current_sources:
            st.info("🔍 Sources will appear here as you research.")
        else:
            col1, col2, col3 = st.columns(3)
            with col1: min_year = st.number_input("Min Year", min_value=1990, max_value=2024, value=2000)
            with col2: min_cit  = st.number_input("Min Citations", min_value=0, max_value=50000, value=0, step=500)
            with col3: sort_by  = st.selectbox("Sort By", ["Relevance","Citations","Year"])
            filtered = [p for p in st.session_state.current_sources if p.get("year",0)>=min_year and p.get("citations",0)>=min_cit]
            if sort_by=="Citations": filtered.sort(key=lambda x:x.get("citations",0),reverse=True)
            elif sort_by=="Year":    filtered.sort(key=lambda x:x.get("year",0),reverse=True)
            else:                    filtered.sort(key=lambda x:x.get("relevance",0),reverse=True)
            st.markdown(f"**Showing {len(filtered)} of {len(st.session_state.current_sources)} papers**")
            for paper in filtered:
                rel = paper.get("relevance",0.5)
                rc = "relevance-high" if rel>=0.85 else "relevance-medium" if rel>=0.7 else "relevance-low"
                with st.expander(f"📄 {paper['title']} ({paper['year']})"):
                    st.markdown(f'<div class="source-card {rc}"><b>Authors:</b> {paper["authors"]}<br><b>Journal:</b> {paper["journal"]} | <b>Year:</b> {paper["year"]} | <b>Citations:</b> {paper.get("citations",0):,}<br><b>Relevance:</b> {rel*100:.0f}%</div>', unsafe_allow_html=True)
                    st.markdown(f"**Abstract:** {paper['abstract']}")
                    st.code(f"APA: {paper['authors']} ({paper['year']}). {paper['title']}. {paper['journal']}.", language=None)
                    st.code(f'MLA: {paper["authors"]}. "{paper["title"]}." {paper["journal"]}, {paper["year"]}.', language=None)
            if st.button("🗑️ Clear Sources Library"):
                st.session_state.current_sources = []
                st.rerun()

if __name__ == "__main__":
    main()
