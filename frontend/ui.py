# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.agent import agent_executor

st.set_page_config(page_title="SME AI Consultant", page_icon="📊")

st.title("📊 SME AI Business Consultant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask about your business data...")

if prompt:

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing business data..."):
            response = agent_executor.run(prompt)
            st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })