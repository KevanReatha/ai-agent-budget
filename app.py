import os
from dotenv import load_dotenv
import openai
import pandas as pd
import streamlit as st
from io import StringIO
import plotly.express as px
from prompts import build_categorization_prompt

# Load .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Budget Assistant", layout="wide")
st.title("💸 AI Budget Assistant")

uploaded_file = st.file_uploader("Upload your statement (CSV)", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ✅ Ensure Category column exists
    if "Category" not in df.columns:
        df["Category"] = "Uncategorised"
    else:
        df["Category"] = df["Category"].fillna("Uncategorised")

    st.subheader("📄 Preview of uploaded transactions")
    st.write(df.head(10))

    if st.button("Analyze Spending"):
        with st.spinner("Categorizing transactions..."):
            try:
                df_uncat = df[df["Category"] == "Uncategorised"].copy()

                if df_uncat.empty:
                    st.info("✅ All transactions are already categorized.")
                    result_df = df
                else:
                    # ✅ Optimization: chunking + essential columns only
                    chunk_size = 40
                    # ✅ Only include columns that exist in the DataFrame
                    possible_cols = ["Date", "Description", "Amount"]
                    essential_cols = [col for col in possible_cols if col in df_uncat.columns]
                    categorized_chunks = []

                    for i in range(0, len(df_uncat), chunk_size):
                        chunk = df_uncat.iloc[i:i + chunk_size]
                        csv_chunk = chunk[essential_cols].to_csv(index=False)
                        prompt = build_categorization_prompt(csv_chunk)

                        response = openai.chat.completions.create(
                            model="gpt-3.5-turbo",  # ✅ Cheaper model
                            messages=[
                                {"role": "system", "content": "You are a personal finance assistant."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.3
                        )

                        gpt_csv = response.choices[0].message.content.strip()
                        chunk_df = pd.read_csv(StringIO(gpt_csv))

                        # ✅ Restore index for proper merging
                        chunk_df.index = chunk.index
                        categorized_chunks.append(chunk_df)

                    df_ai = pd.concat(categorized_chunks).sort_index()
                    df.update(df_ai)
                    result_df = df.copy()

                # ✅ Convert Date
                result_df["Date"] = pd.to_datetime(result_df["Date"], errors="coerce")

                # ✅ Create AmountAbs for totals
                result_df["AmountAbs"] = result_df["Amount"].abs()

                # ✅ Summary table
                st.subheader("💰 Total by Category")
                summary = result_df.groupby("Category")["AmountAbs"].sum().reset_index()
                st.dataframe(summary)

                # ✅ Line chart by month
                result_df["Month"] = result_df["Date"].dt.to_period("M").astype(str)
                months = sorted(result_df["Month"].dropna().unique())
                selected_months = st.multiselect("📅 Select months to include", months, default=months)
                filtered = result_df[result_df["Month"].isin(selected_months)]

                if not filtered.empty:
                    fig = px.line(
                        filtered.sort_values("Date"),
                        x="Date",
                        y="AmountAbs",
                        color="Category",
                        title="📈 Spending Over Time by Category",
                        markers=True
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No data in selected months.")

            except Exception as e:
                st.error(f"Something went wrong: {e}")