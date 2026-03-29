import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

st.set_page_config(page_title="Upload and Clean", page_icon="📂", layout="wide")

st.title("📂 Upload and Clean Dataset")

st.markdown("""
Upload a CSV or Excel dataset.  
This page allows you to:
- preview the raw dataset
- clean missing values
- remove duplicates
- standardize text columns
- view the cleaned dataset
- download the cleaned dataset
""")

uploaded_file = st.file_uploader(
    "Upload your dataset (CSV or Excel)",
    type=["csv", "xlsx"]
)

def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        return pd.read_excel(file)
    return None

def clean_dataframe(df):
    cleaned_df = df.copy()

    # Remove fully empty rows
    cleaned_df = cleaned_df.dropna(how="all")

    # Remove duplicate rows
    cleaned_df = cleaned_df.drop_duplicates()

    # Trim spaces from column names
    cleaned_df.columns = [col.strip() if isinstance(col, str) else col for col in cleaned_df.columns]

    # Clean object/string columns
    for col in cleaned_df.select_dtypes(include=["object"]).columns:
        cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
        cleaned_df[col] = cleaned_df[col].replace(["nan", "None", ""], np.nan)

    # Drop rows that are fully empty after cleanup
    cleaned_df = cleaned_df.dropna(how="all")

    return cleaned_df

def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)

        if df is not None:
            st.success("Dataset uploaded successfully.")

            st.subheader("Original Dataset Preview")
            st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
            st.dataframe(df, use_container_width=True)

            st.markdown("## Cleaning Options")

            remove_missing = st.checkbox("Remove rows with missing values", value=False)
            fill_missing = st.checkbox("Fill missing values", value=False)
            fill_value = st.text_input("Value to fill missing cells with", value="Unknown")

            if st.button("Clean Dataset"):
                cleaned_df = clean_dataframe(df)

                if remove_missing:
                    cleaned_df = cleaned_df.dropna()

                if fill_missing:
                    cleaned_df = cleaned_df.fillna(fill_value)

                st.subheader("Cleaned Dataset Preview")
                st.write(f"Rows: {cleaned_df.shape[0]}, Columns: {cleaned_df.shape[1]}")
                st.dataframe(cleaned_df, use_container_width=True)

                csv_data = convert_df_to_csv(cleaned_df)

                st.download_button(
                    label="Download Cleaned Dataset as CSV",
                    data=csv_data,
                    file_name="cleaned_dataset.csv",
                    mime="text/csv"
                )

                st.session_state["cleaned_data"] = cleaned_df

        else:
            st.error("Unsupported file format.")

    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("Please upload a dataset to begin.")
