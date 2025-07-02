import streamlit as st
import pandas as pd
import openai
from dotenv import load_dotenv
import os
from helpers import call_openai_to_categorize

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Budget Agent", layout="centered")
st.title("🧠 AI Budget Agent")

uploaded_file = st.file_uploader("📂 Upload your ING transaction file (.csv)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Preview of uploaded transactions")
    st.write(df.head())

    if st.button("Analyze Spending"):
        with st.spinner("Processing with GPT..."):
            result_df = call_openai_to_categorize(df)
        st.success("Analysis complete ✅")

        st.subheader("📊 Categorized Transactions")
        st.write(result_df)

        st.subheader("💰 Total by Category")
        st.write(result_df.groupby("Category")["Amount"].sum().sort_values(ascending=False))