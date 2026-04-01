import streamlit as st
import pandas as pd
import numpy as np
from transformers import pipeline

st.set_page_config(page_title="Sentiment Analysis", page_icon="🤖", layout="wide")


# -------------------------------------------------
# Custom Styling
# -------------------------------------------------
def apply_custom_style():
    st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .hero-box {
        padding: 1.7rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #1C1F26, #111827);
        box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        margin-bottom: 1.2rem;
    }
    .page-title {
        font-size: 2rem;
        font-weight: 800;
        color: #FAFAFA;
        margin-bottom: 0.4rem;
    }
    .page-subtitle {
        font-size: 1rem;
        color: #C9D1D9;
        line-height: 1.7;
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #FAFAFA;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }
    .info-box {
        padding: 1rem 1.2rem;
        border-radius: 14px;
        background-color: #161B22;
        border: 1px solid #30363D;
        color: #C9D1D9;
        margin-top: 0.8rem;
        margin-bottom: 1rem;
    }
    .stMetric {
        background-color: #1C1F26;
        border: 1px solid #2A2F3A;
        padding: 0.7rem;
        border-radius: 14px;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.6rem 1rem;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid #2A2F3A;
        border-radius: 12px;
        overflow: hidden;
    }
    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid #2A2F3A;
    }
    </style>
    """, unsafe_allow_html=True)


apply_custom_style()


# -------------------------------------------------
# Page Header
# -------------------------------------------------
st.markdown("""
<div class="hero-box">
    <div class="page-title">🤖 Sentiment Analysis Engine</div>
    <div class="page-subtitle">
        This page performs sentiment analysis using DistilBERT. 
        Select the text column, label column, and preferred domain, then run the model to generate predictions and confidence scores.
    </div>
