import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)

st.set_page_config(page_title="Results Dashboard", page_icon="📊", layout="wide")


# -------------------------------------------------
# Custom Styling
# -------------------------------------------------
def apply_custom_style():
    st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    .hero-box {
        padding: 1.8rem;
        border-radius: 22px;
        background: linear-gradient(135deg, #1C1F26, #111827);
        box-shadow: 0 8px 28px rgba(0,0,0,0.35);
        margin-bottom: 1.4rem;
        animation: fadeInUp 0.8s ease-in-out;
    }

    .page-title {
        font-size: 2.1rem;
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
        font-size: 1.25rem;
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
        animation: fadeInUp 0.8s ease-in-out;
    }

    .metric-card {
        background: linear-gradient(135deg, #1C1F26, #161B22);
        border: 1px solid #2A2F3A;
        border-radius: 18px;
        padding: 1rem;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
        animation: fadeInUp 0.8s ease-in-out;
    }

    .metric-title {
        font-size: 0.9rem;
        color: #9BA3AF;
        margin-bottom: 0.25rem;
    }

    .metric-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #FAFAFA;
    }

    .metric-sub {
        font-size: 0.85rem;
        color: #C9D1D9;
        margin-top: 0.25rem;
    }

    div.stButton > button, div.stDownloadButton > button {
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

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0px);
        }
    }
    </style>
    """, unsafe_allow_html=True)


apply_custom_style()


# -------------------------------------------------
# Helper Functions
# -------------------------------------------------
def safe_classification_metrics(y_true, y_pred):
    """
    Compute overall weighted precision, recall, and F1 safely.
    """
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="weighted", zero_division=0
    )
    acc = accuracy_score(y_true, y_pred)
    return acc, precision, recall, f1


def make_metric_card(title, value, subtitle=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def to_csv_bytes(df: pd.DataFrame):
    return df.to_csv(index=False).encode("utf-8")


# -------------------------------------------------
# Page Header
# -------------------------------------------------
st.markdown("""
<div class="hero-box">
    <div class="page-title">📊 Results Dashboard</div>
    <div class="page-subtitle">
        Explore prediction outcomes, confidence patterns, evaluation metrics, and downloadable results
        through an interactive and user-friendly dashboard.
    </div>
