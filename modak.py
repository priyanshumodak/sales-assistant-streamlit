import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai  # Using OpenAI package, but pointing to OpenRouter only

# -----------------------------
# OpenRouter setup (ONLY)
openai.api_key = st.secrets["OPENROUTER_API_KEY"]
openai.api_base = "https://openrouter.ai/api/v1"  # Ensure OpenRouter is used
# -----------------------------

st.set_page_config(page_title="Sales Assistant", layout="wide")
st.title("🟢 AI Sales Assistant (OpenRouter Only)")

# Sample CSV for testing
sample_data = {
    "Product": ["A", "B", "C"],
    "Sales": [100, 150, 200],
    "Month": ["July", "July", "July"]
}
df = pd.DataFrame(sample_data)
st.subheader("Sample Data Preview")
st.dataframe(df)

# Simple histogram
plt.figure(figsize=(5,3))
plt.bar(df["Product"], df["Sales"], color="skyblue")
plt.title("Sales per Product")
plt.ylabel("Sales")
st.pyplot(plt)

# Ask AI question
st.subheader("Ask AI (OpenRouter)")
user_question = st.text_input("Example: Which product sold the most?")

if user_question:
    prompt = f"""
You are a helpful sales analyst. Here is sample sales data:
{df.to_csv(index=False)}

Answer this question: {user_question}
"""
    with st.spinner("Generating AI response from OpenRouter..."):
        response = openai.chat.completions.create(
            model="openai/gpt-oss-20b:free",  # OpenRouter free model
            messages=[
                {"role": "system", "content": "You are a helpful sales analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content
        st.subheader("AI Response")
        st.write(answer)

