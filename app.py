import json
from pathlib import Path

import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Sentiment Analysis Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -------------------------------------------------
# Helpers
# -------------------------------------------------
def load_lottie_file(filepath: str):
    file_path = Path(filepath)
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


# -------------------------------------------------
# Load local Lottie animation
# -------------------------------------------------
lottie_animation = load_lottie_file("assets/home_animation.json")


# -------------------------------------------------
# Premium CSS Styling
# -------------------------------------------------
st.markdown("""
<style>
.main {
    background: radial-gradient(circle at top left, #111827 0%, #0E1117 45%, #090C10 100%);
}
.block-container {
    padding-top: 1.3rem;
    padding-bottom: 2rem;
    max-width: 1280px;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1220 0%, #111827 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}

/* Animations */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(18px);
    }
    to {
        opacity: 1;
        transform: translateY(0px);
    }
}
@keyframes softGlow {
    0% { box-shadow: 0 0 0px rgba(79,139,249,0.08); }
    50% { box-shadow: 0 0 24px rgba(79,139,249,0.18); }
    100% { box-shadow: 0 0 0px rgba(79,139,249,0.08); }
}

/* Hero */
.hero-box {
    padding: 2.3rem;
    border-radius: 28px;
    background:
        linear-gradient(135deg, rgba(28,31,38,0.96), rgba(17,24,39,0.96)),
        radial-gradient(circle at top right, rgba(79,139,249,0.14), transparent 35%);
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 20px 48px rgba(0,0,0,0.34);
    animation: fadeInUp 0.85s ease-out;
    position: relative;
    overflow: hidden;
}
.hero-box::after {
    content: "";
    position: absolute;
    top: -90px;
    right: -70px;
    width: 240px;
    height: 240px;
    background: radial-gradient(circle, rgba(79,139,249,0.18), transparent 72%);
    border-radius: 50%;
}
.badge-row {
    display: flex;
    gap: 0.7rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}
.badge-pill {
    background: rgba(79,139,249,0.10);
    border: 1px solid rgba(79,139,249,0.24);
    color: #D8E6FF;
    padding: 0.42rem 0.85rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.2px;
}
.hero-title {
    font-size: 3rem;
    font-weight: 900;
    line-height: 1.08;
    color: #FAFAFA;
    margin-bottom: 0.85rem;
}
.hero-title span {
    color: #7FB3FF;
}
.hero-subtitle {
    font-size: 1.03rem;
    color: #C9D1D9;
    line-height: 1.85;
    max-width: 900px;
}
.hero-side-panel {
    padding: 1.35rem;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(26,31,43,0.98), rgba(20,25,34,0.98));
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 16px 34px rgba(0,0,0,0.28);
    min-height: 100%;
    animation: fadeInUp 1s ease-out;
}
.lottie-wrapper {
    border-radius: 20px;
    padding: 0.4rem;
    background: linear-gradient(135deg, rgba(79,139,249,0.08), rgba(127,179,255,0.04));
    border: 1px solid rgba(79,139,249,0.16);
    animation: softGlow 2.6s infinite ease-in-out;
}

/* Section */
.section-title {
    font-size: 1.55rem;
    font-weight: 800;
    color: #FAFAFA;
    margin-top: 1.1rem;
    margin-bottom: 1rem;
    animation: fadeInUp 0.8s ease-out;
}
.section-subtitle {
    font-size: 0.97rem;
    color: #AAB6C5;
    margin-top: -0.35rem;
    margin-bottom: 1rem;
    line-height: 1.7;
}

/* Cards */
.premium-card {
    padding: 1.35rem;
    border-radius: 22px;
    background: linear-gradient(135deg, #1A1F2B 0%, #141922 100%);
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 28px rgba(0,0,0,0.22);
    min-height: 220px;
    animation: fadeInUp 0.85s ease-out;
    transition: all 0.28s ease;
}
.premium-card:hover {
    transform: translateY(-5px);
    border: 1px solid rgba(79,139,249,0.28);
    box-shadow: 0 16px 34px rgba(0,0,0,0.30);
}
.card-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}
.card-title {
    font-size: 1.08rem;
    font-weight: 800;
    color: #FAFAFA;
    margin-bottom: 0.55rem;
}
.card-text {
    font-size: 0.95rem;
    color: #C9D1D9;
    line-height: 1.72;
}

/* Workflow */
.workflow-card {
    padding: 1.35rem;
    border-radius: 22px;
    background: linear-gradient(135deg, #151B24 0%, #10151D 100%);
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 10px 26px rgba(0,0,0,0.23);
    min-height: 220px;
    animation: fadeInUp 0.9s ease-out;
}
.step-number {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4F8BF9, #7FB3FF);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    margin-bottom: 0.8rem;
    animation: softGlow 2.2s infinite ease-in-out;
}
.step-title {
    font-size: 1.08rem;
    font-weight: 800;
    color: #FAFAFA;
    margin-bottom: 0.55rem;
}
.step-text {
    color: #C9D1D9;
    line-height: 1.72;
    font-size: 0.95rem;
}

/* Info / CTA */
.info-strip {
    padding: 1.1rem 1.3rem;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(79,139,249,0.10), rgba(127,179,255,0.06));
    border: 1px solid rgba(79,139,249,0.22);
    color: #DCE8FF;
    margin-top: 1rem;
    margin-bottom: 1rem;
    animation: fadeInUp 1s ease-out;
}
.cta-box {
    padding: 1.2rem 1.35rem;
    border-radius: 18px;
    background: linear-gradient(135deg, #161B22 0%, #121720 100%);
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 24px rgba(0,0,0,0.20);
    animation: fadeInUp 1s ease-out;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1A1F2B 0%, #141922 100%);
    border: 1px solid rgba(255,255,255,0.06);
    padding: 0.95rem;
    border-radius: 18px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.18);
    animation: fadeInUp 0.9s ease-out;
}
div[data-testid="stMetricValue"] {
    color: #FAFAFA;
}
div[data-testid="stMetricLabel"] {
    color: #AAB6C5;
}

/* Buttons */
div.stButton > button {
    border-radius: 14px;
    font-weight: 700;
    padding: 0.68rem 1rem;
    width: 100%;
    border: 1px solid rgba(79,139,249,0.26);
    background: linear-gradient(135deg, #1B2535, #162030);
    color: white;
}
div.stButton > button:hover {
    border-color: rgba(127,179,255,0.45);
    box-shadow: 0 0 18px rgba(79,139,249,0.12);
}

header[data-testid="stHeader"] {
    background: transparent;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# Hero Section
# -------------------------------------------------
left, right = st.columns([1.75, 1], gap="large")

with left:
    st.markdown("""
    <div class="hero-box">
        <div class="badge-row">
            <div class="badge-pill">DistilBERT Powered</div>
            <div class="badge-pill">Supervised Workflow</div>
            <div class="badge-pill">CSV / XLSX Support</div>
            <div class="badge-pill">Domain-Aware</div>
        </div>
        <div class="hero-title">🧠 Ultra-Premium <span>Sentiment Analysis</span> Experience</div>
        <div class="hero-subtitle">
            A scalable, elegant, and user-focused web platform designed to transform labelled text and
            structured feedback data into clear sentiment insights. Built for non-technical users, the application
            combines smart data cleaning, domain-aware analysis, DistilBERT-powered prediction, and polished
            visual interpretation in one premium workflow.
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown('<div class="hero-side-panel">', unsafe_allow_html=True)
    st.markdown('<div class="lottie-wrapper">', unsafe_allow_html=True)

    if lottie_animation is not None:
        st_lottie(
            lottie_animation,
            speed=1,
            reverse=False,
            loop=True,
            quality="high",
            height=280,
            key="home_lottie"
        )
    else:
        st.markdown("""
        <div style="text-align:center; color:#C9D1D9; padding:2rem 1rem;">
            <div style="font-size:3rem;">✨</div>
            <div style="font-size:1rem; font-weight:700; color:#FAFAFA; margin-top:0.5rem;">
                Lottie animation not found
            </div>
            <div style="margin-top:0.5rem; line-height:1.7;">
                Add a JSON file at <b>assets/home_animation.json</b> to display the premium animation here.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="margin-top:1rem; text-align:center; color:#C9D1D9; line-height:1.7;">
        Interactive visual storytelling for a modern and memorable first impression.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Highlights
# -------------------------------------------------
st.markdown('<div class="section-title">Platform Highlights</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">A concise overview of the technical foundations and practical usability of the platform.</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Model Backbone", "DistilBERT")
m2.metric("Workflow Type", "Supervised")
m3.metric("Input Support", "CSV / XLSX")
m4.metric("Target Audience", "Non-Technical")

# -------------------------------------------------
# Feature Cards
# -------------------------------------------------
st.markdown('<div class="section-title">Core Capabilities</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Each module is crafted to make the full sentiment analysis journey transparent, intuitive, and visually impressive.</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="large")

with c1:
    st.markdown("""
    <div class="premium-card">
        <div class="card-icon">📂</div>
        <div class="card-title">Advanced Upload & Cleaning</div>
        <div class="card-text">
            Upload labelled CSV or Excel datasets, inspect missing-value patterns, remove duplicates, standardise text,
            compare messy and cleaned columns, and prepare the data with confidence before analysis.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="premium-card">
        <div class="card-icon">🤖</div>
        <div class="card-title">Domain-Aware Sentiment Analysis</div>
        <div class="card-text">
            Perform DistilBERT-based sentiment classification with optional domain guidance across student feedback,
            product reviews, movie reviews, social media content, and general-purpose textual data.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="premium-card">
        <div class="card-icon">📊</div>
        <div class="card-title">Premium Analytics Dashboard</div>
        <div class="card-text">
            Review confidence scores, sentiment distributions, evaluation metrics, visual comparisons,
            and downloadable enriched results through a polished and highly interactive reporting space.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# Workflow
# -------------------------------------------------
st.markdown('<div class="section-title">Application Workflow</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">A premium three-stage pipeline that moves from raw input to interpretable sentiment insight.</div>', unsafe_allow_html=True)

w1, w2, w3 = st.columns(3, gap="large")

with w1:
    st.markdown("""
    <div class="workflow-card">
        <div class="step-number">1</div>
        <div class="step-title">Upload & Inspect</div>
        <div class="step-text">
            Import your labelled dataset and inspect its quality through previews, profile metrics,
            missing-value summaries, and structured data diagnostics.
        </div>
    </div>
    """, unsafe_allow_html=True)

with w2:
    st.markdown("""
    <div class="workflow-card">
        <div class="step-number">2</div>
        <div class="step-title">Clean & Analyse</div>
        <div class="step-text">
            Apply configurable cleaning operations, choose the preferred domain, and run DistilBERT-powered
            sentiment analysis with a clear and guided user experience.
        </div>
    </div>
    """, unsafe_allow_html=True)

with w3:
    st.markdown("""
    <div class="workflow-card">
        <div class="step-number">3</div>
        <div class="step-title">Interpret & Download</div>
        <div class="step-text">
            Explore interactive charts, prediction summaries, performance indicators, and downloadable results
            designed for learning, research, and practical decision support.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# CTA and Quick View
# -------------------------------------------------
st.markdown("""
<div class="info-strip">
<b>🚀 Getting Started:</b> Use the left navigation menu and begin with <b>Upload and Clean</b>.
The platform is designed to guide you from data preparation to final visual interpretation in one cohesive workflow.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Quick View</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Select your main purpose to see how the platform can support your workflow.</div>', unsafe_allow_html=True)

q1, q2 = st.columns([1.2, 1], gap="large")

with q1:
    user_goal = st.selectbox(
        "Select your primary purpose",
        [
            "Educational learning and experimentation",
            "Business review analysis",
            "Research demonstration",
            "General sentiment exploration"
        ]
    )

    if user_goal == "Educational learning and experimentation":
        st.markdown("""
        <div class="cta-box">
            <b style="color:#FAFAFA;">🎓 Educational Learning</b><br><br>
            <span style="color:#C9D1D9; line-height:1.8;">
            The platform is well-suited for learners who want to understand how labelled data, cleaning operations,
            model predictions, and evaluation metrics interact within a complete NLP workflow.
            </span>
        </div>
        """, unsafe_allow_html=True)

    elif user_goal == "Business review analysis":
        st.markdown("""
        <div class="cta-box">
            <b style="color:#FAFAFA;">💼 Business Review Analysis</b><br><br>
            <span style="color:#C9D1D9; line-height:1.8;">
            The workflow can be used to analyse customer-facing review datasets and uncover overall sentiment patterns,
            confidence trends, and structured business-facing insights.
            </span>
        </div>
        """, unsafe_allow_html=True)

    elif user_goal == "Research demonstration":
        st.markdown("""
        <div class="cta-box">
            <b style="color:#FAFAFA;">🔬 Research Demonstration</b><br><br>
            <span style="color:#C9D1D9; line-height:1.8;">
            The interface is suitable for dissertation work, academic demonstrations, and project presentations
            where accessibility, explainability, and visual polish are important.
            </span>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="cta-box">
            <b style="color:#FAFAFA;">🌐 General Exploration</b><br><br>
            <span style="color:#C9D1D9; line-height:1.8;">
            The platform provides a straightforward path from uploaded labelled data
            to sentiment prediction and interpretive visual analytics.
            </span>
        </div>
        """, unsafe_allow_html=True)

with q2:
    st.markdown("""
    <div class="premium-card" style="min-height:100%;">
        <div class="card-icon">🧭</div>
        <div class="card-title">Suggested Navigation</div>
        <div class="card-text">
            <b>Page 1:</b> Upload and clean the dataset<br><br>
            <b>Page 2:</b> Select the text column, label column, and domain, then run DistilBERT analysis<br><br>
            <b>Page 3:</b> Explore graphics, metrics, confidence scores, and downloadable outputs<br><br>
            <b>Page 4:</b> Share feedback to help improve the platform
        </div>
    </div>
    """, unsafe_allow_html=True)
