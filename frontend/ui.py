import streamlit as st
from app.agent import agent

st.title("SME AI Business Consultant")

query = st.text_input("Ask about your business")

if query:
    response = agent.run(query)
    st.write(response)