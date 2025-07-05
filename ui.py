import streamlit as st
import json
from evaluator import evaluate_conversation_turn_async
import asyncio

st.title("Conversation Evaluator")
st.markdown("UI to demonstrate facet evaluator")

text_to_evaluate = st.text_area(
    "Enter text to evaluate:",
    "This service is terrible. I have been on hold for 45 minutes and I am extremely angry.",
    height=150
)

if st.button("Evaluate Text", type="primary"):
    if text_to_evaluate.strip():
        with st.spinner("Evaluating asynchronously....."):
            results = asyncio.run(evaluate_conversation_turn_async(text_to_evaluate))
            with open("results_1.json", "w") as f:
                json.dump(results, f, indent=2)
        st.success("Evaluation done")
        
        st.subheader("Full results")
        st.json(results)
    else:
        st.warning("Please enter some text to evaluate.")