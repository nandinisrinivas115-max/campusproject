import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(page_title="CampusGen AI", page_icon="🎓")

st.title("🎓 CampusGen AI")
st.subheader("Your AI College Admission Assistant")
st.write("Ask any question about college admissions!")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.5-flash-lite"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask any admission question...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=(
                    "You are CampusGen, a helpful college admission "
                    "assistant. Answer questions clearly and simply. "
                    "Never invent college-specific fees, deadlines, "
                    "or admission rules. If unsure, say so.\n\n"
                    + prompt
                )
            )
            answer = response.text or "Please try asking that again."
            st.write(answer)

        except Exception as e:
            answer = f"Error: {e}"
            st.error(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
