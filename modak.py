import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai
import os

# -----------------------------
# Load OpenRouter API key from Streamlit secrets
# Make sure you added it as OPENROUTER_API_KEY in Streamlit Cloud secrets
openai.api_key = st.secrets["OPENROUTER_API_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"
# -----------------------------

st.set_page_config(page_title="Sales Assistant", layout="wide")
st.title("📊 AI Sales Assistant")

# Upload CSV
uploaded_file = st.file_uploader("Upload your sales CSV", type=["csv", "xlsx"])
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("Data Preview")
        st.dataframe(df.head())

        st.subheader("Basic Visualizations")
        numeric_cols = df.select_dtypes(include=["float", "int"]).columns.tolist()
        if numeric_cols:
            col = st.selectbox("Select column for histogram", numeric_cols)
            plt.figure(figsize=(8,4))
            plt.hist(df[col], bins=20, color="skyblue", edgecolor="black")
            plt.xlabel(col)
            plt.ylabel("Count")
            plt.title(f"Histogram of {col}")
            st.pyplot(plt)
        else:
            st.write("No numeric columns to visualize.")

        # Ask AI
        st.subheader("Ask AI about your sales data")
        user_question = st.text_input("Type your question here:")

        if user_question:
            # Convert DataFrame to CSV string for AI context
            data_str = df.head(100).to_csv(index=False)  # limit rows for performance

            prompt = f"""
You are an AI sales analyst. Here is a sample of the sales data (CSV format):
{data_str}

Answer the following question based on this data:
{user_question}
"""

            with st.spinner("Analyzing with AI..."):
                response = openai.chat.completions.create(
                    model="openai/gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful sales analyst."},
                        {"role": "user", "content": prompt}
                    ]
                )

                answer = response.choices[0].message.content
                st.subheader("AI Response")
                st.write(answer)

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a CSV or Excel file to get started.")
