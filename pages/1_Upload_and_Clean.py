import re
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
        Upload a CSV or Excel file, inspect missing values, choose specific columns to clean,
        apply text-cleaning rules, and compare messy and cleaned data side by side.
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your dataset (CSV or Excel)", type=["csv", "xlsx"])


# -----------------------------
# Helper functions
# -----------------------------
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    return None


def dataset_profile(df):
    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Duplicate Rows": int(df.duplicated().sum()),
        "Missing Cells": int(df.isnull().sum().sum())
    }


def get_missing_summary(df):
    missing_counts = df.isnull().sum()
    missing_percent = (missing_counts / len(df)) * 100 if len(df) > 0 else 0

    summary_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": missing_counts.values,
        "Missing Percentage": missing_percent.values
    })

    summary_df = summary_df[summary_df["Missing Values"] > 0].sort_values(
        by="Missing Values", ascending=False
    )
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


def clean_text_value(
    text,
    remove_hashtags=False,
    remove_mentions=False,
    remove_commas=False,
    remove_urls=False,
    remove_special_chars=False,
    remove_extra_spaces=True,
    text_case_option="None"
):
    if pd.isna(text):
        return text

    text = str(text)

    if remove_urls:
        text = re.sub(r"http\\S+|www\\S+", "", text)

    if remove_hashtags:
        text = re.sub(r"#\\w+", "", text)

    if remove_mentions:
        text = re.sub(r"@\\w+", "", text)

    if remove_commas:
        text = text.replace(",", "")

    if remove_special_chars:
        text = re.sub(r"[^A-Za-z0-9\\s]", "", text)

    if remove_extra_spaces:
        text = re.sub(r"\\s+", " ", text).strip()

    if text_case_option == "Lowercase":
        text = text.lower()
    elif text_case_option == "Uppercase":
        text = text.upper()
    elif text_case_option == "Title Case":
        text = text.title()

    return text


def clean_selected_text_columns(
    df,
    selected_text_columns,
    preserve_original,
    remove_hashtags,
    remove_mentions,
    remove_commas,
    remove_urls,
    remove_special_chars,
    remove_extra_spaces,
    text_case_option
):
    cleaned_df = df.copy()

    comparison_frames = []

    for col in selected_text_columns:
        cleaned_series = cleaned_df[col].apply(
            lambda x: clean_text_value(
                x,
                remove_hashtags=remove_hashtags,
                remove_mentions=remove_mentions,
                remove_commas=remove_commas,
                remove_urls=remove_urls,
                remove_special_chars=remove_special_chars,
                remove_extra_spaces=remove_extra_spaces,
                text_case_option=text_case_option
            )
        )

        if preserve_original:
            new_col_name = f"{col}_cleaned"
            cleaned_df[new_col_name] = cleaned_series
            comparison_df = pd.DataFrame({
                f"{col}_messy": cleaned_df[col],
                f"{col}_cleaned": cleaned_df[new_col_name]
            })
        else:
            original_series = cleaned_df[col].copy()
            cleaned_df[col] = cleaned_series
            comparison_df = pd.DataFrame({
                f"{col}_messy": original_series,
                f"{col}_cleaned": cleaned_df[col]
            })

        comparison_frames.append((col, comparison_df))

    return cleaned_df, comparison_frames


def basic_structure_clean(df):
    cleaned_df = df.copy()
    cleaned_df = cleaned_df.dropna(how="all")
    cleaned_df.columns = [str(col).strip() for col in cleaned_df.columns]

    for col in cleaned_df.select_dtypes(include=["object"]).columns:
        cleaned_df[col] = cleaned_df[col].replace(["", "nan", "None", "null"], np.nan)

    cleaned_df = cleaned_df.dropna(how="all")
    return cleaned_df


def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")


# -----------------------------
# Main App
# -----------------------------
if uploaded_file is None:
    st.markdown('<div class="info-box">Please upload a dataset to begin.</div>', unsafe_allow_html=True)

