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

st.title("📂 Upload and Clean Dataset")

st.markdown("""
This page allows users to:

- upload a CSV or Excel dataset
- inspect data quality issues
- identify missing values by column
- preview rows affected by missing values
- clean duplicate and incomplete records
- apply column-wise missing value strategies
- standardise text formatting
- compare the dataset before and after cleaning
- download the cleaned dataset
""")


# -----------------------------
# File upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload your dataset (CSV or Excel)",
    type=["csv", "xlsx"]
)


# -----------------------------
# Helper functions
# -----------------------------
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    return None


def basic_clean_dataframe(df, text_case_option):
    cleaned_df = df.copy()

    # Remove fully empty rows
    cleaned_df = cleaned_df.dropna(how="all")

    # Clean column names
    cleaned_df.columns = [str(col).strip() for col in cleaned_df.columns]

    # Clean string columns
    for col in cleaned_df.select_dtypes(include=["object"]).columns:
        cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
        cleaned_df[col] = cleaned_df[col].replace(["", "nan", "None", "null"], np.nan)

        if text_case_option == "Lowercase":
            cleaned_df[col] = cleaned_df[col].apply(lambda x: x.lower() if isinstance(x, str) else x)
        elif text_case_option == "Uppercase":
            cleaned_df[col] = cleaned_df[col].apply(lambda x: x.upper() if isinstance(x, str) else x)
        elif text_case_option == "Title Case":
            cleaned_df[col] = cleaned_df[col].apply(lambda x: x.title() if isinstance(x, str) else x)

    # Remove fully empty rows again
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

    summary_df = summary_df[summary_df["Missing Values"] > 0].sort_values(
        by="Missing Values", ascending=False
    )
    return summary_df


def fill_column_values(df, column, strategy, custom_value=None):
    series = df[column]

    if strategy == "Mean":
        if pd.api.types.is_numeric_dtype(series):
            df[column] = series.fillna(series.mean())

    elif strategy == "Median":
        if pd.api.types.is_numeric_dtype(series):
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


# -----------------------------
# Main app
# -----------------------------
if uploaded_file is None:
    st.info("Please upload a dataset to begin.")

else:
    try:
        df = load_data(uploaded_file)

        if df is None:
            st.error("Unsupported file format.")
            st.stop()

        st.success("Dataset uploaded successfully.")

        # -----------------------------
        # Original dataset profile
        # -----------------------------
        st.subheader("Original Dataset Overview")

        profile = dataset_profile(df)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows", profile["Rows"])
        c2.metric("Columns", profile["Columns"])
        c3.metric("Duplicate Rows", profile["Duplicate Rows"])
        c4.metric("Missing Cells", profile["Missing Cells"])

        st.markdown("### Original Dataset Preview")
        st.dataframe(df.head(100), use_container_width=True)

        st.markdown("### Data Types")
        dtype_df = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str).values
        })
        st.dataframe(dtype_df, use_container_width=True)

        # -----------------------------
        # Missing value analysis
        # -----------------------------
        st.subheader("Missing Values Analysis")
        missing_summary = get_missing_summary(df)

        if not missing_summary.empty:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Missing Values Table")
                st.dataframe(missing_summary, use_container_width=True)

            with col2:
                st.markdown("#### Missing Values Pie Chart")
                fig_pie = px.pie(
                    missing_summary,
                    names="Column",
                    values="Missing Values",
                    title="Columns Contributing to Missing Values",
                    hole=0.45
                )
                fig_pie.update_traces(textposition="inside", textinfo="percent+label")
                st.plotly_chart(fig_pie, use_container_width=True)

            st.markdown("#### Missing Values Bar Chart")
            fig_bar = px.bar(
                missing_summary,
                x="Column",
                y="Missing Values",
                title="Missing Values by Column",
                text="Missing Values"
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            selected_missing_col = st.selectbox(
                "Preview rows with missing values in a selected column",
                missing_summary["Column"].tolist()
            )
            affected_rows = df[df[selected_missing_col].isnull()]
            st.dataframe(affected_rows.head(100), use_container_width=True)

        else:
            st.success("No missing values found in the uploaded dataset.")

        st.markdown("---")
        st.subheader("Cleaning Configuration")

        # -----------------------------
        # General cleaning options
        # -----------------------------
        remove_fully_empty_rows = st.checkbox("Remove fully empty rows", value=True)
        remove_duplicates = st.checkbox("Remove duplicate rows", value=True)
        remove_rows_with_missing = st.checkbox("Remove rows with any missing values", value=False)

        text_case_option = st.selectbox(
            "Text standardisation",
            ["None", "Lowercase", "Uppercase", "Title Case"]
        )

        # -----------------------------
        # Column-wise missing value strategies
        # -----------------------------
        st.markdown("### Column-wise Missing Value Handling")

        columns_with_missing = df.columns[df.isnull().sum() > 0].tolist()

        selected_columns = st.multiselect(
            "Select columns to fill missing values",
            columns_with_missing
        )

        column_strategies = {}

        for col in selected_columns:
            st.markdown(f"#### Column: `{col}`")
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

        # -----------------------------
        # Run cleaning
        # -----------------------------
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
                        cleaned_df,
                        col,
                        config["strategy"],
                        config["custom_value"]
                    )

            # -----------------------------
            # Results section
            # -----------------------------
            st.markdown("---")
            st.subheader("Cleaned Dataset Overview")

            cleaned_profile = dataset_profile(cleaned_df)
            d1, d2, d3, d4 = st.columns(4)
            d1.metric("Rows", cleaned_profile["Rows"])
            d2.metric("Columns", cleaned_profile["Columns"])
            d3.metric("Duplicate Rows", cleaned_profile["Duplicate Rows"])
            d4.metric("Missing Cells", cleaned_profile["Missing Cells"])

            st.markdown("### Before vs After Comparison")
            comparison_df = pd.DataFrame({
                "Metric": ["Rows", "Columns", "Duplicate Rows", "Missing Cells"],
                "Before Cleaning": [
                    profile["Rows"],
                    profile["Columns"],
                    profile["Duplicate Rows"],
                    profile["Missing Cells"]
                ],
                "After Cleaning": [
                    cleaned_profile["Rows"],
                    cleaned_profile["Columns"],
                    cleaned_profile["Duplicate Rows"],
                    cleaned_profile["Missing Cells"]
                ]
            })
            st.dataframe(comparison_df, use_container_width=True)

            st.markdown("### Cleaned Dataset Preview")
            st.dataframe(cleaned_df.head(100), use_container_width=True)

            st.markdown("### Remaining Missing Values")
            cleaned_missing_summary = get_missing_summary(cleaned_df)

            if not cleaned_missing_summary.empty:
                st.dataframe(cleaned_missing_summary, use_container_width=True)

                fig_after = px.pie(
                    cleaned_missing_summary,
                    names="Column",
                    values="Missing Values",
                    title="Remaining Missing Values After Cleaning",
                    hole=0.45
                )
                fig_after.update_traces(textposition="inside", textinfo="percent+label")
                st.plotly_chart(fig_after, use_container_width=True)
            else:
                st.success("No missing values remain after cleaning.")

            # Save in session state
            st.session_state["cleaned_data"] = cleaned_df

            # Download
            csv_data = convert_df_to_csv(cleaned_df)
            st.download_button(
                label="Download Cleaned Dataset as CSV",
                data=csv_data,
                file_name="cleaned_dataset.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Error loading or processing file: {e}")