</div>
""", unsafe_allow_html=True)


# -------------------------------------------------
# Helper Functions
# -------------------------------------------------
@st.cache_resource
def load_sentiment_model(model_name: str):
    """
    Load a Hugging Face text classification pipeline and cache it.
    """
    return pipeline(
        task="text-classification",
        model=model_name,
        tokenizer=model_name,
        truncation=True
    )


def normalize_true_label(value):
    """
    Normalize ground-truth labels into positive / negative / neutral.
    """
    value = str(value).strip().lower()

    mapping = {
        "positive": "positive",
        "pos": "positive",
        "1": "positive",
        "4": "positive",
        "5": "positive",

        "negative": "negative",
        "neg": "negative",
        "0": "negative",
        "1.0": "negative",
        "2": "negative",
        "2.0": "negative",

        "neutral": "neutral",
        "neu": "neutral",
        "3": "neutral",
        "3.0": "neutral"
    }

    return mapping.get(value, value)


def map_model_output(model_label: str):
    """
    Map model output to standard labels.
    Supports:
    - LABEL_0 / LABEL_1 / LABEL_2
    - NEGATIVE / POSITIVE / NEUTRAL
    """
    label = str(model_label).strip().lower()

    # Common 3-class mapping
    if label in {"label_0"}:
        return "negative"
    if label in {"label_1"}:
        return "neutral"
    if label in {"label_2"}:
        return "positive"

    # Common 2-class mapping
    if label == "negative":
        return "negative"
    if label == "positive":
        return "positive"
    if label == "neutral":
        return "neutral"

    # SST-style binary labels
    if label == "label_0":
        return "negative"
    if label == "label_1":
        return "positive"

    return label


def get_default_model_for_domain(domain_name: str):
    """
    Domain-aware model selection.
    You can later replace these with your own fine-tuned DistilBERT models.
    """
    domain_model_map = {
        "General": "cardiffnlp/twitter-roberta-base-sentiment-latest",
        "Student Feedback": "cardiffnlp/twitter-roberta-base-sentiment-latest",
        "Movie Reviews": "lvwerra/distilbert-imdb",
        "Product Reviews": "cardiffnlp/twitter-roberta-base-sentiment-latest",
        "Social Media": "cardiffnlp/twitter-roberta-base-sentiment-latest",
        "Customer Reviews": "cardiffnlp/twitter-roberta-base-sentiment-latest"
    }
    return domain_model_map.get(domain_name, "cardiffnlp/twitter-roberta-base-sentiment-latest")


def run_predictions(classifier, texts, batch_size=16):
    predicted_labels = []
    confidence_scores = []

    for start_idx in range(0, len(texts), batch_size):
        batch = texts[start_idx:start_idx + batch_size]
        results = classifier(batch)

        for item in results:
            predicted_labels.append(map_model_output(item["label"]))
            confidence_scores.append(float(item["score"]))

    return predicted_labels, confidence_scores


# -------------------------------------------------
# Main Logic
# -------------------------------------------------
if "cleaned_data" not in st.session_state:
    st.markdown(
        '<div class="info-box">No cleaned dataset found. Please complete the <b>Upload and Clean</b> page first.</div>',
        unsafe_allow_html=True
    )
    st.stop()

df = st.session_state["cleaned_data"].copy()

if df.empty:
    st.error("The cleaned dataset is empty. Please return to Page 1 and prepare a valid dataset.")
    st.stop()

# Profile
m1, m2, m3 = st.columns(3)
m1.metric("Rows Available", df.shape[0])
m2.metric("Columns Available", df.shape[1])
m3.metric("Workflow", "DistilBERT")

st.markdown('<div class="section-title">Dataset Preview</div>', unsafe_allow_html=True)
st.dataframe(df.head(100), use_container_width=True)

all_columns = df.columns.tolist()
text_columns = df.select_dtypes(include=["object"]).columns.tolist()

if not text_columns:
    st.error("No text columns were found in the cleaned dataset.")
    st.stop()

st.markdown('<div class="section-title">Analysis Configuration</div>', unsafe_allow_html=True)

left_col, right_col = st.columns(2)

with left_col:
    text_column = st.selectbox(
        "Select text column for sentiment analysis",
        text_columns
    )

    label_column_options = ["None"] + all_columns
    label_column = st.selectbox(
        "Select label column (optional but recommended for evaluation)",
        label_column_options
    )

with right_col:
    domain = st.selectbox(
        "Select preferred domain",
        [
            "General",
            "Student Feedback",
            "Movie Reviews",
            "Product Reviews",
            "Social Media",
            "Customer Reviews"
        ],
        index=0
    )

    use_default_domain_model = st.checkbox(
        "Use recommended model for selected domain",
        value=True
    )

if use_default_domain_model:
    selected_model_name = get_default_model_for_domain(domain)
else:
    selected_model_name = st.text_input(
        "Enter custom Hugging Face model name",
        value="cardiffnlp/twitter-roberta-base-sentiment-latest"
    )

st.markdown(f"""
<div class="info-box">
<b>Selected Domain:</b> {domain}<br>
<b>Selected Model:</b> {selected_model_name}<br>
<b>Text Column:</b> {text_column}<br>
<b>Label Column:</b> {label_column}
</div>
""", unsafe_allow_html=True)

max_rows = st.number_input(
    "Number of rows to analyse",
    min_value=1,
    max_value=int(len(df)),
    value=min(500, len(df)),
    step=1
)

batch_size = st.selectbox(
    "Batch size for inference",
    [8, 16, 32, 64],
    index=1
)

if st.button("Run Sentiment Analysis", type="primary"):
    try:
        analysis_df = df.head(max_rows).copy()

        # Prepare text
        analysis_df[text_column] = analysis_df[text_column].astype(str).fillna("").str.strip()
        analysis_df = analysis_df[analysis_df[text_column] != ""]

        if analysis_df.empty:
            st.error("No valid text rows available after cleaning.")
            st.stop()

        with st.spinner("Loading model and generating predictions..."):
            classifier = load_sentiment_model(selected_model_name)

            texts = analysis_df[text_column].tolist()
            predictions, confidence_scores = run_predictions(
                classifier=classifier,
                texts=texts,
                batch_size=batch_size
            )

        analysis_df["predicted_sentiment"] = predictions
        analysis_df["confidence_score"] = confidence_scores
        analysis_df["selected_domain"] = domain
        analysis_df["selected_model"] = selected_model_name

        # Normalize labels if user selected one
        if label_column != "None" and label_column in analysis_df.columns:
            analysis_df["true_label"] = analysis_df[label_column].apply(normalize_true_label)
        else:
            analysis_df["true_label"] = np.nan

        # Save to session state for Page 3
        st.session_state["analysis_results"] = analysis_df
        st.session_state["text_column"] = text_column
        st.session_state["label_column"] = label_column
        st.session_state["domain"] = domain
        st.session_state["model_name"] = selected_model_name

        st.success("Sentiment analysis completed successfully.")

        st.markdown('<div class="section-title">Prediction Preview</div>', unsafe_allow_html=True)
        preview_cols = [text_column, "predicted_sentiment", "confidence_score"]
        if label_column != "None" and "true_label" in analysis_df.columns:
            preview_cols.insert(1, "true_label")

        st.dataframe(analysis_df[preview_cols].head(100), use_container_width=True)

        st.info("Predictions have been saved. You can now move to the Results page.")

    except Exception as e:
        st.error(f"An error occurred during sentiment analysis: {e}")
