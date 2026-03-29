import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sentiment Analysis Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom CSS for styling
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
.hero-box {
    padding: 2.5rem 2rem;
    border-radius: 20px;
    background: linear-gradient(135deg, #1C1F26, #111827);
    box-shadow: 0 8px 24px rgba(0,0,0,0.35);
    margin-bottom: 1.5rem;
}
.hero-title {
    font-size: 2.7rem;
    font-weight: 800;
    color: #FAFAFA;
    margin-bottom: 0.5rem;
}
.hero-subtitle {
    font-size: 1.1rem;
    color: #C9D1D9;
    line-height: 1.7;
}
.feature-card {
    padding: 1.4rem;
    border-radius: 18px;
    background-color: #1C1F26;
    box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    height: 100%;
}
.feature-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #FAFAFA;
    margin-bottom: 0.6rem;
}
.feature-text {
    font-size: 0.95rem;
    color: #C9D1D9;
    line-height: 1.6;
}
.section-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #FAFAFA;
    margin-top: 1rem;
    margin-bottom: 1rem;
}
.info-strip {
    padding: 1rem 1.2rem;
    border-radius: 14px;
    background-color: #161B22;
    border: 1px solid #30363D;
    color: #C9D1D9;
    margin-top: 1rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Hero section
# -----------------------------
col1, col2 = st.columns([1.8, 1])

with col1:
    st.markdown("""
    <div class="hero-box">
        <div class="hero-title">🧠 Sentiment Analysis Platform</div>
        <div class="hero-subtitle">
            A scalable web-based platform leveraging <b>DistilBERT</b> for labelled text and structured feedback data.
            Designed for non-technical users, this application helps users upload, clean, analyse, and interpret
            sentiment data through an intuitive interface.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="hero-box" style="text-align:center;">
        <div style="font-size:4rem;">📊</div>
        <div style="font-size:1.2rem; font-weight:700; color:#FAFAFA;">Interactive Analytics</div>
        <div style="color:#C9D1D9; margin-top:0.5rem;">
            Clean data, classify sentiment, and explore model-driven insights in one place.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Quick metrics
# -----------------------------
st.markdown('<div class="section-title">Platform Highlights</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Model", "DistilBERT")
m2.metric("Workflow", "Supervised")
m3.metric("Supported Input", "CSV / XLSX")
m4.metric("User Type", "Non-Technical")

# -----------------------------
# Feature cards
# -----------------------------
st.markdown('<div class="section-title">Core Features</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📂 Upload and Clean Data</div>
        <div class="feature-text">
            Upload labelled datasets in CSV or Excel format, identify missing values,
            clean duplicates, standardise text, and preview refined data before analysis.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🤖 Domain-Aware Sentiment Analysis</div>
        <div class="feature-text">
            Perform sentiment classification using DistilBERT with support for domain-aware workflows,
            such as student feedback, product reviews, and media-related text.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📈 Visual Results and Insights</div>
        <div class="feature-text">
            Explore predictions, confidence scores, and visual summaries through an accessible
            dashboard designed to support learning, reflection, and decision-making.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Process flow section
# -----------------------------
st.markdown('<div class="section-title">Application Workflow</div>', unsafe_allow_html=True)

flow1, flow2, flow3 = st.columns(3)

with flow1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">Step 1</div>
        <div class="feature-text">
            Upload a labelled dataset and inspect data quality through previews, summaries, and missing-value charts.
        </div>
    </div>
    """, unsafe_allow_html=True)

with flow2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">Step 2</div>
        <div class="feature-text">
            Clean and prepare the dataset using interactive controls for duplicate removal, missing-value handling, and text refinement.
        </div>
    </div>
    """, unsafe_allow_html=True)

with flow3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">Step 3</div>
        <div class="feature-text">
            Run sentiment analysis, evaluate predictions, and interpret the results using visual outputs and downloadable files.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Nice info panel
# -----------------------------
st.markdown("""
<div class="info-strip">
<b>Getting Started:</b> Use the navigation menu on the left and begin with the <b>Upload and Clean</b> page.
This platform is designed to provide an accessible end-to-end sentiment analysis workflow without requiring coding expertise.
</div>
""", unsafe_allow_html=True)
