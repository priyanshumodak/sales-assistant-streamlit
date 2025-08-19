# modak.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai

# -----------------------------
# Load OpenRouter API key from Streamlit Secrets
openai.api_key = st.secrets["OPENROUTER_API_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"
# -----------------------------

st.set_page_config(page_title="Sales Assistant Test", layout="wide")
st.title("🧪 Sales Assistant Test (Streamlit Cloud)")

# Test: API key length
st.write("API key length (should be >0):", len(st.secrets["OPENROUTER_API_KEY"]))

# Use a tiny built-in sample CSV
sample_data = {
    "Product": ["A", "B", "C"],
    "Sales": [100, 150, 200],
    "Month": ["July", "July", "July"]
}
df = pd.DataFrame(sample_data)
st.subheader("Sample Data Preview")
st.dataframe(df)

# Simple histogram for testing
plt.figure(figsize=(5,3))
plt.bar(df["Product"], df["Sales"], color="skyblue")
plt.title("Sales per Product")
plt.ylabel("Sales")
st.pyplot(plt)

# Test AI response
st.subheader("Ask AI (test question)")
user_question = st.text_input("Example: Which product sold the most?")

if user_question:
    prompt = f"""
You are a helpful sales analyst. Here is sample sales data:
{df.to_csv(index=False)}

Answer this question: {user_question}
"""
    with st.spinner("Generating AI response..."):
        response = openai.chat.completions.create(
            model="openai/gpt-oss-20b:free",  # Free OpenRouter model
            messages=[
                {"role": "system", "content": "You are a helpful sales analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content
        st.subheader("AI Response")
        st.write(answer)
