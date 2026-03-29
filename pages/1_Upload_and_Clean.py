def apply_custom_style():
    st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero-box {
        padding: 2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #1C1F26, #111827);
        box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        margin-bottom: 1.5rem;
    }

    .page-title {
        font-size: 2.3rem;
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
        font-size: 1.35rem;
        font-weight: 700;
        color: #FAFAFA;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    .feature-card {
        padding: 1.25rem;
        border-radius: 18px;
        background-color: #1C1F26;
        box-shadow: 0 6px 18px rgba(0,0,0,0.25);
        border: 1px solid #2A2F3A;
        margin-bottom: 1rem;
    }

    .feature-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #FAFAFA;
        margin-bottom: 0.5rem;
    }

    .feature-text {
        font-size: 0.95rem;
        color: #C9D1D9;
        line-height: 1.6;
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

    div.stDownloadButton > button {
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

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Upload and Clean", page_icon="📂", layout="wide")

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
    div.stButton > button, div.stDownloadButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 600;
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

st.markdown("""
<div class="hero-box">
    <div class="page-title">📂 Upload and Clean Dataset</div>
    <div class="page-subtitle">
        Upload a CSV or Excel file, inspect data quality issues, handle missing values, standardise text,
        and download the refined dataset for sentiment analysis.
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your dataset (CSV or Excel)", type=["csv", "xlsx"])

def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    return None

def basic_clean_dataframe(df, text_case_option):
    cleaned_df = df.copy()
    cleaned_df = cleaned_df.dropna(how="all")
    cleaned_df.columns = [str(col).strip() for col in cleaned_df.columns]

    for col in cleaned_df.select_dtypes(include=["object"]).columns:
        cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
        cleaned_df[col] = cleaned_df[col].replace(["", "nan", "None", "null"], np.nan)

        if text_case_option == "Lowercase":
            cleaned_df[col] = cleaned_df[col].apply(lambda x: x.lower() if isinstance(x, str) else x)
        elif text_case_option == "Uppercase":
            cleaned_df[col] = cleaned_df[col].apply(lambda x: x.upper() if isinstance(x, str) else x)
        elif text_case_option == "Title Case":
            cleaned_df[col] = cleaned_df[col].apply(lambda x: x.title() if isinstance(x, str) else x)

    cleaned_df = cleaned_df.dropna(how="all")
    return cleaned_df

def get_missing_summary(df):
    missing_counts = df.isnull().sum()
    missing_percent = (missing_counts / len(df)) * 100 if len(df) > 0 else 0
    summary_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": missing_counts.values,
        "Missing Percentage": missing_percent.values
    })
    summary_df = summary_df[summary_df["Missing Values"] > 0].sort_values(by="Missing Values", ascending=False)
    return summary_df

def fill_column_values(df, column, strategy, custom_value=None):
    series = df[column]
    if strategy == "Mean" and pd.api.types.is_numeric_dtype(series):
        df[column] = series.fillna(series.mean())
    elif strategy == "Median" and pd.api.types.is_numeric_dtype(series):
        df[column] = series.fillna(series.median())
    elif strategy == "Mode":
        mode_series = series.mode()
        if not mode_series.empty:
            df[column] = series.fillna(mode_series.iloc[0])
    elif strategy == "Custom Value":
        df[column] = series.fillna(custom_value)
    return df

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

def dataset_profile(df):
    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Duplicate Rows": int(df.duplicated().sum()),
        "Missing Cells": int(df.isnull().sum().sum())
    }

if uploaded_file is None:
    st.markdown('<div class="info-box">Please upload a dataset to begin.</div>', unsafe_allow_html=True)
else:
    try:
        df = load_data(uploaded_file)
        if df is None:
            st.error("Unsupported file format.")
            st.stop()

        st.success("Dataset uploaded successfully.")

        profile = dataset_profile(df)
        a, b, c, d = st.columns(4)
        a.metric("Rows", profile["Rows"])
        b.metric("Columns", profile["Columns"])
        c.metric("Duplicate Rows", profile["Duplicate Rows"])
        d.metric("Missing Cells", profile["Missing Cells"])

        st.markdown('<div class="section-title">Original Dataset Preview</div>', unsafe_allow_html=True)
        st.dataframe(df.head(100), use_container_width=True)

        st.markdown('<div class="section-title">Missing Values Analysis</div>', unsafe_allow_html=True)
        missing_summary = get_missing_summary(df)

        if not missing_summary.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(missing_summary, use_container_width=True)

            with col2:
                fig_pie = px.pie(
                    missing_summary,
                    names="Column",
                    values="Missing Values",
                    title="Columns Contributing to Missing Values",
                    hole=0.45
                )
                fig_pie.update_traces(textposition="inside", textinfo="percent+label")
                st.plotly_chart(fig_pie, use_container_width=True)

            fig_bar = px.bar(
                missing_summary,
                x="Column",
                y="Missing Values",
                title="Missing Values by Column",
                text="Missing Values"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.success("No missing values found in the uploaded dataset.")

        st.markdown('<div class="section-title">Cleaning Configuration</div>', unsafe_allow_html=True)

        remove_fully_empty_rows = st.checkbox("Remove fully empty rows", value=True)
        remove_duplicates = st.checkbox("Remove duplicate rows", value=True)
        remove_rows_with_missing = st.checkbox("Remove rows with any missing values", value=False)

        text_case_option = st.selectbox(
            "Text standardisation",
            ["None", "Lowercase", "Uppercase", "Title Case"]
        )

        columns_with_missing = df.columns[df.isnull().sum() > 0].tolist()
        selected_columns = st.multiselect("Select columns to fill missing values", columns_with_missing)

        column_strategies = {}
        for col in selected_columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                strategy = st.selectbox(
                    f"Choose fill method for {col}",
                    ["Mean", "Median", "Mode", "Custom Value"],
                    key=f"strategy_{col}"
                )
            else:
                strategy = st.selectbox(
                    f"Choose fill method for {col}",
                    ["Mode", "Custom Value"],
                    key=f"strategy_{col}"
                )

            custom_value = None
            if strategy == "Custom Value":
                custom_value = st.text_input(
                    f"Enter custom value for {col}",
                    value="Unknown",
                    key=f"custom_{col}"
                )

            column_strategies[col] = {"strategy": strategy, "custom_value": custom_value}

        if st.button("Clean Dataset", type="primary"):
            cleaned_df = df.copy()

            if remove_fully_empty_rows:
                cleaned_df = cleaned_df.dropna(how="all")

            cleaned_df = basic_clean_dataframe(cleaned_df, text_case_option)

            if remove_duplicates:
                cleaned_df = cleaned_df.drop_duplicates()

            if remove_rows_with_missing:
                cleaned_df = cleaned_df.dropna()
            else:
                for col, config in column_strategies.items():
                    cleaned_df = fill_column_values(
                        cleaned_df, col, config["strategy"], config["custom_value"]
                    )

            st.session_state["cleaned_data"] = cleaned_df

            cleaned_profile = dataset_profile(cleaned_df)
            e, f, g, h = st.columns(4)
            e.metric("Rows", cleaned_profile["Rows"])
            f.metric("Columns", cleaned_profile["Columns"])
            g.metric("Duplicate Rows", cleaned_profile["Duplicate Rows"])
            h.metric("Missing Cells", cleaned_profile["Missing Cells"])

            st.markdown('<div class="section-title">Cleaned Dataset Preview</div>', unsafe_allow_html=True)
            st.dataframe(cleaned_df.head(100), use_container_width=True)

            csv_data = convert_df_to_csv(cleaned_df)
            st.download_button(
                "Download Cleaned Dataset as CSV",
                data=csv_data,
                file_name="cleaned_dataset.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Error loading or processing file: {e}")

