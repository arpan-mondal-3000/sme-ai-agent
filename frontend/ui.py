import streamlit as st
from app.agent import agent_executor

st.set_page_config(page_title="SME AI Consultant", page_icon="📊")

st.title("SME AI Business Consultant")

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
            result = agent_executor.invoke({"input": prompt})
            output = result.get("output", "").strip()

            FAILURE_SIGNALS = [
                "Agent stopped due to",
                "Thought:",
                "Action:",
                "Observation:",
                "Action Input:",
            ]

            if any(signal in output for signal in FAILURE_SIGNALS):
                response = (
                    "I couldn't form a complete answer. Please try:\n"
                    "- Breaking it into simpler questions\n"
                    "- Being more specific, e.g. *'What was the profit in June 2023?'*\n"
                    "- Then follow up with *'Suggest improvements based on that'*"
                )
            else:
                response = output

            st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })