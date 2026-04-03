import os
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Feedback", page_icon="💬", layout="wide")


# -------------------------------------------------
# Premium CSS Styling
# -------------------------------------------------
def apply_custom_style():
    st.markdown("""
    <style>
    .main {
        background: radial-gradient(circle at top left, #111827 0%, #0E1117 45%, #090C10 100%);
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B1220 0%, #111827 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }

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
        0% { box-shadow: 0 0 0px rgba(79,139,249,0.10); }
        50% { box-shadow: 0 0 22px rgba(79,139,249,0.22); }
        100% { box-shadow: 0 0 0px rgba(79,139,249,0.10); }
    }

    .hero-box {
        padding: 2rem;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(28,31,38,0.96), rgba(17,24,39,0.96));
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 18px 42px rgba(0,0,0,0.32);
        margin-bottom: 1.2rem;
        animation: fadeInUp 0.85s ease-out;
        position: relative;
        overflow: hidden;
    }

    .hero-box::after {
        content: "";
        position: absolute;
        top: -70px;
        right: -50px;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(79,139,249,0.16), transparent 70%);
        border-radius: 50%;
    }

    .page-title {
        font-size: 2.2rem;
        font-weight: 900;
        color: #FAFAFA;
        margin-bottom: 0.45rem;
    }

    .page-subtitle {
        font-size: 1rem;
        color: #C9D1D9;
        line-height: 1.8;
        max-width: 850px;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 800;
        color: #FAFAFA;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
        animation: fadeInUp 0.8s ease-out;
    }

    .premium-card {
        padding: 1.35rem;
        border-radius: 22px;
        background: linear-gradient(135deg, #1A1F2B 0%, #141922 100%);
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 10px 28px rgba(0,0,0,0.22);
        animation: fadeInUp 0.85s ease-out;
        margin-bottom: 1rem;
    }

    .info-strip {
        padding: 1rem 1.2rem;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(79,139,249,0.10), rgba(127,179,255,0.06));
        border: 1px solid rgba(79,139,249,0.22);
        color: #DCE8FF;
        margin-top: 0.8rem;
        margin-bottom: 1rem;
        animation: fadeInUp 0.85s ease-out;
    }

    .mini-card {
        padding: 1rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #171C26 0%, #11161F 100%);
        border: 1px solid rgba(255,255,255,0.06);
        box-shadow: 0 8px 20px rgba(0,0,0,0.18);
        animation: fadeInUp 0.95s ease-out;
        min-height: 140px;
    }

    .mini-card-title {
        font-size: 1rem;
        font-weight: 800;
        color: #FAFAFA;
        margin-bottom: 0.5rem;
    }

    .mini-card-text {
        font-size: 0.92rem;
        color: #C9D1D9;
        line-height: 1.7;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 14px;
        font-weight: 700;
        padding: 0.7rem 1rem;
        border: 1px solid rgba(79,139,249,0.26);
        background: linear-gradient(135deg, #1B2535, #162030);
        color: white;
    }

    div.stButton > button:hover {
        border-color: rgba(127,179,255,0.45);
        box-shadow: 0 0 18px rgba(79,139,249,0.12);
    }

    div[data-baseweb="select"] > div,
    .stTextInput > div > div > input,
    .stTextArea textarea {
        border-radius: 14px !important;
    }

    div[data-testid="stForm"] {
        background: linear-gradient(135deg, #161B22 0%, #121720 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 22px;
        padding: 1.2rem;
        box-shadow: 0 10px 24px rgba(0,0,0,0.22);
        animation: fadeInUp 1s ease-out;
    }

    div[data-testid="stSuccessMessage"] {
        border-radius: 14px;
    }
    </style>
    """, unsafe_allow_html=True)


apply_custom_style()


# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown("""
<div class="hero-box">
    <div class="page-title">💬 Share Your Feedback</div>
    <div class="page-subtitle">
        Your feedback helps improve the sentiment analysis platform. You can rate the experience,
        report issues, suggest improvements, and share how useful the application was for your work or learning.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-strip">
<b>Why feedback matters:</b> This platform is designed for accessibility, transparency, and practical usability.
Your suggestions can help improve the interface, workflow, and analytical experience for future users.
</div>
""", unsafe_allow_html=True)


# -------------------------------------------------
# Top Info Cards
# -------------------------------------------------
c1, c2, c3 = st.columns(3, gap="large")

with c1:
    st.markdown("""
    <div class="mini-card">
        <div class="mini-card-title">⭐ Rate the Experience</div>
        <div class="mini-card-text">
            Share your overall impression of the platform’s design, usability, and usefulness.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="mini-card">
        <div class="mini-card-title">🛠 Report Issues</div>
        <div class="mini-card-text">
            Let us know if you encountered bugs, confusing workflows, or technical limitations.
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="mini-card">
        <div class="mini-card-title">🚀 Suggest Improvements</div>
        <div class="mini-card-text">
            Recommend features, visual enhancements, or workflow changes that would strengthen the app.
        </div>
    </div>
    """, unsafe_allow_html=True)


# -------------------------------------------------
# Feedback Form
# -------------------------------------------------
st.markdown('<div class="section-title">Feedback Form</div>', unsafe_allow_html=True)

with st.form("feedback_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        user_name = st.text_input("Your name (optional)")
        user_role = st.selectbox(
            "Your role",
            [
                "Student",
                "Researcher",
                "Business User",
                "Educator",
                "Developer",
                "Other"
            ]
        )
        overall_rating = st.slider(
            "Overall rating",
            min_value=1,
            max_value=5,
            value=4,
            help="1 = Poor, 5 = Excellent"
        )

    with col2:
        primary_use = st.selectbox(
            "Primary purpose of using the app",
            [
                "Educational learning",
                "Project work",
                "Research demonstration",
                "Business analysis",
                "General exploration"
            ]
        )
        ease_of_use = st.slider(
            "Ease of use rating",
            min_value=1,
            max_value=5,
            value=4
        )
        design_rating = st.slider(
            "Design and visual experience rating",
            min_value=1,
            max_value=5,
            value=4
        )

    liked_features = st.multiselect(
        "Which features did you like most?",
        [
            "Upload and cleaning workflow",
            "Missing value analysis",
            "Text cleaning options",
            "Domain selection",
            "DistilBERT sentiment analysis",
            "Results dashboard",
            "Charts and visualisations",
            "Overall design"
        ]
    )

    issue_type = st.selectbox(
        "Did you face any issues?",
        [
            "No issues",
            "Performance issue",
            "Upload issue",
            "Cleaning workflow issue",
            "Prediction issue",
            "Visual/dashboard issue",
            "Other"
        ]
    )

    feedback_message = st.text_area(
        "Your detailed feedback",
        placeholder="Share your experience, suggestions, or any issue you observed...",
        height=180
    )

    feature_request = st.text_area(
        "Feature request (optional)",
        placeholder="Example: export as Excel, add word cloud, more domain models, etc.",
        height=120
    )

    contact_email = st.text_input("Email (optional, if you want follow-up)")

    submit_feedback = st.form_submit_button("Submit Feedback")

# -------------------------------------------------
# Save Feedback
# -------------------------------------------------
def save_feedback_to_csv(feedback_row, file_path="user_feedback.csv"):
    feedback_df = pd.DataFrame([feedback_row])

    if os.path.exists(file_path):
        existing_df = pd.read_csv(file_path)
        updated_df = pd.concat([existing_df, feedback_df], ignore_index=True)
        updated_df.to_csv(file_path, index=False)
    else:
        feedback_df.to_csv(file_path, index=False)


if submit_feedback:
    if not feedback_message.strip():
        st.error("Please provide your feedback before submitting.")
    else:
        feedback_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_name": user_name,
            "user_role": user_role,
            "primary_use": primary_use,
            "overall_rating": overall_rating,
            "ease_of_use": ease_of_use,
            "design_rating": design_rating,
            "liked_features": ", ".join(liked_features) if liked_features else "",
            "issue_type": issue_type,
            "feedback_message": feedback_message,
            "feature_request": feature_request,
            "contact_email": contact_email
        }

        save_feedback_to_csv(feedback_data)

        st.success("✅ Thank you! Your feedback has been submitted successfully.")

        st.markdown("""
        <div class="info-strip">
        <b>Feedback recorded successfully.</b><br>
        Your input will help improve the app’s usability, interface design, and sentiment analysis workflow.
        </div>
        """, unsafe_allow_html=True)


# -------------------------------------------------
# Optional Footer Panel
# -------------------------------------------------
st.markdown('<div class="section-title">What Happens Next?</div>', unsafe_allow_html=True)

st.markdown("""
<div class="premium-card">
    <div style="font-size:1.05rem; font-weight:800; color:#FAFAFA; margin-bottom:0.6rem;">
        📌 Feedback Review Process
    </div>
    <div style="font-size:0.95rem; color:#C9D1D9; line-height:1.8;">
        Submitted feedback can be used to refine the design, improve analysis workflows, enhance visual dashboards,
        and prioritise future features such as additional export formats, improved domain support, and richer analytics.
    </div>
</div>
""", unsafe_allow_html=True)