else:
    try:
        df = load_data(uploaded_file)

        if df is None:
            st.error("Unsupported file format.")
            st.stop()

        st.success("Dataset uploaded successfully.")

        # Original profile
        profile = dataset_profile(df)
        a, b, c, d = st.columns(4)
        a.metric("Rows", profile["Rows"])
        b.metric("Columns", profile["Columns"])
        c.metric("Duplicate Rows", profile["Duplicate Rows"])
        d.metric("Missing Cells", profile["Missing Cells"])

        st.markdown('<div class="section-title">Original Dataset Preview</div>', unsafe_allow_html=True)
        st.dataframe(df.head(100), use_container_width=True)

        # Missing value analysis
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

        # General cleaning
        remove_fully_empty_rows = st.checkbox("Remove fully empty rows", value=True)
        remove_duplicates = st.checkbox("Remove duplicate rows", value=True)
        remove_rows_with_missing = st.checkbox("Remove rows with any missing values", value=False)

        # Missing value filling
        st.markdown("### Missing Value Handling")
        columns_with_missing = df.columns[df.isnull().sum() > 0].tolist()
        selected_missing_columns = st.multiselect(
            "Select columns to fill missing values",
            columns_with_missing
        )

        column_strategies = {}
        for col in selected_missing_columns:
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

            column_strategies[col] = {
                "strategy": strategy,
                "custom_value": custom_value
            }

        # Text cleaning section
        st.markdown("### Text Cleaning Options")

        text_columns = df.select_dtypes(include=["object"]).columns.tolist()
        selected_text_columns = st.multiselect(
            "Select text columns to clean",
            text_columns
        )

        preserve_original = st.checkbox(
            "Preserve original columns and create new cleaned columns",
            value=True
        )

        text_case_option = st.selectbox(
            "Text standardisation",
            ["None", "Lowercase", "Uppercase", "Title Case"]
        )

        remove_hashtags = st.checkbox("Remove hashtags (#example)", value=False)
        remove_mentions = st.checkbox("Remove mentions (@user)", value=False)
        remove_commas = st.checkbox("Remove commas", value=False)
        remove_urls = st.checkbox("Remove URLs", value=False)
        remove_special_chars = st.checkbox("Remove special characters", value=False)
        remove_extra_spaces = st.checkbox("Remove extra spaces", value=True)

        # Run cleaning
        if st.button("Clean Dataset", type="primary"):
            cleaned_df = df.copy()

            if remove_fully_empty_rows:
                cleaned_df = cleaned_df.dropna(how="all")

            cleaned_df = basic_structure_clean(cleaned_df)

            if remove_duplicates:
                cleaned_df = cleaned_df.drop_duplicates()

            if remove_rows_with_missing:
                cleaned_df = cleaned_df.dropna()
            else:
                for col, config in column_strategies.items():
                    cleaned_df = fill_column_values(
                        cleaned_df,
                        col,
                        config["strategy"],
                        config["custom_value"]
                    )

            comparison_frames = []
            if selected_text_columns:
                cleaned_df, comparison_frames = clean_selected_text_columns(
                    cleaned_df,
                    selected_text_columns,
                    preserve_original,
                    remove_hashtags,
                    remove_mentions,
                    remove_commas,
                    remove_urls,
                    remove_special_chars,
                    remove_extra_spaces,
                    text_case_option
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

            # Comparison view
            if comparison_frames:
                st.markdown('<div class="section-title">Messy vs Cleaned Column Comparison</div>', unsafe_allow_html=True)

                selected_compare_col = st.selectbox(
                    "Select a cleaned text column to compare",
                    [col_name for col_name, _ in comparison_frames]
                )

                for col_name, compare_df in comparison_frames:
                    if col_name == selected_compare_col:
                        st.dataframe(compare_df.head(100), use_container_width=True)
                        break

            csv_data = convert_df_to_csv(cleaned_df)
            st.download_button(
                "Download Cleaned Dataset as CSV",
                data=csv_data,
                file_name="cleaned_dataset.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Error loading or processing file: {e}")
