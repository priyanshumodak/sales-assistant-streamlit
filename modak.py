import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import openai
import os

# Load key from environment variable
openai.api_key = os.getenv("OPENROUTER_API_KEY")

# Use OpenRouter instead of OpenAI
openai.api_base = "https://openrouter.ai/api/v1"

# Example request
response = openai.ChatCompletion.create(
    model="openai/gpt-4o-mini",  # You can also try "anthropic/claude-3.5-sonnet"
    messages=[
        {"role": "system", "content": "You are a helpful sales assistant."},
        {"role": "user", "content": "Give me strategies to improve online sales conversions."}
    ]
)

print(response["choices"][0]["message"]["content"])

st.set_page_config(page_title="AI Business Insights", layout="wide")
st.title("📊 AI-Powered Business Insights Assistant")

st.write("Upload your business data (CSV/Excel), and get instant insights + visualizations with AI.")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Read the uploaded file
    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📂 Preview of Data")
    st.dataframe(df.head())

    # Basic Visualization
    st.subheader("📈 Quick Visualization")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if len(numeric_cols) >= 2:
        x_axis = st.selectbox("Select X-axis", options=numeric_cols)
        y_axis = st.selectbox("Select Y-axis", options=numeric_cols)

        fig, ax = plt.subplots()
        ax.plot(df[x_axis], df[y_axis], marker='o')
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f"{y_axis} vs {x_axis}")
        st.pyplot(fig)

    # Generate AI insights
    st.subheader("🤖 AI Insights")
    prompt = f"Analyze this business data and give key insights in simple language. Data sample:\n{df.head(20).to_string()}"

    if st.button("Generate Insights with AI"):
        with st.spinner("Analyzing data with OpenAI..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a business analyst who explains data in simple terms."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            insights = response["choices"][0]["message"]["content"]
            st.success(insights)

    # Interactive Q&A
    st.subheader("💬 Ask Questions About Your Data")
    user_question = st.text_input("Ask a question (e.g., Which month had the highest sales?)")

    if user_question:
        q_prompt = f"Here is some business data:\n{df.head(20).to_string()}\nNow answer this question: {user_question}"
        with st.spinner("Thinking..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful AI business data analyst."},
                    {"role": "user", "content": q_prompt}
                ],
                max_tokens=250
            )
            answer = response["choices"][0]["message"]["content"]
            st.info(answer)