</div>
""", unsafe_allow_html=True)


# -------------------------------------------------
# Load Results
# -------------------------------------------------
if "analysis_results" not in st.session_state:
    st.markdown(
        '<div class="info-box">No analysis results found. Please complete the <b>Sentiment Analysis</b> page first.</div>',
        unsafe_allow_html=True
    )
    st.stop()

results_df = st.session_state["analysis_results"].copy()
text_column = st.session_state.get("text_column", None)
label_column = st.session_state.get("label_column", "None")
domain = st.session_state.get("domain", "General")
model_name = st.session_state.get("model_name", "DistilBERT")

if results_df.empty:
    st.error("The analysis results are empty. Please return to Page 2 and run sentiment analysis.")
    st.stop()


# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------
st.sidebar.markdown("## Dashboard Filters")

predicted_filter = st.sidebar.multiselect(
    "Filter by predicted sentiment",
    options=sorted(results_df["predicted_sentiment"].dropna().unique().tolist()),
    default=sorted(results_df["predicted_sentiment"].dropna().unique().tolist())
)

min_confidence = st.sidebar.slider(
    "Minimum confidence score",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.01
)

filtered_df = results_df[
    results_df["predicted_sentiment"].isin(predicted_filter) &
    (results_df["confidence_score"] >= min_confidence)
].copy()

if filtered_df.empty:
    st.warning("No rows match the selected filters. Please adjust the sidebar filters.")
    st.stop()


# -------------------------------------------------
# Summary Info
# -------------------------------------------------
st.markdown(f"""
<div class="info-box">
<b>Domain:</b> {domain}<br>
<b>Model:</b> {model_name}<br>
<b>Rows Displayed:</b> {len(filtered_df)} / {len(results_df)}<br>
<b>Text Column:</b> {text_column}
</div>
""", unsafe_allow_html=True)


# -------------------------------------------------
# Key Metrics
# -------------------------------------------------
m1, m2, m3, m4 = st.columns(4)

with m1:
    make_metric_card("Rows Analysed", f"{len(filtered_df):,}", "Filtered result set")

with m2:
    avg_conf = filtered_df["confidence_score"].mean()
    make_metric_card("Average Confidence", f"{avg_conf:.2%}", "Mean model confidence")

with m3:
    top_sentiment = filtered_df["predicted_sentiment"].mode().iloc[0]
    make_metric_card("Top Predicted Sentiment", top_sentiment.title(), "Most frequent class")

with m4:
    unique_preds = filtered_df["predicted_sentiment"].nunique()
    make_metric_card("Predicted Classes", str(unique_preds), "Distinct sentiment outputs")


# -------------------------------------------------
# Tabs
# -------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Overview",
    "🧪 Evaluation",
    "🔍 Prediction Explorer",
    "⬇️ Download Results"
])


# -------------------------------------------------
# TAB 1: Overview
# -------------------------------------------------
with tab1:
    st.markdown('<div class="section-title">Predicted Sentiment Distribution</div>', unsafe_allow_html=True)

    pred_counts = (
        filtered_df["predicted_sentiment"]
        .value_counts()
        .reset_index()
    )
    pred_counts.columns = ["Sentiment", "Count"]

    c1, c2 = st.columns(2)

    with c1:
        fig_bar = px.bar(
            pred_counts,
            x="Sentiment",
            y="Count",
            color="Sentiment",
            text="Count",
            title="Predicted Sentiment Counts",
            template="plotly_dark"
        )
        fig_bar.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font_color="#FAFAFA"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with c2:
        fig_pie = px.pie(
            pred_counts,
            names="Sentiment",
            values="Count",
            hole=0.5,
            title="Predicted Sentiment Share",
            template="plotly_dark"
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        fig_pie.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font_color="#FAFAFA"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown('<div class="section-title">Confidence Score Distribution</div>', unsafe_allow_html=True)

    fig_hist = px.histogram(
        filtered_df,
        x="confidence_score",
        nbins=30,
        color="predicted_sentiment",
        title="Confidence Score Distribution by Predicted Sentiment",
        template="plotly_dark"
    )
    fig_hist.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font_color="#FAFAFA"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    if label_column != "None" and "true_label" in filtered_df.columns and filtered_df["true_label"].notna().any():
        st.markdown('<div class="section-title">True vs Predicted Label Comparison</div>', unsafe_allow_html=True)

        compare_df = (
            filtered_df.groupby(["true_label", "predicted_sentiment"])
            .size()
            .reset_index(name="Count")
        )

        fig_compare = px.bar(
            compare_df,
            x="true_label",
            y="Count",
            color="predicted_sentiment",
            barmode="group",
            title="True Label vs Predicted Sentiment",
            template="plotly_dark"
        )
        fig_compare.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font_color="#FAFAFA"
        )
        st.plotly_chart(fig_compare, use_container_width=True)


# -------------------------------------------------
# TAB 2: Evaluation
# -------------------------------------------------
with tab2:
    if label_column == "None" or "true_label" not in filtered_df.columns or not filtered_df["true_label"].notna().any():
        st.markdown(
            '<div class="info-box">No valid true labels are available for evaluation. Please select a label column on Page 2.</div>',
            unsafe_allow_html=True
        )
    else:
        eval_df = filtered_df.dropna(subset=["true_label", "predicted_sentiment"]).copy()

        if eval_df.empty:
            st.warning("No rows available for evaluation after removing missing labels.")
        else:
            y_true = eval_df["true_label"].astype(str).tolist()
            y_pred = eval_df["predicted_sentiment"].astype(str).tolist()

            acc, precision, recall, f1 = safe_classification_metrics(y_true, y_pred)

            e1, e2, e3, e4 = st.columns(4)
            with e1:
                make_metric_card("Accuracy", f"{acc:.2%}", "Overall correctness")
            with e2:
                make_metric_card("Precision", f"{precision:.2%}", "Weighted precision")
            with e3:
                make_metric_card("Recall", f"{recall:.2%}", "Weighted recall")
            with e4:
                make_metric_card("F1-Score", f"{f1:.2%}", "Weighted F1")

            st.markdown('<div class="section-title">Confusion Matrix</div>', unsafe_allow_html=True)

            labels = sorted(list(set(y_true) | set(y_pred)))
            cm = confusion_matrix(y_true, y_pred, labels=labels)
            cm_df = pd.DataFrame(cm, index=labels, columns=labels)

            fig_cm = px.imshow(
                cm_df,
                text_auto=True,
                color_continuous_scale="Blues",
                title="Confusion Matrix",
                template="plotly_dark"
            )
            fig_cm.update_layout(
                xaxis_title="Predicted Label",
                yaxis_title="True Label",
                paper_bgcolor="#0E1117",
                plot_bgcolor="#0E1117",
                font_color="#FAFAFA"
            )
            st.plotly_chart(fig_cm, use_container_width=True)

            st.markdown('<div class="section-title">Detailed Classification Report</div>', unsafe_allow_html=True)

            report_dict = classification_report(
                y_true, y_pred, output_dict=True, zero_division=0
            )
            report_df = pd.DataFrame(report_dict).transpose().reset_index()
            report_df.rename(columns={"index": "Class"}, inplace=True)

            st.dataframe(report_df, use_container_width=True)


# -------------------------------------------------
# TAB 3: Prediction Explorer
# -------------------------------------------------
with tab3:
    st.markdown('<div class="section-title">Prediction Explorer</div>', unsafe_allow_html=True)

    view_sentiment = st.selectbox(
        "Select sentiment to inspect",
        options=["All"] + sorted(filtered_df["predicted_sentiment"].dropna().unique().tolist())
    )

    explorer_df = filtered_df.copy()
    if view_sentiment != "All":
        explorer_df = explorer_df[explorer_df["predicted_sentiment"] == view_sentiment]

    sort_option = st.selectbox(
        "Sort rows by confidence",
        ["Highest confidence first", "Lowest confidence first"]
    )

    ascending_order = sort_option == "Lowest confidence first"
    explorer_df = explorer_df.sort_values(by="confidence_score", ascending=ascending_order)

    preview_columns = [text_column, "predicted_sentiment", "confidence_score"]
    if "true_label" in explorer_df.columns and explorer_df["true_label"].notna().any():
        preview_columns.insert(1, "true_label")

    st.dataframe(explorer_df[preview_columns].head(200), use_container_width=True)

    st.markdown('<div class="section-title">Top Sample Predictions</div>', unsafe_allow_html=True)

    sample_preview = explorer_df[preview_columns].head(5)

    for idx, row in sample_preview.iterrows():
        text_val = row[text_column]
        pred_val = row["predicted_sentiment"]
        conf_val = row["confidence_score"]
        true_val = row["true_label"] if "true_label" in row else "N/A"

        st.markdown(f"""
        <div class="info-box">
        <b>Predicted:</b> {pred_val.title()} &nbsp; | &nbsp;
        <b>Confidence:</b> {conf_val:.2%} &nbsp; | &nbsp;
        <b>True Label:</b> {true_val if pd.notna(true_val) else "N/A"}<br><br>
        <b>Text:</b> {text_val}
        </div>
        """, unsafe_allow_html=True)


# -------------------------------------------------
# TAB 4: Download Results
# -------------------------------------------------
with tab4:
    st.markdown('<div class="section-title">Download Enriched Results</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    Download the full enriched results dataset, including predicted sentiment, confidence scores,
    selected domain, and model information.
    </div>
    """, unsafe_allow_html=True)

    csv_bytes = to_csv_bytes(filtered_df)

    st.download_button(
        label="⬇️ Download Results as CSV",
        data=csv_bytes,
        file_name="sentiment_analysis_results.csv",
        mime="text/csv"
    )

    st.markdown('<div class="section-title">Result Summary Table</div>', unsafe_allow_html=True)
    st.dataframe(filtered_df.head(100), use_container_width=True)
