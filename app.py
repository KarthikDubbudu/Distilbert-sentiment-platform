import streamlit as st

st.set_page_config(
    page_title="Sentiment Analysis Platform",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Scalable Web-Based Sentiment Analysis Platform")
st.subheader("Leveraging DistilBERT for Labelled Text and Structured Feedback Data")

st.markdown("""
Welcome to the sentiment analysis platform.

This application is designed to:
- upload labelled datasets
- clean messy data
- prepare data for sentiment analysis
- support further analysis through DistilBERT

Use the navigation panel on the left to move between pages.
Start with **Upload and Clean**.
""")
