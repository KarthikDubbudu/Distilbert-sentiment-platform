import streamlit as st

st.set_page_config(
    page_title="Sentiment Analysis Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Premium CSS Styling
# -------------------------------------------------
st.markdown("""
<style>
/* Global */
.main {
    background: radial-gradient(circle at top left, #111827 0%, #0E1117 45%, #090C10 100%);
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1250px;
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
@keyframes pulseGlow {
    0% {
        box-shadow: 0 0 0px rgba(79,139,249,0.10);
    }
    50% {
        box-shadow: 0 0 22px rgba(79,139,249,0.22);
    }
    100% {
        box-shadow: 0 0 0px rgba(79,139,249,0.10);
    }
}
@keyframes floatCard {
    0% {
        transform: translateY(0px);
    }
    50% {
        transform: translateY(-4px);
    }
    100% {
        transform: translateY(0px);
    }
}

/* Hero */
.hero-wrapper {
    padding: 2.6rem 2.4rem;
    border-radius: 28px;
    background:
        linear-gradient(135deg, rgba(28,31,38,0.95), rgba(17,24,39,0.95)),
        radial-gradient(circle at top right, rgba(79,139,249,0.16), transparent 35%);
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 20px 50px rgba(0,0,0,0.35);
    animation: fadeInUp 0.9s ease-out;
    position: relative;
    overflow: hidden;
}
.hero-wrapper::after {
    content: "";
    position: absolute;
    top: -80px;
    right: -60px;
    width: 220px;
    height: 220px;
    background: radial-gradient(circle, rgba(79,139,249,0.18), transparent 70%);
    border-radius: 50%;
}
.badge-row {
    display: flex;
    gap: 0.7rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}
.badge-pill {
    background: rgba(79,139,249,0.12);
    border: 1px solid rgba(79,139,249,0.25);
    color: #D6E4FF;
    padding: 0.42rem 0.85rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.2px;
}
.hero-title {
    font-size: 3rem;
    font-weight: 900;
    line-height: 1.1;
    color: #FAFAFA;
    margin-bottom: 0.8rem;
}
.hero-title span {
    color: #7FB3FF;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: #C9D1D9;
    line-height: 1.85;
    max-width: 900px;
}
.hero-side-card {
    padding: 1.6rem;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(28,31,38,0.98), rgba(20,24,32,0.98));
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 16px 30px rgba(0,0,0,0.30);
    animation: fadeInUp 1s ease-out;
    text-align: center;
    min-height: 100%;
}
.hero-side-icon {
    font-size: 4rem;
    margin-bottom: 0.6rem;
}
.hero-side-title {
    font-size: 1.2rem;
    font-weight: 800;
    color: #FAFAFA;
    margin-bottom: 0.5rem;
}
.hero-side-text {
    color: #C9D1D9;
    line-height: 1.7;
    font-size: 0.96rem;
}

/* Section title */
.section-title {
    font-size: 1.55rem;
    font-weight: 800;
    color: #FAFAFA;
    margin-top: 1.2rem;
    margin-bottom: 1rem;
    animation: fadeInUp 0.7s ease-out;
}
.section-subtitle {
    font-size: 0.98rem;
    color: #AAB6C5;
    margin-top: -0.4rem;
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
    min-height: 210px;
    animation: fadeInUp 0.8s ease-out;
    transition: all 0.3s ease;
}
.premium-card:hover {
    transform: translateY(-4px);
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
    margin-bottom: 0.6rem;
}
.card-text {
    font-size: 0.95rem;
    color: #C9D1D9;
    line-height: 1.7;
}

/* Workflow step cards */
.workflow-card {
    padding: 1.35rem;
    border-radius: 22px;
    background: linear-gradient(135deg, #151B24 0%, #10151D 100%);
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 10px 26px rgba(0,0,0,0.23);
    min-height: 220px;
    animation: fadeInUp 0.9s ease-out;
    position: relative;
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
    animation: pulseGlow 2.3s infinite ease-in-out;
}
.step-title {
    font-size: 1.08rem;
    font-weight: 800;
    color: #FAFAFA;
    margin-bottom: 0.55rem;
}
.step-text {
    color: #C9D1D9;
    line-height: 1.75;
    font-size: 0.95rem;
}

/* Showcase strip */
.showcase-box {
    padding: 1.2rem 1.35rem;
    border-radius: 18px;
    background: rgba(17,24,39,0.7);
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    animation: fadeInUp 0.9s ease-out;
}
.showcase-title {
    font-size: 1rem;
    font-weight: 700;
    color: #FAFAFA;
    margin-bottom: 0.3rem;
}
.showcase-text {
    color: #C9D1D9;
    line-height: 1.65;
    font-size: 0.92rem;
}

/* CTA strip */
.cta-strip {
    padding: 1.2rem 1.4rem;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(79,139,249,0.12), rgba(127,179,255,0.08));
    border: 1px solid rgba(79,139,249,0.24);
    color: #EAF2FF;
    margin-top: 1rem;
    margin-bottom: 1rem;
    animation: fadeInUp 1s ease-out;
}
.cta-title {
    font-size: 1.05rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
}
.cta-text {
    font-size: 0.95rem;
    color: #D7E5FF;
    line-height: 1.7;
}

/* Streamlit metrics polish */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1A1F2B 0%, #141922 100%);
    border: 1px solid rgba(255,255,255,0.06);
    padding: 0.9rem;
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
    padding: 0.65rem 1rem;
    width: 100%;
    border: 1px solid rgba(79,139,249,0.26);
    background: linear-gradient(135deg, #1B2535, #162030);
    color: white;
}
div.stButton > button:hover {
    border-color: rgba(127,179,255,0.45);
    box-shadow: 0 0 18px rgba(79,139,249,0.12);
}

/* Hide excess top spacing visuals */
header[data-testid="stHeader"] {
    background: transparent;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Hero Section
# -------------------------------------------------
col1, col2 = st.columns([1.85, 1], gap="large")

with col1:
    st.markdown("""
    <div class="hero-wrapper">
        <div class="badge-row">
            <div class="badge-pill">DistilBERT Powered</div>
            <div class="badge-pill">Supervised Workflow</div>
            <div class="badge-pill">CSV / XLSX Ready</div>
            <div class="badge-pill">Domain-Aware</div>
        </div>
        <div class="hero-title">🧠 Premium <span>Sentiment Analysis</span> Platform</div>
        <div class="hero-subtitle">
            A scalable web-based application designed for non-technical users to upload, clean, analyse,
            and interpret labelled text and structured feedback data through an elegant and highly interactive interface.
            The platform integrates <b>DistilBERT</b> with accessible data preparation, domain-aware analysis,
            and a polished results dashboard for practical and educational use.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="hero-side-card">
        <div class="hero-side-icon">✨</div>
        <div class="hero-side-title">Interactive Intelligence</div>
        <div class="hero-side-text">
            Transform messy datasets into clear, model-driven insights through a premium workflow built for clarity,
            interpretability, and confident decision-making.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# Highlights
# -------------------------------------------------
st.markdown('<div class="section-title">Platform Highlights</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">A concise overview of the core technological and usability foundations of the platform.</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Model Backbone", "DistilBERT")
m2.metric("Analysis Workflow", "Supervised")
m3.metric("Input Support", "CSV / XLSX")
m4.metric("Target Users", "Non-Technical")

# -------------------------------------------------
# Premium feature cards
# -------------------------------------------------
st.markdown('<div class="section-title">Core Capabilities</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Each module is designed to make the sentiment analysis pipeline intuitive, transparent, and visually engaging.</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="large")

with c1:
    st.markdown("""
    <div class="premium-card">
        <div class="card-icon">📂</div>
        <div class="card-title">Advanced Upload & Cleaning</div>
        <div class="card-text">
            Upload labelled datasets in CSV or Excel format, explore missing-value distributions, remove duplicates,
            standardise text, and compare messy and cleaned columns before analysis.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="premium-card">
        <div class="card-icon">🤖</div>
        <div class="card-title">Domain-Aware Sentiment Engine</div>
        <div class="card-text">
            Run sentiment analysis using DistilBERT while selecting the preferred domain context, such as student feedback,
            movie reviews, product reviews, social media, or a general-purpose workflow.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="premium-card">
        <div class="card-icon">📊</div>
        <div class="card-title">Premium Results Dashboard</div>
        <div class="card-text">
            Explore confidence scores, sentiment distributions, evaluation metrics, confusion matrices, and downloadable
            enriched outputs through a highly polished analytics experience.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# Showcase strip
# -------------------------------------------------
st.markdown('<div class="section-title">Why This Platform Stands Out</div>', unsafe_allow_html=True)

s1, s2, s3 = st.columns(3, gap="large")

with s1:
    st.markdown("""
    <div class="showcase-box">
        <div class="showcase-title">Accessible by Design</div>
        <div class="showcase-text">
            The entire application is structured for users without coding experience, making advanced NLP accessible in a practical way.
        </div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class="showcase-box">
        <div class="showcase-title">Transparent Workflow</div>
        <div class="showcase-text">
            Users can inspect data preparation, compare cleaned text, review predictions, and understand outputs rather than receiving black-box results.
        </div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown("""
    <div class="showcase-box">
        <div class="showcase-title">Research-Ready Experience</div>
        <div class="showcase-text">
            The platform supports academic experimentation, educational demonstration, and practical analytics with a modern visual interface.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# Workflow section
# -------------------------------------------------
st.markdown('<div class="section-title">Application Workflow</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">A guided three-stage process that moves from raw data to interpretable sentiment insights.</div>', unsafe_allow_html=True)

flow1, flow2, flow3 = st.columns(3, gap="large")

with flow1:
    st.markdown("""
    <div class="workflow-card">
        <div class="step-number">1</div>
        <div class="step-title">Upload & Inspect</div>
        <div class="step-text">
            Begin by uploading a labelled dataset and inspecting its structure, missing values, duplicate records,
            and overall data quality through clean previews and visual diagnostics.
        </div>
    </div>
    """, unsafe_allow_html=True)

with flow2:
    st.markdown("""
    <div class="workflow-card">
        <div class="step-number">2</div>
        <div class="step-title">Clean & Analyse</div>
        <div class="step-text">
            Apply configurable cleaning operations, select the appropriate domain, and perform sentiment analysis
            using DistilBERT to generate predictions and confidence scores.
        </div>
    </div>
    """, unsafe_allow_html=True)

with flow3:
    st.markdown("""
    <div class="workflow-card">
        <div class="step-number">3</div>
        <div class="step-title">Explore & Interpret</div>
        <div class="step-text">
            Review the enriched outputs in a premium dashboard with visual analytics, evaluation metrics,
            and downloadable results tailored for learning and decision support.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# CTA strip
# -------------------------------------------------
st.markdown("""
<div class="cta-strip">
    <div class="cta-title">🚀 Getting Started</div>
    <div class="cta-text">
        Use the navigation menu on the left and begin with <b>Upload and Clean</b>.
        The platform has been designed to provide a complete, user-friendly sentiment analysis workflow
        from dataset preparation to final visual interpretation.
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Interactive quick actions
# -------------------------------------------------
st.markdown('<div class="section-title">Quick View</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">A simple interactive panel to summarise the platform orientation and intended use.</div>', unsafe_allow_html=True)

qa1, qa2 = st.columns([1.2, 1], gap="large")

with qa1:
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
        <div class="info-box">
        This platform is especially suitable for learners who want to understand how labelled data,
        cleaning operations, model predictions, and evaluation metrics work together in a complete NLP workflow.
        </div>
        """, unsafe_allow_html=True)

    elif user_goal == "Business review analysis":
        st.markdown("""
        <div class="info-box">
        The platform can be used to analyse customer-facing feedback and review datasets,
        helping users detect overall sentiment patterns and confidence trends in a structured way.
        </div>
        """, unsafe_allow_html=True)

    elif user_goal == "Research demonstration":
        st.markdown("""
        <div class="info-box">
        The workflow is appropriate for project demonstrations, dissertation work,
        and research communication where interpretability and usability are important.
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="info-box">
        The general workflow provides a straightforward path from uploaded labelled data
        to sentiment predictions and visual result interpretation.
        </div>
        """, unsafe_allow_html=True)

with qa2:
    st.markdown("""
    <div class="premium-card" style="min-height: 100%;">
        <div class="card-icon">💡</div>
        <div class="card-title">Suggested Navigation</div>
        <div class="card-text">
            <b>Page 1:</b> Upload and clean the dataset<br><br>
            <b>Page 2:</b> Configure the text column, label column, and domain, then run DistilBERT analysis<br><br>
            <b>Page 3:</b> Explore metrics, graphics, confidence scores, and downloadable outputs
        </div>
    </div>
    """, unsafe_allow_html=True)
